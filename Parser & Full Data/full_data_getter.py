import pandas as pd
import os

def process_all_student_files(root_folder):
    all_data_frames = []
    err_list = []
    all_cnt = 0
    for dirpath, _, filenames in os.walk(root_folder):
        # Проверяем, находимся ли мы на 6 уровне
        if len(dirpath.split(os.sep)) == 5:
            for filename in filenames:
                if filename.endswith("student_table.xlsx"):
                    student_path = os.path.join(dirpath, filename)
                    general_path = os.path.join(dirpath, "general_table.xlsx")

                    general_df = pd.read_excel(general_path)
                    general_df.rename(columns={'Согласий': 'Аттестатов'}, inplace=True)

                    student_df = pd.read_excel(student_path)
                    student_df.rename(columns={'Тип поступления': 'Тип', 'СНИЛС': 'ФИО'}, inplace=True)
                    student_df = student_df[(student_df['Тип'].str.contains("ОК")) & (student_df['Сумма'] > 100)]

                    pass_score = general_df['Проходной балл'][0]
                    quota = general_df['КЦП'][0]

                    df = pd.DataFrame({
                        "Year": general_df['Год'][0],
                        "University": general_df['ВУЗ'][0],
                        "Faculty": general_df['Факультет'][0],
                        "Program": general_df['Направление'][0],
                        "Name": student_df["ФИО"],
                        "Score": student_df["Сумма"],
                        "Avg_score": student_df["Средний балл"],
                        "Num_subjects": general_df['Количество Предметов'][0],
                        "Quota": general_df['КЦП'][0],
                        "All_app": general_df['Заявлений'][0],
                        "Orig_app": general_df['Аттестатов'][0],
                        "BVI": general_df['БВИ'].astype(str)[0].split("/")[-1]
                    })

                    df = df.sort_values(by="Score", ascending=False)
                    df['q90'] = df['Avg_score'].quantile(0.9)
                    df['q80'] = df['Avg_score'].quantile(0.8)
                    df['q75'] = df['Avg_score'].quantile(0.75)
                    df['q70'] = df['Avg_score'].quantile(0.7)
                    df['q65'] = df['Avg_score'].quantile(0.65)
                    df['q60'] = df['Avg_score'].quantile(0.6)
                    df['q55'] = df['Avg_score'].quantile(0.55)
                    df['q50'] = df['Avg_score'].quantile(0.5)
                    df['q40'] = df['Avg_score'].quantile(0.4)
                    df['q30'] = df['Avg_score'].quantile(0.3)
                    df['q20'] = df['Avg_score'].quantile(0.2)
                    df['q10'] = df['Avg_score'].quantile(0.1)

                    df['q25_by_1Q'] = df['Avg_score'][:quota].quantile(0.25)

                    df['q25_by_2Q'] = df['Avg_score'][:2*quota].quantile(0.25)

                    df['q25_by_3Q'] = df['Avg_score'][:3*quota].quantile(0.25)

                    df['q25_by_4Q'] = df['Avg_score'][:4*quota].quantile(0.25)

                    df['q25_by_5Q'] = df['Avg_score'][:5*quota].quantile(0.25)

                    df['q25_by_6Q'] = df['Avg_score'][:6*quota].quantile(0.25)

                    df['q25_by_7Q'] = df['Avg_score'][:7*quota].quantile(0.25)

                    df['q25_by_8Q'] = df['Avg_score'][:8*quota].quantile(0.25)

                    df['q25_by_9Q'] = df['Avg_score'][:9*quota].quantile(0.25)

                    df['q25_by_10Q'] = df['Avg_score'][:10*quota].quantile(0.25)

                    df['Is_pass'] = df['Score'] >= pass_score

                    all_cnt += df.shape[0]

                    print(dirpath, all_cnt)

                    all_data_frames.append(df)

    all_data = pd.concat(all_data_frames, ignore_index=True)
    all_data.to_csv("year.csv", index=False)

root = "all_years"
process_all_student_files(root)
