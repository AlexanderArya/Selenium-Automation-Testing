from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
import re
import subprocess
import threading
from datetime import datetime
from pathlib import Path
import glob
import time

app = Flask(__name__)
CORS(app)

# Konfigurasi
LOG_FOLDER = os.path.join(os.path.dirname(__file__), 'logs')
TEST_FOLDER = os.path.join(os.path.dirname(__file__), 'tests')
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(TEST_FOLDER, exist_ok=True)

# Global state untuk tracking test execution
test_executions = {}

class LogParser:
    """Parser untuk file log dengan berbagai format"""
    
    @staticmethod
    def parse_text_log(file_path):
        logs = []
        pattern = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}),\d+\s-\s(\w+)\s-\s(.+)'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    match = re.match(pattern, line.strip())
                    if match:
                        timestamp, level, message = match.groups()
                        logs.append({
                            'timestamp': timestamp,
                            'level': level,
                            'message': message
                        })
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return logs
    
    @staticmethod
    def parse_json_log(file_path):
        logs = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Error parsing JSON log {file_path}: {e}")
        
        return logs

class TestMetricsAnalyzer:
    """Analyzer untuk metrik test automation"""
    
    @staticmethod
    def analyze_test_results(logs):
        metrics = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'warnings': 0,
            'total_duration': 0,
            'test_cases': [],
            'execution_timeline': []
        }
        
        for log in logs:
            level = log.get('level', '').upper()
            
            if level == 'ERROR':
                metrics['errors'] += 1
            elif level == 'WARNING':
                metrics['warnings'] += 1
            
            message = log.get('message', '')
            
            if 'PASSED' in message or 'SUCCESS' in message:
                metrics['passed'] += 1
                metrics['total_tests'] += 1
            elif 'FAILED' in message or 'FAIL' in message:
                metrics['failed'] += 1
                metrics['total_tests'] += 1
            
            duration_match = re.search(r'duration[:\s]+(\d+\.?\d*)\s*(s|ms|sec)', message, re.IGNORECASE)
            if duration_match:
                duration = float(duration_match.group(1))
                unit = duration_match.group(2)
                if unit in ['ms']:
                    duration = duration / 1000
                metrics['total_duration'] += duration
            
            test_match = re.search(r'test[_\s](\w+)|Test Case[:\s]+([^\s]+)', message, re.IGNORECASE)
            if test_match:
                test_name = test_match.group(1) or test_match.group(2)
                status = 'passed' if 'PASSED' in message or 'SUCCESS' in message else 'failed'
                metrics['test_cases'].append({
                    'name': test_name,
                    'status': status,
                    'timestamp': log.get('timestamp', '')
                })
        
        if metrics['total_tests'] > 0:
            metrics['pass_rate'] = round((metrics['passed'] / metrics['total_tests']) * 100, 2)
            metrics['fail_rate'] = round((metrics['failed'] / metrics['total_tests']) * 100, 2)
            metrics['avg_duration'] = round(metrics['total_duration'] / metrics['total_tests'], 2)
        else:
            metrics['pass_rate'] = 0
            metrics['fail_rate'] = 0
            metrics['avg_duration'] = 0
        
        return metrics

