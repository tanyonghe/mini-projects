# Import required libraries.
from selenium import webdriver
from time import sleep
import schedule
import random


URL = 'https://myaces.nus.edu.sg/htd/htd'
CREDENTIALS_FILE = 'credentials.txt'

# Reads in user input for credentials and other information.
def get_input(filename):
    file = open(filename, 'r')
    return file.readlines() 


# Logs in with given username and password.
def login(browser, username_key, password_key):
    username = browser.find_element_by_id('userNameInput')
    username.send_keys(username_key)

    password = browser.find_element_by_id('passwordInput')
    password.send_keys(password_key)

    submit = browser.find_element_by_xpath('//*[@id="submitButton"]')
    submit.click()
    

# Submit temperature declarations for both AM and PM.
def submit_temperatures(browser, temperature_key):
    submit_temperature(browser, temperature_key, 'AM')
    
    sleep(0.3)
    back = browser.find_element_by_xpath("//input[@value='Back']")
    back.click()
    
    sleep(0.3)
    submit_temperature(browser, temperature_key, 'PM')


# Submit temperature declarations for specified day period (i.e. AM or PM).
def submit_temperature(browser, temperature_key, period):
    el = browser.find_element_by_name('declFrequency')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == period:
            option.click()
            break

    temperature = browser.find_element_by_id('temperature')
    temperature.send_keys(temperature_key)

    symptomsFlag = browser.find_element_by_name('symptomsFlag')
    symptomsFlag.click()

    save = browser.find_element_by_name('Save')
    save.click()


# Main function for declaring temperatures on the temperature declaration site.
def declare_temperature():
    user_input = get_input(CREDENTIALS_FILE)
    username_key = user_input[0].strip()
    password_key = user_input[1].strip()
    temperature_key = format(random.uniform(36.0, 36.5), '.1f')
    
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(URL)

    login(browser, username_key, password_key)
    submit_temperatures(browser, temperature_key)
    
    browser.quit()
    print("Finished declaring temperatures for today!")
    

# Main loop for running the schedule on a daily basis.
def main_loop():
    while 1:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    # Declare once for today.
    declare_temperature()
    
    # Declare once at 12 noon every day.
    schedule.every().day.at("12:00").do(declare_temperature)
    main_loop()
