import requests
from requests.exceptions import HTTPError

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

'''
    Helper module for sending request or getting the page source by
    opening headless browser, respectively 'get_response' and 'get_page_content'
'''


TIMEOUT = 100


'''
    Returning the page content by PhantomJS

    :param: (str) url - the given URL for sending request
    :param: (str) waitSelector - CSS Selector for waiting for the loading component

    :return: (str) content - the obtained page content
'''

def get_page_content(url, waitComponent = None):
    # Page content
    content = None

    try:
        # Configurations for headless browser
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # Headless browser
        driver = webdriver.Chrome(options = options)

        # Going to the URL
        driver.get(url)

        # Wait until loaded: (Wait until a row is loaded)
        if waitComponent:
            WebDriverWait(driver, TIMEOUT).until(waitComponent)

        # Storing the content
        content = driver.page_source

        # Exiting
        driver.quit()

    except Exception as err:
        print(f"[ERROR]: {err}")

    # Returning the content
    return content


'''
    Returns the response of the requests to the given url

    :param: (str) url - the given URL for sending request
    :return: (str) response - the obtained response
'''

def get_response(url):
    # Response
    response = None

    try:
        # Sending request to the URL
        response = requests.get(URL)

        # Status of the response
        response.raise_for_status()

    except HTTPError as err:
        print(f'HTTP error occurred: {err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Request is successful!')

    # Returning the response
    return response
