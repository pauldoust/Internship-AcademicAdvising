#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests 
from bs4 import BeautifulSoup
import pandas


# In[77]:


base_url = "https://cenacad.espol.edu.ec/index.php/module/Report/action/Materias/l/0/o/0/limit/15"
base_dynamic_url = "https://cenacad.espol.edu.ec/index.php/module/Report/action/Materias/l/0/o/"
base_domain = "https://cenacad.espol.edu.ec"
r = requests.get(base_url)
c = r.content


soup = BeautifulSoup(c,"html.parser")

paging = soup.find("table",{"class":"centrado", "cellspacing" : "0",  "cellpadding":"0", "style":"width:100%; text-align:center; "}).find("div").find_all("a")

web_pages = []
for page in paging:
    webLink = base_domain +page.attrs['href'] 
    web_pages.append(webLink)

print(len(web_pages))
web_content_list = []
all_pages = 3591
for page_index in range(0,240):
    page_filter = page_index * 15
    url = base_dynamic_url + str (page_filter) +   "/limit/15"
    print("Visiting: " + url)
    r = requests.get(url)
    c = r.content
    soup2 = BeautifulSoup(c,"html.parser")
    course_name = soup2.find_all("td",{"valign":"top","style":"width:47%;", "class" : "izquierda"})
    course_code = soup2.find_all("td",{"valign":"top","style":"width:15%;", "class" : "izquierda"})
    course_credits = soup2.find("td",{"valign":"top","style":"width:15%;", "class" : "izquierda"})
    index = 0
    for course in course_name:
        print(course.text + " " + course_code[index].text + " " + course_code[index].findNext('td').text + " " +course_code[index].findNext('td').findNext('td').text)
        web_content_dict = {}
        web_content_dict["Course_Name"] = course.text
        web_content_dict["Course_Code"] = course_code[index].text 
        web_content_dict["Course_Theoritical_Credits"] =  course_code[index].findNext('td').text
        web_content_dict["Course_Practical_Credits"] =  course_code[index].findNext('td').findNext('td').text
        web_content_list.append(web_content_dict)
        index = index+1
#     break

df = pandas.DataFrame(web_content_list)
df.to_csv(r'C:/Users/mpouldou/final-data/Statistics2-unified/COURSE_CREDITS.csv', index = None, header=True) 
print("END")

