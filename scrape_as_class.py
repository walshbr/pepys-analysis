import lxml
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import secret
import json

# start
# >>> python 3
# >>> import scrape_as_class

# reload
# >>> import importlib
# >>> importlib.reload(scrape_as_class)
# >>> diary = scrape_as_class.Diary()

class Diary(object):
    # rather than enter the data bit by bit, we create a constructor that takes in the data at one time and spins it into the format we want
    # all the attributes we want the class to have follow the __init__ syntax
    def __init__(self):
        # all the attributes we want the class to have
        # classes may contain functions we define ourselves, like the setup_driver function
        self.driver = self.setup_driver()
        self.num_entries = 5
        # if there is no sp_diary.json, start at one
        self.entries = [DiaryEntry(self.driver)]
        # if there is an sp_diary.json, look at it and find out the last you were on
        # self.adjust_driver_to_last_entry()
        
        # remaining_entries = True if self.driver.current_url != "https://www.pepysdiary.com/diary/1660/01/09/" else False

        # while remaining_entries:
        #     time.sleep(1)
        #     self.entries.append(DiaryEntry(self.driver))
        #     next_entry = self.driver.find_element(By.CSS_SELECTOR, 'li.nextprev-next')
        #     next_entry.click()
        #     # if self.driver.current_url != "https://www.pepysdiary.com/diary/1660/01/09/":
        #     #     next_entry.click()
        #     # else:
        #     #     break
        
        
        while self.driver.current_url != "https://www.pepysdiary.com/diary/1669/05/31/":
        # for entry in range(self.num_entries)[0:]:
            print(self.driver.current_url)
            time.sleep(1)
            self.entries.append(DiaryEntry(self.driver))
            next_entry = self.driver.find_element(By.CSS_SELECTOR, 'li.nextprev-next')
            next_entry.click()
        else:
            print(self.driver.current_url)
            time.sleep(1)
            self.entries.append(DiaryEntry(self.driver))
            self.driver.quit()
        self.output_to_json()

    def output_to_json(self):

        # create dictionary
        diary_dict = []
        for i in self.entries:
            this_dict = {}
            this_dict['url'] = i.url
            this_dict['year'] = i.year
            this_dict['month'] = i.month
            this_dict['date'] =  i.date
            this_dict['entry_date'] = i.entry_date
            this_dict['entry_text'] = i.entry_text
            this_dict['endnotes'] = i.endnotes
            this_dict['footnotes'] = i.footnotes
            this_dict['annotations'] = i.annotations
            diary_dict.append(this_dict)

        
        with open('sp_diary.json', 'w') as outfile:
            json.dump(diary_dict, outfile)


    def setup_driver(self):
        """Sets up the crhome driver and returns it for later use"""
        MY_PATH = secret.path()
        service = Service(executable_path=MY_PATH)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://www.pepysdiary.com/diary/1660/01/01/')
        return driver

# the Text class works the same as the Corpus, but will contain text-level only attributes
class DiaryEntry(object):
    # now create the blueprint for our text object
    def __init__(self,parent_driver):
        self.driver = parent_driver
        # grab the current url
        self.url = parent_driver.current_url
        # grab the year
        self.year = parent_driver.current_url.split('/')[4]
        # grab month
        self.month = parent_driver.current_url.split('/')[5]
        # a grab date
        self.date = parent_driver.current_url.split('/')[6]
        # grab full entry date
        self.soup = BeautifulSoup(parent_driver.page_source, 'lxml')
        self.raw_date = self.soup.find('div', class_='manuscript').h1.text
        self.entry_date = self.raw_date.replace("\n", "").replace("\t", "")
        # grab text
        self.entry_text = self.get_text()
        self.endnotes = self.get_endnotes()
        self.footnotes = self.get_footnotes()
        self.annotations = self.get_annotations()

    def get_text(self):
        entry_text = []
        
        try:
            self.driver.find_element(By.CSS_SELECTOR, '.footnotes')
            stop_at = self.soup.find('aside', class_='footnotes')
            for i in stop_at.find_all_previous('p'):
                entry_text.insert(0,i.text)
        except NoSuchElementException:
            for i in self.soup.find('div', class_='manuscript').find_all('p'):
                entry_text.append(i.text)

        extra = 'Daily entries from the 17th century London diary'
        if extra in entry_text: entry_text.remove(extra)
        
        return entry_text
        
    def get_endnotes(self):
        endnotes = []

        try:
            for i in self.soup.find('aside', class_='footnotes').find_all('p'):
                endnotes.append(i.text)
        except:
            pass
        else: print('end')

        return endnotes
    
    def get_footnotes(self):
        footnotes = []
        try:
            for i in self.soup.find('aside', class_='footnotes').ol.find_all('li'):
                footnotes.append(i.text)
        except:
            pass
        else: 
            print('foot')
            
        return footnotes

    def get_annotations(self):
        annotations = []
        # try:
        #     for i in self.soup.find('section', id='annotations').find_all('div', class_='media-body'):
        #         annotations.append(i.text)
        # except:
        #     pass
        # else: 
        #     annotations.append('na')
        try:
            for i in self.soup.find('section', id='annotations').find_all('div', class_='media-body'):
                # annotation = []
                datetime = []
                username = []
                usercomment = []

                sep0 = '\non'
                annot = i.text
                user = annot.split(sep0, 1)[0]
                user_fixed = user.replace("\n", "").replace("\t", "")
                username.append(user_fixed)

                sep1 = 'Link\n\n\n\n'
                comm = annot.split(sep1, 1)[1]
                comm_fixed = comm.replace("\n", " ")
                usercomment.append(comm_fixed)

                for post in i.find_all('time'):
                    datetime.append(post['datetime'])
                    
                # annotation.append(datetime)
                # annotation.append(username)
                # annotation.append(usercomment)
                # annotations.append(annotation)

                annotation = [
                    {'datetime': datet, 'username': usern, 'usercomment': userc}
                    for datet, usern, userc in zip(datetime, username, usercomment)
                ]
                annotations.append(annotation)
        except:
            pass
        else: 
            print('annot')
        
        return annotations
       
