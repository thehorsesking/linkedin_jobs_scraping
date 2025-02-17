#importing libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from datetime import datetime
from random import randrange
import csv
import re
import winsound


#get login details from txt file
def login_details():
    #open txt password file
    with open("rewahad_linkedin_password.txt",'r') as f:
        info = f.read().split("\n")

    email = info[0]
    password = info[1]       

    return email, password 

#read previous files for job_ids that were completed
def previous_file():
    df1 = pd.read_csv('jobs_20250207_114818.csv')
    df2 = pd.read_csv('jobs_20250207_165729.csv')
    df3 = pd.read_csv('jobs_20250208_095940.csv')
    df4 = pd.read_csv('jobs_20250208_101102.csv')
    
    previous_file = pd.concat([df1, df2,df3,df4], ignore_index=True)
    return previous_file['job_id'].values.tolist()

#defining global variables to use everywhere
def global_variable():
    global driver #makes the driver global keyword
    global wait #makes the wait global keyword
    global email, password, job_list, sleep_time, timestamp, csv_filename
    global previous_job_id
    previous_job_id = previous_file()
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    sleep_time= randrange(10)
    job_list = []
    email, password = login_details()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"jobs_{timestamp}.csv"


def sleep():
    time.sleep(sleep_time)   

# Write header only once when the file is created
def initialize_csv():
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["job_id","job_title","Company", "Location", "easy_apply", "job_url","job_description","email","jos_poster","jos_poster_profile"])  # Adjust columns as needed


# Append new job data to the CSV
def save_job(job_data):
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(job_data.values())
    print(f"Job saved: {job_data}")


#opening chrome webdriver
def open_chrome():
    # Set up Chrome WebDriver
    driver.maximize_window()

def open_webpage_sleep(url):
    try:
        driver.set_page_load_timeout(300)  # Increase timeout        
        driver.get(url)
        sleep()
    except TimeoutException:
        print(f"Timeout! Could not load: {url}")        

#opening linkedin job page
def open_linkedin_job_page(num):
    #url= f"https://www.linkedin.com/jobs/search/?alertAction=viewjobs&geoId=105117694&keywords=sql&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start={num}"
    url = f"https://www.linkedin.com/jobs/search/?alertAction=viewjob&geoId=105117694&keywords=data%20analyst&origin=JOBS_HOME_KEYWORD_AUTOCOMPLETE&start={num}"
    #url = f'https://www.linkedin.com/jobs/search/?alertAction=viewjob&geoId=105117694&keywords=analyst&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start={num}'
    open_webpage_sleep(url)


#clicking singin button on first page
def click_singin():
    #sign_in_button.click()
    try :
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-modal='base-sign-in-modal']")))
        sign_in_button.click()
        sleep()
    except :
        print('singin button not clicked ')
        

     

#sending login details
def send_login_details():
    #send email & password
    try:
        login_id = wait.until(EC.element_to_be_clickable((By.ID, "base-sign-in-modal_session_key")))
        login_id.clear()
        login_id.send_keys(email)

        sleep()

        login_pass = wait.until(EC.element_to_be_clickable((By.ID, "base-sign-in-modal_session_password")))
        login_pass.clear()
        login_pass.send_keys(password)
    except :
        print('Login detail not send. ')


#click singin after sending login details
def click_login_singin():
    #click sing in after password
    try:
        sleep()  # Wait for jobs to load

        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH , "//*[@id='base-sign-in-modal']//div[2]/button")))
        sign_in_button.click()
        print('Login button Clicked')
    except :
        print('Login button not clicked. ')

#find the scrollable element to scroll down
def find_scrollable_element():
    
    try:
        divs = driver.find_elements(By.XPATH, "//main[@id='main']//div")

        # Loop through divs and check if they have a scrollable overflow
        scrollable_div_class = None
        for div in divs:
            overflow_y = driver.execute_script("return window.getComputedStyle(arguments[0]).overflowY;", div)
            if overflow_y in ['auto', 'scroll']:
                scrollable_div_class = div.get_attribute("class")
                return scrollable_div_class
    
    except :
        print('Could not find scrollable element, Error:')

#scroll each page to get all job data
def scroll_job_search_page():

    scrollable_div_class = find_scrollable_element()

    try:
        scrollable_pane = driver.find_element(By.CLASS_NAME, scrollable_div_class)

        for _ in range(10):  
            driver.execute_script("arguments[0].scrollTop += 500", scrollable_pane)  # Scroll down step by step
            time.sleep(1)  # Wait for jobs to load
    except :
        print("Could not scroll page, Error:")


