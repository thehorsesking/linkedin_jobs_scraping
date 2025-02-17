# LinkedIn Job Scraper

## Overview

This project is a LinkedIn job scraper built using Selenium and Python. It automates the process of searching for jobs on LinkedIn, extracting relevant details, and saving them in a CSV file for further analysis.

## Features

1. Logs into LinkedIn using credentials stored in a text file.
2. Scrapes job listings based on specific search criteria.
3. Extracts job details such as:
  - Job ID
  - Job Title
  - Company Name
  - Location
  - Easy Apply availability
  - Job URL
  - Job Description
  - Recruiter Email (if available)
  - Job Poster Name & Profile URL
  - Scrolls through job listings to fetch more data.
  - Stores extracted job data in a structured CSV format.
  - Avoids duplicate job entries by checking against previously scraped jobs.

## Requirements

  - Python 3.x
  - Google Chrome (latest version recommended)
  - ChromeDriver (managed automatically using webdriver_manager)
  - Selenium
  - Pandas

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies by running:
    pip install selenium webdriver-manager pandas
3. Create a text file named linkedin_password.txt in the same directory, containing your LinkedIn login credentials in the following format:
    your_email@example.com
    your_password

## How to Use
1. Run the script:
    ```bash
    python script_name.py
2. The script will prompt if you want to run a test (scraping a small number of jobs) or the full process.
3. The scraper will:
    - Open LinkedIn in Chrome.
    - Log in automatically.
    - Search for jobs matching the defined criteria.
    - Scroll through and collect job listings.
    - Extract detailed job information, including descriptions and recruiter details.
    - Save all data into a CSV file named in the format jobs_YYYYMMDD_HHMMSS.csv.

### Notes
  - Ensure you are logged out of LinkedIn in Chrome before running the script.
  - The script waits for elements dynamically to handle LinkedIn’s loading times.
  - If LinkedIn detects automation, you might face temporary access restrictions. Running with randomized delays (sleep_time) helps avoid detection.

## Disclaimer
This project is for educational purposes only. Scraping LinkedIn data is subject to LinkedIn's terms of service, and misuse could result in account restrictions. Use responsibly.
