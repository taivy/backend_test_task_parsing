import logging
import sys
import time
import random
from functools import wraps
import traceback

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


SITE_SEARCH_URL = "https://www.peoplesearchexpert.com/people/"

# write logs to stdout
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def driver_exceptions_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (NoSuchElementException, TimeoutException) as e:
            traceback.print_exc()
            func_name = func.__name__
            logging.error("Error parsing site at function %s: %s",
                          func_name, str(e))

    return inner


def get_driver():
    chrome_options = webdriver.ChromeOptions()

    # make driver run in headless mode
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1600,900")
    chrome_options.add_argument('--disable-gpu')

    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_options.experimental_options["prefs"] = chrome_prefs

    driver = webdriver.Chrome(options=chrome_options)

    return driver


@driver_exceptions_handler
def go_to_search_results_page(
        driver, first_name, last_name, middle_initial, city, state):
    wait = WebDriverWait(driver, 30)

    driver.get(SITE_SEARCH_URL)

    # randomize waiting time to have less chance of being detected as bot
    time.sleep(random.randint(1, 5))
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//form[@class="navbar-form"]')))

    full_name = ' '.join(
        [first_name or '', middle_initial or '', last_name or ''])

    driver.find_element_by_xpath(
        '//form[@class="navbar-form"]//input[@name="q[full_name]"]').send_keys(full_name)

    # handle typeahead dropdown
    # input city, wait for dropdown, input state (doesn't work if insert city
    # and state in one go)
    driver.find_element_by_xpath(
        '//form[@class="navbar-form"]//input[@name="q[location]"]').send_keys(city)
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH,
             '//ul[contains(@class, "typeahead") and contains(@class, "dropdown-menu")]')))
    driver.find_element_by_xpath(
        '//form[@class="navbar-form"]//input[@name="q[location]"]').send_keys(' ')
    for char in state:
        driver.find_element_by_xpath(
            '//form[@class="navbar-form"]//input[@name="q[location]"]').send_keys(char)

    driver.find_element_by_xpath(
        '//button[contains(text(), "Search Records")]').click()
    wait.until(EC.visibility_of_element_located((By.ID, 'search-results')))
    try:
        driver.find_element_by_xpath(
            '//h3[contains(text(), "your query returned no match")]')
        return None
    except NoSuchElementException:
        pass
    return driver.current_url


@driver_exceptions_handler
def get_concrete_results_page(driver, city, state):
    wait = WebDriverWait(driver, 30)

    driver.find_element_by_xpath(
        '//a[contains(text(), "View Details")]').click()
    wait.until(EC.visibility_of_element_located((By.ID, 'personad-records')))

    try:
        driver.find_element_by_xpath(
            '//button[contains(text(), "Show More")]').click()
    except NoSuchElementException:
        # no "Show more" button since there are little options and it's not
        # needed
        pass

    state_name_formatted = state.title()
    city_name_formatted = city.title()

    driver.find_element_by_xpath(
        '//div[contains(@class, "match-by-state-list")]' +
        f'//button[contains(text(), "{state_name_formatted}")]/..').click()
    time.sleep(random.randint(1, 2))

    city_link_elem = driver.find_element_by_xpath(
        '//div[contains(@class, "match-by-state-list")]' +
        f'//button[contains(text(), "{city_name_formatted}")]/..')

    city_link = city_link_elem.get_attribute('href')
    return city_link


def get_search_results(first_name, last_name, middle_initial,
                       city, state, general_results_page=False):
    driver = get_driver()
    result_link = go_to_search_results_page(
        driver, first_name, last_name, middle_initial, city, state)

    if general_results_page:
        driver.close()
        return result_link

    result_link = get_concrete_results_page(driver, city, state)
    driver.close()
    return result_link
