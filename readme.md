# 🚀 Project Belajar Selenium

Repository ini berisi **project pembelajaran Selenium** yang bertujuan untuk memahami dan mempraktikkan **automasi web testing** menggunakan Selenium WebDriver. Project ini cocok untuk pemula hingga menengah yang ingin belajar automasi testing secara terstruktur dan bertahap.

---

## 📌 Tujuan Project

* Memahami konsep dasar **Selenium WebDriver**
* Melakukan automasi interaksi browser (klik, input, submit, navigasi)
* Mengelola **locator** (ID, Name, XPath, CSS Selector)
* Mengimplementasikan **wait strategy** (Implicit & Explicit Wait)
* Melakukan testing pada website nyata maupun dummy
* Menerapkan **best practice** struktur project automasi

---

## 🧰 Teknologi yang Digunakan

* **Python** 3.9+
* **Selenium WebDriver**
* **Google Chrome / Mozilla Firefox**
* **ChromeDriver / GeckoDriver**
* (Opsional) **pytest** untuk test runner
* (Opsional) **virtualenv** untuk environment isolation

---

## 📁 Struktur Project

```
project-belajar-selenium/
│
├── drivers/                 # WebDriver (chromedriver/geckodriver)
├── tests/                   # File test selenium
│   ├── test_login.py
│   ├── test_form.py
│   └── test_navigation.py
│
├── pages/                   # Page Object Model (POM)
│   ├── login_page.py
│   └── home_page.py
│
├── utils/                   # Helper & utility
│   └── wait_helper.py
│
├── requirements.txt         # Dependency project
├── .gitignore
└── README.md
```

---

## ⚙️ Instalasi & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/project-belajar-selenium.git
cd project-belajar-selenium
```

### 2️⃣ Buat Virtual Environment (Disarankan)

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download WebDriver

* **ChromeDriver**: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
* **GeckoDriver**: [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

Pastikan versi WebDriver sesuai dengan versi browser.

Letakkan driver di folder `drivers/` atau tambahkan ke **PATH**.

---

## ▶️ Menjalankan Test

### Menjalankan file selenium biasa

```bash
python tests/test_login.py
```

### Menjalankan dengan pytest (jika digunakan)

```bash
pytest tests/
```

---

## 🧪 Contoh Test Case

* Login dengan data valid
* Login dengan data tidak valid
* Mengisi dan submit form
* Navigasi antar halaman
* Validasi title dan URL halaman
* Validasi element tampil/tidak tampil

---

## 🧠 Konsep yang Dipelajari

* WebDriver initialization
* Locator strategy (ID, XPath, CSS)
* Explicit Wait (`WebDriverWait`)
* Page Object Model (POM)
* Handling alert, iframe, dan window
* Screenshot otomatis saat error

---

## 📌 Best Practice yang Digunakan

* Menggunakan **Page Object Model (POM)**
* Tidak hardcode `sleep()` berlebihan
* Locator dibuat reusable
* Struktur folder rapi dan scalable
* Test mudah dibaca dan dipelihara

---

## 🐞 Troubleshooting Umum

**❌ WebDriver tidak ditemukan**

> Pastikan driver sesuai OS dan browser

**❌ ElementNotInteractableException**

> Gunakan Explicit Wait

**❌ TimeoutException**

> Periksa locator dan waktu wait

---

## 📚 Referensi

* [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/)
* [https://www.w3schools.com/python/](https://www.w3schools.com/python/)
* [https://docs.pytest.org/](https://docs.pytest.org/)

---

## 📈 Rencana Pengembangan

* [ ] Integrasi pytest
* [ ] Reporting (Allure / HTML Report)
* [ ] Parallel testing
* [ ] CI/CD (GitHub Actions)

---

## 🤝 Kontribusi

Project ini bersifat **belajar**. Silakan fork dan kembangkan sesuai kebutuhan.

---

## 📝 Lisensi

Project ini menggunakan lisensi **MIT**.

---

✨ *Happy Testing & Happy Learning Selenium!*
