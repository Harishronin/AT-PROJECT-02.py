"""
TestcaseID:TC_PIM_01

Test objective:
  Forgot password link validation on login page
URL= https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

Precondition:
1.Launch URL
2.OrangeHRM 3.0 site launched on a compatible browser
3.Click on “Forgot password” link
Steps
1.Username textbox is visible
2.Provide username
3.Click on Reset Password

Expected Result:
The user should be able to see the username box and get a successful message saying “Reset password link sent successfully”.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object Model for the OrangeHRM Login Page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.forgot_password_link = (By.LINK_TEXT, "Forgot your password?")
        self.username_textbox = (By.NAME, "username")
        self.reset_password_button = (By.XPATH, "//button[text()='Reset Password']")
        self.success_message = (By.XPATH, "//div[contains(@class, 'oxd-alert-success')]")

    def open(self, url):
        """Opens the login page."""
        self.driver.get(url)

    def click_forgot_password(self):
        """Clicks on the 'Forgot your password?' link."""
        self.wait.until(EC.element_to_be_clickable(self.forgot_password_link)).click()

    def is_username_textbox_visible(self):
        """Checks if the username textbox is visible."""
        return self.wait.until(EC.visibility_of_element_located(self.username_textbox)).is_displayed()

    def enter_username(self, username):
        """Enters the username in the textbox."""
        self.wait.until(EC.presence_of_element_located(self.username_textbox)).send_keys(username)

    def click_reset_password(self):
        """Clicks the Reset Password button."""
        self.wait.until(EC.element_to_be_clickable(self.reset_password_button)).click()

    def is_success_message_displayed(self):
        """Checks if the success message is displayed."""
        success_element = self.wait.until(EC.visibility_of_element_located(self.success_message))
        return "Reset password link sent successfully" in success_element.text
import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """Initializes the WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
import pytest
from pages.login_page import LoginPage


def test_forgot_password(driver):
    """
    Test Case: Validate the forgot password functionality on the login page.
    """
    # Test data
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"

    # Initialize Page Object
    login_page = LoginPage(driver)

    # Step 1: Open the login page
    login_page.open(url)

    # Step 2: Click on the "Forgot your password?" link
    login_page.click_forgot_password()

    # Step 3: Validate that the username textbox is visible
    assert login_page.is_username_textbox_visible(), "Username textbox is not visible."

    # Step 4: Provide username
    login_page.enter_username(username)

    # Step 5: Click on Reset Password button
    login_page.click_reset_password()

    # Step 6: Validate the success message
    assert login_page.is_success_message_displayed(), "Success message is not displayed."
    print("Test Passed: Forgot password functionality works as expected.")


"""
TestcaseID:TC_PIM_02
Test objective:
  Header validation on Admin page 
Precondition:
1.Launch URL and login as “Admin”
2.OrangeHRM 3.0 site launched on a compatible browser
Steps:
1.Go to Admin page and validate “Title of the page as OrangeHRM”
2.Validate below options are displaying on admin page
                 1.User management
                 2.Job
                3.Organizations
               4.Qualifications
               5.Nationalities
              6.Corporate banking
              7.Configuration

Expected Result:
The user should be able to see above mentioned Admin page headers on Admin page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminPage:
    """Page Object Model for the OrangeHRM Admin Page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.admin_link = (By.XPATH, "//span[text()='Admin']")

    def navigate_to_admin_page(self):
        """Navigates to the Admin page."""
        self.wait.until(EC.element_to_be_clickable(self.admin_link)).click()

    def validate_page_title(self, expected_title):
        """Validates the title of the page."""
        self.wait.until(lambda d: d.title == expected_title)
        assert self.driver.title == expected_title, f"Expected: {expected_title}, Found: {self.driver.title}"

    def are_headers_present(self, headers):
        """Validates the presence of specified headers on the Admin page."""
        for header in headers:
            header_xpath = (By.XPATH, f"//span[text()='{header}']")
            try:
                self.wait.until(EC.visibility_of_element_located(header_xpath))
                print(f"Header '{header}' is visible on the Admin page.")
            except Exception:
                print(f"Header '{header}' is NOT visible on the Admin page.")
                return False
        return True

