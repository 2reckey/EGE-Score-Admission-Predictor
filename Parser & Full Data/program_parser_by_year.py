import os
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import shutil
import re


def sanitize_filename(filename):
    # Список запрещенных символов в Windows
    invalid_chars = r'<>:"/\|?*'
    # Заменяем запрещенные символы на подчеркивание
    sanitized = re.sub(f'[{re.escape(invalid_chars)}]', ' ', filename)
    return sanitized


def find_all_html_files(root_folder):
    """Находит все HTML-файлы на 3 уровне"""
    html_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        # Проверяем, находимся ли мы на 3 уровне
        if len(dirpath.split(os.sep)) == 3:
            for filename in filenames:
                if "html" in filename:
                    html_files.append(os.path.join(dirpath, filename))
    return html_files


def find_faculty(row):
    faculty_link = row.find("b")
    if faculty_link:
        return faculty_link.text.strip()
    return ""


def find_program(row):
    program_link = row.find("a")
    if program_link:
        program_name = program_link.text.strip()
        relative_path = program_link["href"]
        kcp_value = row.find("td", align="center").get_text().strip()
        return program_name, relative_path, kcp_value
    else:
        return "", "", ""


def create_faculty_and_program_folders(html_folder, faculty_name, program_name):
    """Создает папки для факультета и направления, если они не существуют"""
    faculty_folder = os.path.join(html_folder, faculty_name)
    if not os.path.exists(faculty_folder):
        os.makedirs(faculty_folder)
    program_folder = os.path.join(faculty_folder, program_name)
    if not os.path.exists(program_folder):
        os.makedirs(program_folder)
    return program_folder


def get_program_url(year, relative_path):
    """Формирует URL для страницы направления"""
    return f"https://web.archive.org/web/{year}0830000000/http://www.admlist.ru/{relative_path}"


def save_program_page(html_file_path, response):
    """Сохраняет HTML-код страницы направления в файл"""
    with open(html_file_path, "w", encoding="UTF-8") as html_file:
        html_file.write(response.text)
    print(f"Создан HTML-файл для направления: {html_file_path.split(os.sep)[-4:]}")


def try_except_request(url):
    try:
        response = requests.get(url)
        return response
    except Exception as e:
        print("Ошибка при выдачи запроса")
        t = 84
        for i in range(t):
            time.sleep(1)
            print(f"{(i + 1) / t:.2f}", end=" ")
            if (i + 1) % 42 == 0: print()
        print()
        return try_except_request(url)


def parse_faculty_and_program_info(html_file_path, year, delay):
    """Парсит информацию о факультете и направлении из HTML-файла"""
    with open(html_file_path, "r", encoding="UTF-8") as file:
        html_content = file.read()
        additional_url = html_file_path.split(os.sep)[-1].split(".")[0].split("_")[-1].lower() + "/"

    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all("tr")
    faculty_name = "AllFaculty"

    for row in rows:
        if find_faculty(row): faculty_name = find_faculty(row)
        program_name, relative_path, kcp_value = find_program(row)

        if program_name and kcp_value != '0':
            process_program_info(html_file_path, year, faculty_name, program_name, relative_path, additional_url)


def process_program_info(html_file_path, year, faculty_name, program_name, relative_path, additional_url):
    """Обрабатывает информацию о программе"""
    program_name = sanitize_filename(program_name)
    faculty_name = sanitize_filename(faculty_name)
    if faculty_name == "-":
        program_name = program_name[3:]
    elif faculty_name in program_name:
        program_name = " ".join(program_name.split(faculty_name)[1:])[2:].rstrip()

    html_folder = os.path.dirname(html_file_path)
    program_folder = create_faculty_and_program_folders(html_folder, faculty_name, program_name)

    if any(file.endswith('.html') for file in os.listdir(program_folder)):
        return

    program_url = get_program_url(year, additional_url + relative_path)
    response = try_except_request(program_url)
    response.encoding = 'utf-8'

    redirect_url = response.url
    date_str = redirect_url.split('/')[4]
    date_obj = datetime.strptime(date_str, '%Y%m%d%f')
    file_name = f"{date_obj.strftime('%Y%m%d')}_index.html"
    new_html_file_path = os.path.join(program_folder, file_name)

    if date_obj.year == year and date_str != f"{year}0830000000":
        save_program_page(new_html_file_path, response)
    else:
        shutil.rmtree(program_folder)
        print(f"{program_name} не добавлен, так как дата {date_str}.")

    time.sleep(delay)


delay = 3

for year in range(2017, 2023):
    root_folder = "all_years"
    html_file_paths = find_all_html_files(os.path.join(root_folder, str(year)))

    counter = 0
    max_counter = len(html_file_paths)

    for html_file_path in html_file_paths:
        print()
        print(counter := counter + 1, "/", max_counter, "   ", html_file_path.split(os.sep)[-1])
        try:
            parse_faculty_and_program_info(html_file_path, year, delay)
        except Exception as e:
            print("---------------------------------------")
            print(f"Ошибка при обработке файла {html_file_path}")
            print(e)
            with open("errors.txt", "a", encoding="UTF-8") as error_file:
                error_file.write(f"{html_file_path}\n {e}\n\n")
            continue
