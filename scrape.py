from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests


service = Service(executable_path='C:/Drivers/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm')

select_element = driver.find_element(By.ID, "selectedSubjects")
select = Select(select_element)
select.select_by_value("MATH") # Respective to the major


submit_button = driver.find_element(By.ID, "socFacSubmit")
submit_button.click()

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
courses = soup.findAll("span", attrs={"class":"boldtxt", "onclick": None}) # course title
professors = soup.findAll("a", attrs={"href":"#!"}) # professor name

course_lines = []
def binarysearch(l, r, target):
    targetVal = target[0]
    m = ((l + r) // 2) + 1
    while l < r:
        if targetVal == course_lines[m]:
            course_lines.insert(m, targetVal)
        if targetVal < course_lines[m]:
            r = m
        


for j in range(len(courses)):
    if j == 0 or courses[j] != courses[j-1]:
        course_lines.append((courses[j].sourceline,courses[j].text, 0))
        print(courses[j].text + courses[j].sourceline)

for j in range(len(professors)):
    if j == 0 or professors[j] != professors[j-1]:
        binarysearch(0,len(course_lines), (professors[j].sourceline,professors[j].text,1))
        print(professors[j].text, professors[j].sourceline)

#Repeat the above for as many pages as there are remaining
for i in range(2,2): # Respective to the number of pages (starts page 2, goes to page 11)
    link_element = driver.find_element(By.LINK_TEXT, str(i))
    link_element.click()

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    courses = soup.findAll("span", attrs={"class":"boldtxt", "onclick": None}) # course title
    professors = soup.findAll("a", attrs={"href":"#!"}) # professor name
    for j in range(len(courses)):
        if j == 0 or courses[j] != courses[j-1]:
            print(courses[j].text)
    for j in range(len(professors)):
        if j == 0 or professors[j] != professors[j-1]:
            print(professors[j].text)

driver.quit()