#scraping job search pages
def job_search_scraper():
    #scraping job data
    try:
        time.sleep(4)

        # Wait for job cards to load
        job_card = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.display-flex.job-card-container.relative.job-card-list[data-job-id]")
            )
        )
        # Extract 'data-job-id' and the text of the first job card
        if job_card:
            # Loop through all the job cards and extract the job IDs & job data
            for card in job_card:
                job_id = card.get_attribute("data-job-id").strip()
                lines = card.text.strip().splitlines()  # Split text into lines
                if 'Easy Apply' in lines:
                    easy_apply = 'Easy Apply'
                else :
                    easy_apply ='No'
                job_data = {
                "job_id": job_id,
                "job_title": lines[0],
                "company": lines[2],
                "location": lines[3],
                "easy_apply": easy_apply,
                "job_url" : 'https://www.linkedin.com/jobs/view/'+job_id+'/',
                "job_description": '',
                "email":'',
                "job_poster": '',
                "job_poster_profile": ''
                }
                if int(job_id) not in previous_job_id:
                    job_list.append(job_data)
                
        else:
            print("No job cards found.")
    except :
        print("job_search_scraper Error:")


#scrape job description from link
def job_description_scrape(job_id):

    try:
        #Click see more information button to get entire page
        see_more_button = driver.find_element(By.CLASS_NAME, "jobs-description__footer-button ")
        see_more_button.click()

        #job description from job page
        job_desc_div = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-box__html-content"))
            )

        for job_desc_html in job_desc_div:
            job_desc = job_desc_html.text


    except :
        print('Job description not found')
        job_desc = None

    email_from_desc(job_id,job_desc)

    for job in job_list:
        if job['job_id'] == job_id:
            job['job_description'] = job_desc
        #append job description for that job_id


def email_from_desc(job_id, job_desc):
    
    job_description = str(job_desc)  # Convert to string in case of NaN or other types

    # Find email addresses
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', job_description)
    
    # Print job_id and emails found
    email_string = ", ".join(emails) if emails else None  # If no emails, set as None
    
    for job in job_list:
        if job['job_id'] == job_id:
            job['email'] = email_string


def job_poster_name(job_id):
    #job poster name
    try:
        job_poster_name_div = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-poster__name"))
            )

        for job_poster_name_html in job_poster_name_div:
            job_poster_name = job_poster_name_html.text
             
            #append name to the list
    except :
        print('Job poster name not found.')
        #append none in job_poster_name
        job_poster_name = None

    for job in job_list:
                if job['job_id'] == job_id:
                    job['job_poster'] = job_poster_name                   

def job_poster_profile(job_id):
    #job poster linkedin profile
    try:
        hirer_info_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hirer-card__hirer-information")))

        # Find the <a> tag inside this div
        profile_link = hirer_info_div.find_element(By.TAG_NAME, "a")

        # Get the href attribute
        profile_url = profile_link.get_attribute("href")

    except :
        print('Job poster profile link not found.')
        profile_url = None
    
        #add to list
    for job in job_list:
        if job['job_id'] == job_id:
                job['job_poster_profile'] = profile_url       


def save_job_search():
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"jobs_{timestamp}.csv"

    # Convert job_list to DataFrame and save
    df = pd.DataFrame(job_list)
    df.to_csv(csv_filename, index=False, encoding="utf-8")

    print(f"CSV file '{csv_filename}' saved successfully!")    




def main():
    
    num=0
    print("Is this a test run?")
    response = ''
    while response not in {"yes", "no"}:
        response = input("Please enter yes or no: ").lower()

    if response == "no":
        jobs_number = 975
        print(f'Running on entire 1000 jobs')
    else:
        jobs_number = num
        print(f'Running Test. Scraping {num+25} jobs')

    global_variable()
    initialize_csv()
    print('Opening Chrome')
    open_chrome()

    print('Opening linkedin page to login')
    open_linkedin_job_page(num)
    
    print('Clicking singin')
    click_singin()
    
    print('sending login details')
    send_login_details()
    
    print('Clicking singin after login details')
    click_login_singin()

    print('Starting Job search scraping')

    #open all pages from containing jobs from 0 to 1000. Maximum value of num can be 975
    while num<= jobs_number:
        print(f'Opening linked page with jobs till ',num+25)
        open_linkedin_job_page(num)
        
        print('Scrolling page down')
        scroll_job_search_page()
        
        print('Scraping Jobs')
        job_search_scraper()
        num+=25
    print('Job search scraping Complete')



    i=1
    total_jobs= len(job_list)
    print('Starting job description scraping')
    #scrape job description
    for job in job_list:
        print('Scraping job desc of ',i,'/',total_jobs)
        if i%25 == 0:
            winsound.Beep(500, 500)
        i+=1

        job_id = job['job_id']
        url= job['job_url']
        open_webpage_sleep(url)
        job_description_scrape(job_id)
        job_poster_name(job_id)
        job_poster_profile(job_id)
        
        save_job(job)
    print('Job description scraping Complete')

    print('Saving file')
    save_job_search()

main()    