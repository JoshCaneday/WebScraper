from bs4 import BeautifulSoup
import requests


url = "https://catalog.ucsd.edu/courses/CSE.html" #the url of the catalog for the respective department
departmentNum = 39 # department id that you want set
departmentNameLength = 3 # example: MATH department has length of 4, CSE department has length of 3


page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

courses = soup.find_all("p", attrs={"class":"course-name"})

res2 = []

for i in courses:
    temp = i.text
    index = 0
    while temp[index] != ".":
        index += 1
    index3 = 0
    while temp[index3] != " ":
        index3 += 1
    courseNum = temp[index3+1:index]
    #print(courseNum)
    index2 = index+2
    while temp[index2] != "(":
        index2 += 1
    courseName = temp[index+2:index2-1]
    res2.append("('" + courseName + "','" + courseNum + "',False,null," + str(departmentNum) + "),")