import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """Initializes the WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

import pytest
from pages.login_page import LoginPage
from pages.admin_page import AdminPage


def test_admin_page_headers(driver):
    """
    Test Case: Validate headers on the Admin page.
    """
    # Test data
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"
    expected_title = "OrangeHRM"
    expected_headers = [
        "User Management",
        "Job",
        "Organization",
        "Qualifications",
        "Nationalities",
        "Corporate Banking",
        "Configuration"
    ]

    # Initialize Page Objects
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)

    # Step 1: Open the login page and log in as Admin
    login_page.open(url)
    login_page.login(username, password)

    # Step 2: Navigate to the Admin page
    admin_page.navigate_to_admin_page()

    # Step 3: Validate the title of the page
    admin_page.validate_page_title(expected_title)

    # Step 4: Validate the presence of expected headers
    assert admin_page.are_headers_present(expected_headers), "Not all headers are visible on the Admin page."



"""
TestcaseID:TC_PIM_03
Test objective:
  Main menu validation on Admin page 
Precondition:
1.Launch URL and login as “Admin”
2.OrangeHRM 3.0 site launched on a compatible browser
Steps:
             1.Go to admin Page
             2.Validate below “Menu options”(on side pane)displaying on Admin page

                 a.Admin
                 b.PIM
                 C.Time
                 d.Leave
                 e.Recruitment
                 f.My Info
                 g.Performance
                 h.Dashboard
                 i.Directory
                k.Maintainance
                l.Buzz

Ecpected Result: The user should able to see above mentioned Admin Page Menu items on Admin page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object Model for the OrangeHRM Login Page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.username_field = (By.NAME, "username")
        self.password_field = (By.NAME, "password")
        self.submit_button = (By.XPATH, "//button[@type='submit']")

    def open(self, url):
        """Opens the login page."""
        self.driver.get(url)

    def login(self, username, password):
        """Logs in using the provided username and password."""
        self.wait.until(EC.visibility_of_element_located(self.username_field)).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.submit_button).click()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdminPage:
    """Page Object Model for the OrangeHRM Admin Page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.admin_link = (By.XPATH, "//span[text()='Admin']")
        self.menu_option_xpath_template = "//span[text()='{}']"

    def navigate_to_admin_page(self):
        """Navigates to the Admin page."""
        self.wait.until(EC.element_to_be_clickable(self.admin_link)).click()

    def are_menu_options_present(self, menu_options):
        """
        Validates the presence of specified menu options on the Admin page.

        Args:
            menu_options (list): List of expected menu option texts.

        Returns:
            bool: True if all menu options are present, otherwise False.
        """
        all_visible = True
        for option in menu_options:
            option_xpath = (By.XPATH, self.menu_option_xpath_template.format(option))
            try:
                self.wait.until(EC.visibility_of_element_located(option_xpath))
                print(f"Menu option '{option}' is visible on the Admin page.")
            except Exception:
                print(f"Menu option '{option}' is NOT visible on the Admin page.")
                all_visible = False
        return all_visible
import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """Initializes the WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

import pytest
from pages.login_page import LoginPage
from pages.admin_page import AdminPage


def test_admin_menu_options(driver):
    """
    Test Case: Validate menu options on the Admin page.
    """
    # Test data
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"
    expected_menu_options = [
        "Admin",
        "PIM",
        "Time",
        "Leave",
        "Recruitment",
        "My Info",
        "Performance",
        "Dashboard",
        "Directory",
        "Maintenance",  
        "Buzz"
    ]

    # Initialize Page Objects
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)

    # Step 1: Open the login page and log in as Admin
    login_page.open(url)
    login_page.login(username, password)

    # Step 2: Navigate to the Admin page
    admin_page.navigate_to_admin_page()

    # Step 3: Validate the presence of expected menu options
    assert admin_page.are_menu_options_present(expected_menu_options), "Some menu options are missing on the Admin page."