# this is what runs if you run the file as a one-off event - $ python3 scrape-as-class.py
def main():
    diary = Diary()

# this allows you to import the classes as a module. it uses the special built-in variable __name__ set to the value "__main__" if the module is being run as the main program
if __name__ == "__main__":
    main()


# diary = []
# first_entry = []

# years = []
# months = []
# dates = []
# entry_dates = []
# entry_texts = []
# endnotes_all = []
# footnotes_all = []
# annotations_all = []

# year = driver.current_url.split('/')[4]
# first_entry.append(year)
# month = driver.current_url.split('/')[5]
# first_entry.append(month)
# date = driver.current_url.split('/')[6]
# first_entry.append(date)
    
# soup = BeautifulSoup(driver.page_source, 'lxml')

# entry_date = soup.find('div', class_='manuscript').h1.text
# first_entry.append(entry_date)

# entry_text = []
# stop_at = soup.find('aside', class_='footnotes')
# for i in stop_at.find_all_previous('p'):
#     entry_text.insert(0,i.text)
# entry_text.remove('Daily entries from the 17th century London diary')
# first_entry.append(entry_text)

# endnotes = []
# footnotes = []
# for i in soup.find('aside', class_='footnotes').find_all('p'):
#     endnotes.append(i.text)
# for i in soup.find('aside', class_='footnotes').ol.find_all('li'):
#     footnotes.append(i.text)

# first_entry.append(endnotes)
# first_entry.append(footnotes)

# annotations = []

# for i in soup.find('section', id='annotations').find_all('div', class_='media-body'):
#     annotations.append(i.text)

# first_entry.append(annotations)

# diary.append(first_entry)

# next_entry = driver.find_element('xpath','//*[@id="content"]/main/div[1]/div[1]/nav/ul/li')
# next_entry.click()

# #we will use a while loop to grab data about the first three players
# count = 0

# entries = ['1', '2', '3', '4', '5']

# for i in entries:
#     count += 1
#     time.sleep(1)
    
#     diary_entry = []
    
#     year = driver.current_url.split('/')[4]
#     diary_entry.append(year)
#     month = driver.current_url.split('/')[5]
#     diary_entry.append(month)
#     date = driver.current_url.split('/')[6]
#     diary_entry.append(date)
    
#     soup = BeautifulSoup(driver.page_source, 'lxml')

#     entry_date = soup.find('div', class_='manuscript').h1.text
#     diary_entry.append(entry_date)

#     entry_text = []
    
#     try:
#         stop_at = soup.find('aside', class_='footnotes')
#         for i in stop_at.find_all_previous('p'):
#             entry_text.insert(0,i.text)
#     except:
#         pass
#     else:
#         for i in soup.find('div', class_='manuscript').find_all('p'):
#             entry_text.append(i.text)
    
#     extra = 'Daily entries from the 17th century London diary'
#     if extra in entry_text: entry_text.remove(extra)
    
#     diary_entry.append(entry_text)

#     endnotes = []
#     footnotes = []
    
#     try:
#         for i in soup.find('aside', class_='footnotes').find_all('p'):
#             endnotes.append(i.text)
#     except:
#         pass
#     else: endnotes.append('na')
        
#     try:
#         for i in soup.find('aside', class_='footnotes').ol.find_all('li'):
#             footnotes.append(i.text)
#     except:
#         pass
#     else: footnotes.append('na')
        
#     diary_entry.append(endnotes)
#     diary_entry.append(footnotes)
    
#     annotations = []

#     try:
#         for i in soup.find('section', id='annotations').find_all('div', class_='media-body'):
#             annotations.append(i.text)
#     except:
#         pass
#     else: annotations.append('na')
    
#     diary_entry.append(annotations)
    
#     diary.append(diary_entry)

#     next_entry = driver.find_element('xpath', '//*[@id="content"]/main/div[1]/div[1]/nav/ul/li[2]')
#     next_entry.click()

# driver.quit()
# print(diary[0])

# labels = ['year', 'month', 'date', 'entry_date', 'entry_text', 'endnotes', 'footnotes', 'annotations']


# # create dictionary
# diary_dict = [dict(zip(labels, i)) for i in diary[0:]]

# import json
# with open('sp_diary.json', 'w') as outfile:
#     json.dump(diary_dict, outfile)