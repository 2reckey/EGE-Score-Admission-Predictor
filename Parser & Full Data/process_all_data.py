import os
import shutil
import pandas as pd

def process_all_student_files(root_folder):
    excel_files = []
    dump_data = []
    for dirpath, _, filenames in os.walk(root_folder):
        # Проверяем, находимся ли мы на 6 уровне
        if len(dirpath.split(os.sep)) == 5:
            for filename in filenames:
                if filename.endswith("student_table.xlsx"):
                    path = os.path.join(dirpath, filename)
                    delete_count = process_student_table(path, excel_files)
                    dump_data.append((path, delete_count))
    return excel_files, dump_data

def process_student_table(file_path, exel_files):
    print(file_path)
    general_table_path = os.path.join(os.path.dirname(file_path), "general_table.xlsx")
    general_df = pd.read_excel(general_table_path)
    if "Количество Предметов" in general_df.columns:
        return 0

    student_df = pd.read_excel(file_path)
    q_80 = student_df[student_df["Сумма"] != 0]["Сумма"].quantile(0.8)
    print(f"80% квантиль от суммы: {q_80}")

    if q_80 > 400:
        num_subjects = 5
    elif q_80 > 300:
        num_subjects = 4
    else:
        num_subjects = 3

    size = student_df.shape[0]
    max_score = 100 * num_subjects + 10
    student_df = student_df[student_df["Сумма"] <= max_score]
    delete_count = size - student_df.shape[0]

    student_df["Средний балл"] = student_df["Сумма"] / num_subjects

    general_df.rename(columns={"Максимальный балл": "Количество Предметов"}, inplace=True)
    general_df["Количество Предметов"] = num_subjects

    if delete_count > 0:
        print(f"Удалено {delete_count} строк")
        print("----------------- \n\n")
        exel_files.append(file_path)
        student_df.to_excel(os.path.join(os.path.dirname(file_path), "student_dump_table.xlsx"), index=False)
        general_df.to_excel(os.path.join(os.path.dirname(file_path), "general_dump_table.xlsx"), index=False)
    else:
        student_df.to_excel(file_path, index=False)
        general_df.to_excel(general_table_path, index=False)

    return delete_count

root = "all_years"
exel_files, dump_data = process_all_student_files(root)
print(exel_files)
print(len(exel_files))

# Сохраняем данные о выбросах в файл "dump_data.xlsx"
dump_df = pd.DataFrame(dump_data, columns=["File Path", "Deleted Rows"])
dump_df.to_excel("dump_data.xlsx", index=False)