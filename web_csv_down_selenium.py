import os
import time
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import ui, expected_conditions as EC


def main():
    dl_dir = '/tmp'  # temporary download dir so I don't spam the real dl dir with csv files
    # check what files are downloaded before the scraping starts (will be explained later)
    csvs_old = {file for file in os.listdir(dl_dir) if file.startswith('NXSA-Results-') and file.endswith('.csv')}

    # I use chrome so check if you have chromedriver installed
    # pass custom dl dir to browser instance
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : '/tmp'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # open page
    driver.get('http://nxsa.esac.esa.int/nxsa-web/#search')

    # wait for search ui to appear (abort after 10 secs)
    # once there, unfold the filters panel
    ui.WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by.By.XPATH, '//td[text()="Observation and Proposal filters"]'))).click()
    # toggle observation availability dropdown
    driver.find_element_by_xpath('//input[@title="Observation Availability"]/../../td[2]/div/img').click()
    # wait until the dropdown elements are available, then click "proprietary"
    ui.WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by.By.XPATH, '//div[text()="Proprietary" and @class="gwt-Label"]'))).click()
    # unfold display options panel
    driver.find_element_by_xpath('//td[text()="Display options"]').click()
    # deselect "pointed observations"
    driver.find_element_by_id('gwt-uid-241').click()
    # select "epic exposures"
    driver.find_element_by_id('gwt-uid-240').click()

    # uncomment if you want to go through the activated settings and verify them
    # when commented, the form is submitted immediately
    #time.sleep(5)

    # submit the form
    driver.find_element_by_xpath('//button/span[text()="Submit"]/../img').click()
    # wait until the results table has at least one row
    ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((by.By.XPATH, '//tr[@class="MPI"]')))
    # click on save
    driver.find_element_by_xpath('//span[text()="Save table as"]').click()
    # wait for dropdown with "CSV" entry to appear
    el = ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by.By.XPATH, '//a[@title="Save as CSV, Comma Separated Values"]')))
    # somehow, the clickability does not suffice - selenium still whines about the wrong element being clicked
    # as a dirty workaround, wait a fixed amount of time to let js finish ui update
    time.sleep(1)
    # click on "CSV" entry
    el.click()

    # now. selenium can't tell whether the file is being downloaded
    # we have to do it ourselves
    # this is a quick-and-dirty check that waits until a new csv file appears in the dl dir
    # replace with watchdogs or whatever
    dl_max_wait_time = 10  # secs
    seconds = 0
    while seconds < dl_max_wait_time:
        time.sleep(1)
        csvs_new = {file for file in os.listdir(dl_dir) if file.startswith('NXSA-Results-') and file.endswith('.csv')}
        if csvs_new - csvs_old:  # new file found in dl dir
            print('Downloaded file should be one of {}'.format([os.path.join(dl_dir, file) for file in csvs_new - csvs_old]))
            break
        seconds += 1

    # we're done, so close the browser
    driver.close()


# script entry point
if __name__ == '__main__':
    main()
