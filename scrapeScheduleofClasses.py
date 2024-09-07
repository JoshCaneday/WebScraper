from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

numPages = 11 #Number of pages
department = 'MATH' #Chosen department
maxLinesinFile = 10000 # Find the file/page with the most lines and set this variable to that, double it for good measure





service = Service(executable_path='C:/Drivers/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm')

select_element = driver.find_element(By.ID, "selectedSubjects")
select = Select(select_element)
select.select_by_value(department)


submit_button = driver.find_element(By.ID, "socFacSubmit")
submit_button.click()

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
courses = soup.find_all("span", attrs={"class":"boldtxt", "onclick": None}) # course title
professors = soup.find_all("a", attrs={"href":"#!"}) # professor name
courseNumbers = soup.find_all("td", attrs={"class":"crsheader", "colspan": None}) # course number


course_lines = []
def binarysearch(l, r, target):
    targetVal = target[0]
    while l < r:
        m = ((l + r) // 2)
        #print(course_lines[m], m, l, r)
        if targetVal < course_lines[m][0]:
            r = m
        else:
            l = m + 1
    if targetVal >= course_lines[m][0]:
        course_lines.insert(m+1,target)
    else:
        course_lines.insert(m,target)


# Below is for Courses

for j in range(len(courses)):
    if j == 0 or courses[j] != courses[j-1]:
        #course_lines.append((courseNumbers[(j*2)].sourceline+maxLinesinFile,courseNumbers[(j*2)].text, 1))
        course_lines.append((courses[j].sourceline+maxLinesinFile,courses[j].text, 0, courseNumbers[(j*2)+1].text))
        #print(courses[j].text, courses[j].sourceline)

#Repeat the above for as many pages as there are remaining
for i in range(2,numPages+1):
    link_element = driver.find_element(By.LINK_TEXT, str(i))
    link_element.click()

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    courses = soup.find_all("span", attrs={"class":"boldtxt", "onclick": None}) # course title
    courseNumbers = soup.find_all("td", attrs={"class":"crsheader", "colspan": None}) # course number
    for j in range(len(courses)):
        if j == 0 or courses[j] != courses[j-1]:
            course_lines.append((courses[j].sourceline + i*maxLinesinFile,courses[j].text, 0, courseNumbers[(j*2)+1].text))
            #print(courses[j].text, courses[j].sourceline)

#print(course_lines)
link_element = driver.find_element(By.LINK_TEXT, "First")
link_element.click()

# Below is for Professors

for j in range(len(professors)):
    if j == 0 or professors[j] != professors[j-1]:
        binarysearch(0,len(course_lines), (professors[j].sourceline+maxLinesinFile,professors[j].text,2,"N/A"))
        #print(professors[j].text, professors[j].sourceline)

#Repeat the above for as many pages as there are remaining
for i in range(2,numPages+1):
    link_element = driver.find_element(By.LINK_TEXT, str(i))
    link_element.click()

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    professors = soup.find_all("a", attrs={"href":"#!"}) # professor name
    for j in range(len(professors)):
        if j == 0 or professors[j] != professors[j-1]:
            binarysearch(0,len(course_lines), (professors[j].sourceline + i*maxLinesinFile,professors[j].text,2,"N/A"))
            #print(professors[j].text, professors[j].sourceline)

res = []
#print(course_lines)
curCourseNum = "0"
curCourseName = "None"
for i in course_lines:
    if i[2] == 0:
        curCourseName = str(i[1])
        curCourseNum = str(i[3])
    elif i[2] == 2:
        res.append("('" + curCourseName.strip() + "','" + curCourseNum + "',True," + i[1].strip() + "),")
    #print(i[0],i[1],i[2],i[3])
    #res += (i[3])

driver.quit()

