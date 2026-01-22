from pages.google_page import GooglePage

def test_open_google(driver):
    page = GooglePage(driver)
    page.open()

    assert "Google" in page.get_title()
