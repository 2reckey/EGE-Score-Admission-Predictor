import os
from difflib import get_close_matches
import pandas as pd


def add_all_pass_scores(root_folder):
    pass_scores_dict = {}
    for dirpath, _, filenames in os.walk(root_folder):
        if len(dirpath.split(os.sep)) == 3:
            pass_scores_path = dirpath
            pass_scores_dict = read_pass_scores_from_file(pass_scores_path)
            print("\n"+pass_scores_path+"\n")

        if len(dirpath.split(os.sep)) == 5:
            for filename in filenames:
                if filename.endswith("general_table.xlsx"):
                    relative_path = os.path.relpath(dirpath, pass_scores_path)
                    pass_score = get_pass_score(relative_path, pass_scores_dict)

                    if not pass_score: continue

                    general_table_path = os.path.join(dirpath, filename)
                    general_df = pd.read_excel(general_table_path)

                    if pd.isna(general_df['Проходной балл'].iloc[0]):
                        general_df.at[0, 'Проходной балл'] = pass_score
                        general_df.to_excel(general_table_path, index=False)
                        print(f"{general_table_path}\n------------")


def get_pass_score(relative_path, pass_scores_dict):
    try:
        return pass_scores_dict[relative_path]
    except KeyError:
        closest_key = find_closest_key(pass_scores_dict, relative_path)
        if closest_key:
            return pass_scores_dict[closest_key]
        else:
            return None


def find_closest_key(dictionary, key):
    closest_keys = get_close_matches(key, dictionary.keys())
    if closest_keys:
        return closest_keys[0]
    else:
        # print(f"Ключ {key} не найден")
        print(key)
        return None


def read_pass_scores_from_file(pass_scores_dir, filename="points.txt"):
    path = os.path.join(pass_scores_dir, filename)
    pass_scores = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split(" = ")
            try:
                pass_scores[key] = int(value)
            except ValueError:
                print(f"Ошибка в {key} = {value}")
                raise Exception
    return pass_scores


# Пример использования
root_folder = "all_years" + os.sep + "2019"
add_all_pass_scores(root_folder)
