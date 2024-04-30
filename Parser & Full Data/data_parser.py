import pandas as pd
from bs4 import BeautifulSoup
import os
import re


def find_all_html_files(root_folder):
    with open("data_errors.txt", "r", encoding='utf-8') as f:
        error_paths = [line.strip() for line in f]

    """Находит все HTML-файлы на 6 уровне"""
    html_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        # Проверяем, находимся ли мы на 6 уровне
        if len(dirpath.split(os.sep)) == 5:
            for filename in filenames:
                if "html" in filename:
                    if any(file.endswith('general_table.xlsx') for file in os.listdir(dirpath)): continue
                    path = os.path.join(dirpath, filename)
                    if path not in error_paths:
                        html_files.append(path)
    return html_files


def create_general_table_data(dir_name, soup, program_name, date_parsing, max_score):
    general_table = soup.find('table')

    general_table_headers = ['Направление', 'Дата'] + [th.text.strip() for th in general_table.find_all('th')] + ["Максимальный балл", "Проходной балл"]
    table_data = []

    for row in general_table.find_all('tr'):
        cells = row.find_all('td')
        if cells:
            row_data = [program_name, date_parsing] + [cell.text.strip() for cell in cells] + [max_score, 0]
            table_data.append(row_data)

    general_table_df = pd.DataFrame(table_data, columns=general_table_headers)
    general_table_path = dir_name + "/general_table.xlsx"
    general_table_df.to_excel(general_table_path, index=False)
    print("Создана таблица общей информации по адресу:", general_table_path)


def create_student_table_data(dir_name, soup, encode):
    student_table = soup.find_all('table')[-1]

    student_table_headers = [th.text.strip() for th in student_table.find('thead').find_all('th')]
    table_data = []

    for row in student_table.find_all('tr'):
        cells = row.find_all('td')
        if cells:
            row_data = []
            for cell in cells:
                script_tag = cell.find('script')
                if script_tag:
                    number = int(re.search(r'\d+', script_tag.string).group())
                    row_data.append(encode(number))
                else:
                    row_data.append(cell.text.strip())
            table_data.append(row_data)

    student_table_df = pd.DataFrame(table_data, columns=student_table_headers)

    if '∑' in student_table_df.columns:
        student_table_df = student_table_df.rename(columns={'∑': 'Сумма'})

    student_table_path = dir_name + "/student_table.xlsx"
    student_table_df.to_excel(student_table_path, index=False)
    print("Создана таблица студентов по адресу:", student_table_path)

    try:
        max_score = student_table_df['Сумма'].astype(int).max()
    except Exception as e:
        max_score = 6666
        with open("data_errors.txt", "a", encoding="UTF-8") as error_file:
            error_file.write(f"{dir_name}\n Ошибка Суммы 6666 {e}\n\n")

    return max_score


def parse_data_by_file(file_path):
    dir_name = os.path.dirname(file_path)
    year = re.search(r"(\d{4})", file_path).group(1)
    date_parsing = re.search(r"(\d{8})", file_path).group(1)
    program_name = os.path.basename(dir_name)

    if year == "2018":
        encode = lambda x: x ^ 27
    else:
        encode = lambda x: (x ^ 37) % 837

    with open(file_path, 'r', encoding="UTF-8") as file:
        html_content = file.read()

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        max_score = create_student_table_data(dir_name, soup, encode)
        create_general_table_data(dir_name, soup, program_name, date_parsing, max_score)
    except Exception as e:
        print("Ошибка", e)
        with open("data_errors.txt", "a", encoding="UTF-8") as error_file:
            error_file.write(f"{file_path}\n {e}\n\n")

import time

while True:
    root_folder = "all_years"
    html_file_paths = find_all_html_files(root_folder)
    counter = 0
    max_counter = len(html_file_paths)

    for file_path in html_file_paths:
        print()
        print(counter := counter + 1, "/", max_counter, "   ", file_path)
        parse_data_by_file(file_path)

    for i in range(5):
        print()
        print(f"Остановка, {5 - i}")
        time.sleep(60)
