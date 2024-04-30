import requests
from bs4 import BeautifulSoup
import re

URL = 'https://web.archive.org/web/20180828001700/http://tabiturient.ru/vuzu/mgimo/proxodnoi/'

response = requests.get(URL)
response.encoding = 'utf-8'
html_content = response.text

# with open("test.html", 'r', encoding='utf-8') as file:
#     html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

spectr_elements = soup.find_all('tr', class_='spectr')

with open('test.txt', 'w', encoding="utf-8") as file:
    for spectr_element in spectr_elements:
        direction = spectr_element.find('b', style='text-transform: uppercase;').string.strip()
        additional_info = spectr_element.find('br').next_sibling.strip()
        passing_score = spectr_element.find(string='Проходной балл на очное: ').find_next('span').string.strip()
        if passing_score.isdigit():
            file.write(f'Направление: {direction}\n')
            file.write(f'Дополнительная информация: {additional_info}\n')
            file.write(f'Проходной балл: {passing_score}\n')
            file.write('---\n')

print("Done")