from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()   
    chrome_options.add_argument('--ignore-certificate-errors')
    service = Service('C:\\Users\\GAMEPLAY\\Documents\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver, email, password):
    driver.get("https://www.gigsberg.com/")
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span#login_btn.logged_out_btn"))
        )
        login_button.click()
    except:
        print("Login button not found or clickable. Trying with JavaScript.")
        login_button = driver.find_element(By.XPATH, "//span[@id='login_btn' and contains(@class, 'logged_out_btn')]")
        driver.execute_script("arguments[0].click();", login_button)
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_field = driver.find_element(By.NAME, "password")
    email_field.send_keys(email)
    password_field.send_keys(password)
    login_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_submit.click()

def navigate_to_account_settings(driver):
  
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    account_settings = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account-settings']"))
    )
    driver.execute_script("arguments[0].click();", account_settings)

    WebDriverWait(driver, 10).until(EC.url_contains("/account-settings"))
    print("Navigated to Account Settings!")

def fetch_email_address(driver):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "account_setting_personal"))
    )
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    
    email_address = email_input.get_attribute("value")
    print(f"Email Address: {email_address}")

def main():
    driver = setup_driver()
    try:
        login(driver, "your email address ", "your password")
        print("Login successful!")
        
        navigate_to_account_settings(driver)
        
        fetch_email_address(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
