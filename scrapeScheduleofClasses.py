from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

class soc:
    def __init__(self, dept, maxLines) -> None:
        self.numPages = None #Number of pages
        self.department = dept #Chosen department (NOTE for this website, any department with length of 3, such as CSE or DSC, contains a space at the end)
                            #So, if you want to scrape from the CSE department, you must intitialize the department variable as 'CSE ' not 'CSE'
        self.maxLinesinFile = maxLines # Find the file/page with the most lines and set this variable to that, double it for good measure
        self.res = None
        self.run()
    
    def getRes(self):
        return self.res

    def run(self):

        
        # Access the chrome driver
        service = Service(executable_path='C:/Drivers/chromedriver-win64/chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        # Go to the schedule of classes web page
        driver.get('https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm')

        # Find the element that corresponds to choosing the department and choose the selected department
        select_element = driver.find_element(By.ID, "selectedSubjects")
        select = Select(select_element)
        select.select_by_value(self.department)

        # Find the checkbox element that allows viewing of not only undergraduate classes but graduate classes as well
        select_checkbox1 = driver.find_element(By.ID, "schedOption31")
        select_checkbox1.click()

        # Find the checkbox element that allows vieiwing of special classes as well such as Teaching Assistant courses
        select_checkbox2 = driver.find_element(By.ID, "schedOption131")
        select_checkbox2.click()

        # Find the element that submits the form to gain access to all the courses that were chosen
        submit_button = driver.find_element(By.ID, "socFacSubmit")
        submit_button.click()

        # Set html var to the web page name as the submission of the form changed the page
        html = driver.page_source
        time.sleep(2)
        # Initialize Beautiful Soup to search the web page for scraping data
        soup = BeautifulSoup(html, "html.parser")
        courses = soup.find_all("span", attrs={"class":"boldtxt", "onclick": None}) # finds all course titles
        professors = soup.find_all("a", attrs={"href":"#!"}) # finds all professor names
        courseNumbers = soup.find_all("td", attrs={"class":"crsheader", "colspan": None}) #finds all course numbers
        self.numPages = 1
        # List to hold the scraped data in the correct order, this allows for correspondence between professor names and course names
        course_lines = []

        # Binary search algorithm to insert into courselines in the correct order
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


        # On the first page, scrapes all data on course names and course numbers
        skip = 0
        j = 0
        while j < (len(courses)):
            # This first if statement refers to a special case on the schedule of classses pages which needs to be accounted for or else the order will mess up
            if courseNumbers[(j*2)+1+(skip*2)].get('align') != None:
                skip += 1
                j -= 1
            # This is the typical route where the special case above does not occur
            elif j == 0 or courses[j].text != courses[j-1].text or courseNumbers[(j*2)+1+(skip*2)].text != courseNumbers[(j*2)+1+(skip*2)].text:
                course_lines.append((courses[j].sourceline+self.maxLinesinFile,courses[j].text, 0, courseNumbers[(j*2)+1+(skip*2)].text))
            j+=1
        #print('pages',self.numPages)
        #Repeat the above for as many pages as there are remaining
        for i in range(2,100):
            link_element = None
            try:
                link_element = driver.find_element(By.LINK_TEXT, str(i))
                self.numPages += 1
            except NoSuchElementException:
                break
            link_element.click()

            html = driver.page_source

            soup = BeautifulSoup(html, "html.parser")
            courses = soup.find_all("span", attrs={"class":"boldtxt", "onclick": None}) # course title
            courseNumbers = soup.find_all("td", attrs={"class":"crsheader", "colspan": None, "title": None}) # course number
            skip = 0
            j = 0
            while j < (len(courses)):
                if courseNumbers[(j*2)+1+(skip*2)].get('align') != None:
                    skip += 1
                    j -= 1
                elif j == 0 or courses[j].text != courses[j-1].text or courseNumbers[(j*2)+1+(skip*2)].text != courseNumbers[(j*2)+1+(skip*2)].text:
                    course_lines.append((courses[j].sourceline + i*self.maxLinesinFile,courses[j].text, 0, courseNumbers[(j*2)+1+(skip*2)].text))
                j+=1

        # Finds element that corresponds to the first page and goes to it so that we can now search for all professors
        if self.numPages > 1:
            link_element = driver.find_element(By.LINK_TEXT, "First")
            link_element.click()

        # Finds all professors on the first page

        for j in range(len(professors)):
            if j == 0 or professors[j].text != professors[j-1].text:
                binarysearch(0,len(course_lines), (professors[j].sourceline+self.maxLinesinFile,professors[j].text,2,"N/A"))

        #Repeat the above for as many pages as there are remaining
        for i in range(2,self.numPages+1):
            link_element = driver.find_element(By.LINK_TEXT, str(i))
            link_element.click()

            html = driver.page_source

            soup = BeautifulSoup(html, "html.parser")
            professors = soup.find_all("a", attrs={"href":"#!"}) # professor name
            for j in range(len(professors)):
                if j == 0 or professors[j].text != professors[j-1].text:
                    binarysearch(0,len(course_lines), (professors[j].sourceline + i*self.maxLinesinFile,professors[j].text,2,"N/A"))

        # This portion here is soley for formatting so that I could insert the data into my database for a different project
        # If you have no need for the formatting, you can simple get the data by printing out the course_lines list: print(course_lines)

        self.res = []
        #print(course_lines)
        curCourseNum = "0"
        curCourseName = "None"
        for i in course_lines:
            if i[2] == 0:
                curCourseName = str(i[1])
                curCourseNum = str(i[3])
            elif i[2] == 2:
                self.res.append("('" + curCourseName.strip().replace(",","").replace("'","") + "','" + curCourseNum + "',True," + i[1].strip() + "),")
            


        # stops the driver
        driver.quit()

if __name__ ==  "__main__":
    aSOC = soc('AIP ', 10000)
    print(aSOC.getRes())