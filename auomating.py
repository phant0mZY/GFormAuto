import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

form_link = "https://docs.google.com/forms/d/e/1FAIpQLScaDxyT9NQIHh1cVgbTDggl2Dm4iusYEbNGVhLfmG4yvq0bLQ/viewform?usp=header"

def fill_form(browser):
    wait = WebDriverWait(browser, 10)

    mcq_questions = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='radiogroup']")))

    for question in mcq_questions:
        try:
            options = question.find_elements(By.XPATH, ".//div[@role='radio']")
            if options:
                random.choice(options).click()
                time.sleep(1)
        except Exception:
            print("No selectable option found for a question, skipping...")

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']")))
    submit_button.click()
    time.sleep(3)

    try:
        submit_another = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Submit another response")))
        submit_another.click()
        time.sleep(2)
    except Exception:
        print("No 'Submit another response' button found, stopping.")

def main():
    num_submissions = int(input("Enter the number of times you want to submit the form: "))

    options = webdriver.ChromeOptions()
    options.add_argument("-incognito")

    browser = webdriver.Chrome(options=options)

    for _ in range(num_submissions):
        browser.get(form_link)
        time.sleep(2)
        fill_form(browser)

        browser.close()

        browser = webdriver.Chrome(options=options)

    browser.quit()

if __name__ == "__main__":
    main()
