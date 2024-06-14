Automated App Review Extraction from Google Play Store
This project automates the extraction of app reviews from the Google Play Store using Selenium, BeautifulSoup, and pandas. It efficiently handles dynamic content loading, pagination, and error handling to scrape reviews and save them into structured Excel files for easy analysis.

Features
Automated Login & Navigation: Logs into the reviewapp.mobi platform and navigates to each app's review page.
Data Extraction: Parses review data, including user ratings and review content.
Data Transformation & Storage: Stores the extracted data into individual Excel files.
Dynamic Web Scraping: Handles dynamic content loading and pagination.
Batch Processing: Processes multiple apps' reviews in a single run.
Error Handling: Manages stale element references and page load issues.
Prerequisites
Python 3.x
Google Chrome
ChromeDriver (compatible with your Chrome version)
Selenium
BeautifulSoup
pandas
Installation
Usage
Open get_data_and_parse.py and replace the placeholder email and password in the login function with your credentials for reviewapp.mobi.

Optionally, update the data_to_parse list with your desired apps and their corresponding Google Play Store URLs and dates.

Run the script:
The script will:

Log into reviewapp.mobi.
Navigate to each app's review page.
Extract and save review data into HTML files.
Convert the HTML files to Excel files with structured data, including ratings.
Note
Manual Intervention: The script will handle pagination automatically. However, if a button is not detected, you may need to manually click the "Next" button and rerun the script.
Date Configuration: You can edit the date in the data_to_parse list to customize the date range for the reviews you want to extract.
