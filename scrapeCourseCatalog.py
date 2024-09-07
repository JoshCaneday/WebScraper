from bs4 import BeautifulSoup
import requests


url = "https://catalog.ucsd.edu/courses/MATH.html"
departmentNum = 124


page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

courses = soup.find_all("p", attrs={"class":"course-name"})

for i in courses:
    temp = i.text
    index = 1
    while temp[index] != ".":
        index += 1
    courseNum = temp[0:index]
    index2 = index+2
    while temp[index2] != "(":
        index2 += 1
    courseName = temp[index+2:index2-1]
    print("('" + courseName + "','" + courseNum + "',False,null," + str(departmentNum) + "),")
