import requests
from bs4 import BeautifulSoup
import re

URL = 'https://web.archive.org/web/20200920074847/https://tabiturient.ru/vuzu/stankin/proxodnoi/'

response = requests.get(URL)
response.encoding = 'utf-8'
html_content = response.text

# with open("test.html", 'r', encoding='utf-8') as file:
#     html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

headnap_elements = soup.find_all('div', class_='headnap')

with open('test.txt', 'w', encoding="utf-8") as file:
    for headnap_element in headnap_elements:
        direction = headnap_element.find('span', class_='font3').string.strip()
        dir_base_element = headnap_element.find('span', class_='font2')
        dir_base = dir_base_element.string.strip()
        faculty_info = dir_base_element.find_next('span', class_='font2').text.strip()
        profile_info = dir_base_element.find_next('span', class_='font2').find_next('span', class_='font2').text.strip()
        passing_score = headnap_element.find(class_='circ2 circ2unique').find(class_='font11').string.strip()
        if passing_score.isdigit() or passing_score == "БВИ":
            file.write(f'Направление: {direction}\n')
            file.write(dir_base+"\n")
            file.write(faculty_info+"\n")
            file.write(profile_info+"\n")
            file.write(f'Проходной балл: {passing_score}\n')
            file.write('---\n')

print("Done")