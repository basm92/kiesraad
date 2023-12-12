from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Assuming you have a dataframe 'data' with a column 'variable_name'

def from_candidate_to_linkedin_link(data, variable_name : str):

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (no browser window)

    # Initialize Chromedriver with configured options
    driver = webdriver.Chrome('path_to_chromedriver', options=chrome_options)  
    driver.maximize_window()

    for index, row in data.iterrows():
        name = row[variable_name]
        
        # Open Google in the browser
        driver.get('https://www.google.com')
        time.sleep(2)
        
        # Find the search bar, input the search query, and press Enter
        search_box = driver.find_element_by_name('q')
        search_box.send_keys(name + ' linkedin')
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # Find all the search results
        search_results = driver.find_elements_by_css_selector('div.r > a')
        
        # Extract the first and second LinkedIn URLs from the search results
        linkedin_urls = []
        for result in search_results:
            url = result.get_attribute('href')
            if 'linkedin.com' in url:
                linkedin_urls.append(url)
                if len(linkedin_urls) == 2:
                    break
        # Update the 'li_urls' column with the LinkedIn URLs
        data.at[index, 'li_urls'] = linkedin_urls

    # Close the browser session
    driver.quit()

