from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Assuming you have a dataframe 'data' with a column 'variable_name'

def from_candidate_to_linkedin_link(data, variable_name : str):
    # Initialize 'li_urls' column as empty list
    data['li_urls'] = ''
    
    # Configure Chrome options for headless mode
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Run in headless mode (no browser window)

    # Initialize Chromedriver with configured options and executable path
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    
    # Open Google in the browser
    driver.get('https://www.google.com')
    time.sleep(2)
        
    reject_button = driver.find_element(By.XPATH, '//div[text()="Alles afwijzen"]')
    reject_button.click()

    for index, row in data.iterrows():
        name = row[variable_name]
        
        # Find the search bar, input the search query, and press Enter
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('site:nl.linkedin.com ' + name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # Find all the search results
        search_results = driver.find_elements(By.CSS_SELECTOR,'div.yuRUbf')

        # Extract the first and second LinkedIn URLs from the search results
        linkedin_urls = []
        for result in search_results:
            element = result.find_element(By.CSS_SELECTOR, 'a')
            url = element.get_attribute('href')
            if 'linkedin.com' in url:
                linkedin_urls.append(url)
                if len(linkedin_urls) == 2:
                    break
                
        # Update the 'li_urls' column with the LinkedIn URLs
        data.at[index, 'li_urls'] = linkedin_urls
        
        # Go back to google main page
        driver.get('https://www.google.com')
    # Close the browser session
    driver.quit()

data = pd.read_csv('../data/tk2021/csv/Telling_TK2021_gemeente_Zeewolde.eml_per_candidate_corrected.csv')
data['fullname'] = data['firstname'].fillna('') + ' ' + data['prefix'].fillna('') + data['lastname'].fillna('')
from_candidate_to_linkedin_link(data, 'fullname')