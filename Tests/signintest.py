import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



@pytest.fixture
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()

def test_signin_page(browser):
    browser.get("http://localhost:8000/signin")

    username_input = browser.find_element(By.ID,'username')
    password_input = browser.find_element(By.ID,'pass1')
    submit_button = browser.find_element(By.ID,'submit-button')

    username_input.send_keys('quin')
    password_input.send_keys('Hello@123')
    submit_button.click()

    welcome_message = browser.find_element(By.ID,'welcome-message')
    assert welcome_message.text == 'Welcome to ChatRoom!'

def test_bad_credentials(browser):
    browser.get("http://localhost:8000/signin")
    username_input = browser.find_element(By.ID,'username')
    password_input = browser.find_element(By.ID,'pass1')
    submit_button = browser.find_element(By.ID,'submit-button')

    username_input.send_keys('quin')
    password_input.send_keys('Hello@23')
    submit_button.click()
    bad_credentials_message=browser.find_element(By.ID,'bad-credentials')
    assert len(bad_credentials_message.text)>0


def test_view_group_without_signin(browser):
    browser.get("http://localhost:8000/group/creategroup")
    element=browser.find_element(By.ID,'username')
    assert element is not None