class TestRunner:
    """Class untuk menjalankan test automation"""
    
    @staticmethod
    def run_python_test(test_file, execution_id):
        """Run Python test file"""
        try:
            test_path = os.path.join(TEST_FOLDER, test_file)
            
            # Update status
            test_executions[execution_id]['status'] = 'running'
            test_executions[execution_id]['start_time'] = datetime.now().isoformat()
            
            # Run test menggunakan subprocess
            result = subprocess.run(
                ['python', test_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # Update hasil
            test_executions[execution_id]['status'] = 'completed'
            test_executions[execution_id]['end_time'] = datetime.now().isoformat()
            test_executions[execution_id]['exit_code'] = result.returncode
            test_executions[execution_id]['stdout'] = result.stdout
            test_executions[execution_id]['stderr'] = result.stderr
            
        except Exception as e:
            test_executions[execution_id]['status'] = 'failed'
            test_executions[execution_id]['error'] = str(e)
    
    @staticmethod
    def run_pytest_test(test_file, execution_id):
        """Run Pytest test file"""
        try:
            test_path = os.path.join(TEST_FOLDER, test_file)
            
            test_executions[execution_id]['status'] = 'running'
            test_executions[execution_id]['start_time'] = datetime.now().isoformat()
            
            # Run pytest dengan output verbose
            result = subprocess.run(
                ['pytest', test_path, '-v', '--tb=short'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            test_executions[execution_id]['status'] = 'completed'
            test_executions[execution_id]['end_time'] = datetime.now().isoformat()
            test_executions[execution_id]['exit_code'] = result.returncode
            test_executions[execution_id]['stdout'] = result.stdout
            test_executions[execution_id]['stderr'] = result.stderr
            
        except Exception as e:
            test_executions[execution_id]['status'] = 'failed'
            test_executions[execution_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/logs')
def get_logs():
    level_filter = request.args.get('level', None)
    file_filter = request.args.get('file', None)
    
    all_logs = []
    log_files = glob.glob(os.path.join(LOG_FOLDER, '*.log')) + \
                glob.glob(os.path.join(LOG_FOLDER, '*.json'))
    
    for log_file in log_files:
        if file_filter and file_filter not in os.path.basename(log_file):
            continue
        
        if log_file.endswith('.json'):
            logs = LogParser.parse_json_log(log_file)
        else:
            logs = LogParser.parse_text_log(log_file)
        
        for log in logs:
            log['source_file'] = os.path.basename(log_file)
            all_logs.append(log)
    
    if level_filter:
        all_logs = [log for log in all_logs if log.get('level', '').upper() == level_filter.upper()]
    
    all_logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({
        'success': True,
        'count': len(all_logs),
        'logs': all_logs
    })

@app.route('/api/metrics')
def get_metrics():
    all_logs = []
    log_files = glob.glob(os.path.join(LOG_FOLDER, '*.log')) + \
                glob.glob(os.path.join(LOG_FOLDER, '*.json'))
    
    for log_file in log_files:
        if log_file.endswith('.json'):
            logs = LogParser.parse_json_log(log_file)
        else:
            logs = LogParser.parse_text_log(log_file)
        all_logs.extend(logs)
    
    metrics = TestMetricsAnalyzer.analyze_test_results(all_logs)
    
    return jsonify({
        'success': True,
        'metrics': metrics
    })

@app.route('/api/tests/list')
def list_tests():
    """List semua test files yang tersedia"""
    test_files = []
    
    # Scan Python test files
    py_files = glob.glob(os.path.join(TEST_FOLDER, 'test_*.py'))
    
    for test_file in py_files:
        stat = os.stat(test_file)
        test_files.append({
            'name': os.path.basename(test_file),
            'path': test_file,
            'type': 'python',
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'success': True,
        'tests': test_files
    })

@app.route('/api/tests/run', methods=['POST'])
def run_test():
    """Endpoint untuk menjalankan test"""
    data = request.get_json()
    test_file = data.get('test_file')
    test_type = data.get('test_type', 'python')
    
    if not test_file:
        return jsonify({
            'success': False,
            'error': 'test_file is required'
        }), 400
    
    # Generate execution ID
    execution_id = f"exec_{int(time.time())}_{test_file}"
    
    # Initialize execution tracking
    test_executions[execution_id] = {
        'test_file': test_file,
        'test_type': test_type,
        'status': 'queued',
        'start_time': None,
        'end_time': None,
        'exit_code': None,
        'stdout': '',
        'stderr': '',
        'error': None
    }
    
    # Run test di background thread
    if test_type == 'pytest':
        thread = threading.Thread(
            target=TestRunner.run_pytest_test,
            args=(test_file, execution_id)
        )
    else:
        thread = threading.Thread(
            target=TestRunner.run_python_test,
            args=(test_file, execution_id)
        )
    
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'execution_id': execution_id,
        'message': f'Test {test_file} started'
    })

@app.route('/api/tests/status/<execution_id>')
def get_test_status(execution_id):
    """Get status eksekusi test"""
    if execution_id not in test_executions:
        return jsonify({
            'success': False,
            'error': 'Execution not found'
        }), 404
    
    return jsonify({
        'success': True,
        'execution': test_executions[execution_id]
    })

@app.route('/api/tests/history')
def get_test_history():
    """Get history semua eksekusi test"""
    history = []
    for exec_id, exec_data in test_executions.items():
        history.append({
            'execution_id': exec_id,
            **exec_data
        })
    
    # Sort by start time (terbaru dulu)
    history.sort(key=lambda x: x.get('start_time', ''), reverse=True)
    
    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'success': True,
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)