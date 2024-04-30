import os
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import shutil

def find_html_file(html_folder):
    """Находит HTML-файл в папке"""
    html_files = os.listdir(html_folder)
    for fl in html_files:
        if "html" in fl:
            return os.path.join(html_folder, fl)
    return ""

def get_university_info(row):
    """Получает информацию о вузе из строки таблицы"""
    link = row.find("a")
    if link:
        university_name = link.text.strip()
        relative_path = link["href"]
        university_file_name = relative_path.split("/")[0].upper()
        return university_name, relative_path, university_file_name
    return "", "", ""

def create_university_folder(html_folder, university_name):
    """Создает папку для вуза, если она не существует"""
    university_folder = os.path.join(html_folder, university_name)
    if not os.path.exists(university_folder):
        os.makedirs(university_folder)
    return university_folder

def get_university_url(year, relative_path):
    """Формирует URL для страницы вуза"""
    return "https://web.archive.org/web/" + str(year) + f"0830000000/http://www.admlist.ru/{relative_path}"

def save_university_page(html_file_path, response):
    """Сохраняет HTML-код страницы вуза в файл"""
    with open(html_file_path, "w", encoding="UTF-8") as html_file:
        html_file.write(response.text)
    print(f"Создан HTML-файл для вуза: {html_file_path.split(os.sep)[-2:]}")

def parse_university_info(row, year, html_folder, delay):
    """Парсит информацию о вузе из строки таблицы"""
    university_name, relative_path, university_file_name = get_university_info(row)
    if university_name:
        university_folder = create_university_folder(html_folder, university_name)
        university_url = get_university_url(year, relative_path)
        response = requests.get(university_url)
        response.encoding = 'utf-8'

        redirect_url = response.url
        date_str = redirect_url.split('/')[4]
        date_obj = datetime.strptime(date_str, '%Y%m%d%f')
        file_name = f"{date_obj.strftime('%Y%m%d')}_{university_file_name}.html"
        html_file_path = os.path.join(university_folder, file_name)

        if date_obj.year == year and date_str != str(year)+"0830000000":
            save_university_page(html_file_path, response)
        else:
            shutil.rmtree(university_folder)
            print(f"{university_name} не добавлен, так как дата {date_str}.")

        time.sleep(delay)



year = 2017
start_parsing_name = "ВШЭ"
end_parsing_name = "ВШЭ-НН"

html_folder = "all_years/"+str(year)
html_file_path = find_html_file(html_folder)

with open(html_file_path, "r", encoding="UTF-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")
rows = soup.find_all("tr")

is_parsing = False
delay = 10

for row in rows:
    university_name = row.find("a").text.strip() if row.find("a") else ""
    if university_name == start_parsing_name:
        is_parsing = True
    elif university_name == end_parsing_name:
        is_parsing = False

    if is_parsing:
        parse_university_info(row, year, html_folder, delay)