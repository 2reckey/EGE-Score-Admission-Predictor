import os
import requests
import time
from datetime import datetime

def create_year_folder(base_folder, year):
    """Создает папку для сохранения файлов за определенный год"""
    year_dir = os.path.join(base_folder, str(year))
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)
    return year_dir

def get_html_file_name(redirect_url, year):
    """Формирует имя файла для сохранения HTML-кода страницы"""
    date_str = redirect_url.split('/')[4]
    date_obj = datetime.strptime(date_str, '%Y%m%d%f')
    return f"{date_obj.strftime('%Y%m%d')}_admlist.html"

def save_html_file(file_path, html_content):
    """Сохраняет HTML-код страницы в файл"""
    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(html_content)
    print(f"HTML-код страницы сохранён в файл {file_path.split('/')[-1]}")

def parse_html_page(base_url, year):
    """Парсит HTML-страницу за определенный год"""
    url = f"{base_url}{year}0830000000/http://www.admlist.ru/"
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        redirect_url = response.url
        file_name = get_html_file_name(redirect_url, year)
        return response.text, file_name
    else:
        print(f"Ошибка при запросе страницы за {year} год: статус-код {response.status_code}")
        return None, None



years = [2017, 2018, 2019, 2020, 2021, 2022]
base_url = "https://web.archive.org/web/"
base_folder = "all_years"
delay = 2

if not os.path.exists(base_folder):
    os.makedirs(base_folder)

for year in years:
    year_folder = create_year_folder(base_folder, year)
    html_content, file_name = parse_html_page(base_url, year)
    if html_content and file_name:
        file_path = os.path.join(year_folder, file_name)
        save_html_file(file_path, html_content)
    time.sleep(delay)