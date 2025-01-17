import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

form_link = "https://docs.google.com/forms/d/e/1FAIpQLScaDxyT9NQIHh1cVgbTDggl2Dm4iusYEbNGVhLfmG4yvq0bLQ/viewform?usp=header"

def fill_form(browser, email):
    wait = WebDriverWait(browser, 10)

    # Fill text fields (assuming the first text field is for email)
    text_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")))
    if text_fields:
        text_fields[0].send_keys(email)
        time.sleep(1)
    
    # Select MCQ answers
    mcq_questions = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='radiogroup']")))
    for question in mcq_questions:
        try:
            options = question.find_elements(By.XPATH, ".//div[@role='radio']")
            if options:
                random.choice(options).click()
                time.sleep(1)
        except Exception:
            print("No selectable option found for a question, skipping...")
    
    # Submit form
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
    emails = []
    
    # Collect unique Gmail addresses from the user
    for i in range(num_submissions):
        email = input(f"Enter Gmail address {i+1}: ")
        emails.append(email)
    
    random.shuffle(emails)  # Shuffle the list to ensure randomness
    
    options = webdriver.ChromeOptions()
    options.add_argument("-incognito")
    browser = webdriver.Chrome(options=options)

    for email in emails:
        browser.get(form_link)
        time.sleep(2)
        fill_form(browser, email)
    
    browser.quit()

if __name__ == "__main__":
    main()
