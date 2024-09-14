from bs4 import BeautifulSoup
import requests

class cc:
    def __init__(self, url_S, deptNum, deptNameLength) -> None:
        self.url = url_S #the url of the catalog for the respective department
        self.departmentNum = deptNum # department id that you want set
        self.departmentNameLength = deptNameLength # example: MATH department has length of 4, CSE department has length of 3
        self.res2 = None
        self.run()

    def getRes(self):
        return self.res2

    def run(self):
        # Gets a hold of the given page with the url
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        # Finds all elements with these parameters which represent the courses in the course catalog
        courses = soup.find_all("p", attrs={"class":"course-name"})

        # This list is where we store all the data
        self.res2 = []
        # Below is solely for formatting so that I could easily insert the scraped data into my database for another project
        # If you have no interest in this format and only care for the data, simply iterate through the courses variable from above to get the data
        for i in courses:
            #print(i)
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
            index4 = 0
            self.res2.append("('" + courseName.replace(",","").replace("'","") + "','" + courseNum + "',False,null," + str(self.departmentNum) + "),")

if __name__ == "__main__":
    aCC = cc("https://catalog.ucsd.edu/courses/JWSP.html", 1, 4)
    print(aCC.getRes())

