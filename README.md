# WebScraper

**WebScraper** is a Python-based project designed to scrape course data from several University of California, San Diego (UCSD) course catalog websites. Utilizing the **Selenium** and **BeautifulSoup** libraries, this scraper extracts course information and formats it into an organized structure. The formatted data is then ready for direct insertion into a MySQL database, which supports another project of mine, [UCSD_Course_Finder](https://github.com/JoshCaneday/UCSD_Course_Finder).

The goal of this project is to simplify the process of collecting and organizing course data from UCSD’s websites. You can adapt this project for other universities or data collection purposes by modifying the scraping targets and structure however much of the scripts in this project were specifically designed for the UCSD websites so you may have to change quite a few things. Additionally, the formatting that was implemented into this project was geared toward my other project; as I said before. So, if you would also like to format the data that is being scraped differently, you would need to change that aspect as well.

## Features
- **Web scraping automation**: Automatically navigates UCSD’s course catalog websites using Selenium.
- **Efficient data parsing**: Extracts relevant course information using BeautifulSoup.
- **Data formatting**: Structures data to be compatible with a MySQL database for quick insertion.
- **Reusable**: The scraper can be adapted to other web pages with similar structures.

## Prerequisites
Before running this project, ensure that you have the following installed:

- **Python 3.6+**
- **Web driver** (e.g., ChromeDriver for Selenium, compatible with your browser)

## Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JoshCaneday/WebScraper.git
   cd WebScraper
2. **Install required dependencies**:
   You will need to install the necessary libraries for Selenium and BeautifulSoup, as well as other dependencies.
   
   a. Install Selenium
   ```bash
   pip install selenium
    ```
   b. Install BeautifulSoup
   ```bash
   pip install beautifulsoup4
   ```
   c. Install other dependencies
   ```bash
   pip install requests
   ```
4. **Download a Web Driver**:
   Selenium requires a web driver to interact with the browser. You need to download the driver for your browser:
   
   Chrome: Download ChromeDriver (Make sure to get the latest version, or whatever version that is currently compatible)
   
   Firefox: Download GeckoDriver (Make sure to get the latest version, or whatever version that is currently compatible)
   
   Ensure the driver is in your system's PATH or provide its path in the script when initializing Selenium.
6. **Set Parameters**:
   Within the two python files, scrapeScheduleofClasses.py and scrapeCourseCatalog.py, at the top of each file are a few parameters that need to be set. These depend on which part
   of the UCSD course catalog websites you want to scrape from. For example, scraping data on all of the CSE courses would be different from scraping the data on all of the BENG courses.
7. **Run the Scraper**:
   ```bash
   python formatData.py
   ```

