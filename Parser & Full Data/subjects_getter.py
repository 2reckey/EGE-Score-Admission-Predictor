import pandas as pd
import os

def process_all_student_files(root_folder, subjects):
    all_data_frames = []
    err_list = []
    all_cnt = 0
    name_set = set()
    for dirpath, _, filenames in os.walk(root_folder):
        # Проверяем, находимся ли мы на 6 уровне
        if len(dirpath.split(os.sep)) == 5:
            for filename in filenames:
                if filename.endswith("student_table.xlsx"):
                    path = os.path.join(dirpath, filename)

                    df = pd.read_excel(path)

                    student_name = df.columns[3]
                    subject_columns = {}

                    for subject in subjects:
                        subject_name = next((column for column in df.columns if
                                             column.upper().startswith(subject) and "ДВИ" not in column.upper()), "")
                        if subject_name:
                            subject_columns[subject] = subject_name

                    if all(name in subject_columns for name in subjects):
                        if any(df[subject_columns[name]].max() > 100 for name in subjects):
                            err_list.append(path)
                            print("error \n\n\n")
                        name_set.update(subject_columns.values())

                        df = df.rename(columns={student_name: "Name", **{subject_columns[name]: name for name in subjects}})
                        df["All SUM"] = sum(df[name] for name in subjects)
                        all_data_frames.append(df[["Name"] + subjects + ["All SUM"]])
                        all_cnt += df[subjects[0]].size
                        print(all_cnt, name_set, path, sep='\n')

    all_data = pd.concat(all_data_frames, ignore_index=True)
    all_data.to_excel("subjects.xlsx", index=False)

    print("------------")
    for path in err_list:
        print(path)


root = "all_years"+os.sep+"2018"
subjects = ["ИНФ", "М", "Р"]
process_all_student_files(root, subjects)
