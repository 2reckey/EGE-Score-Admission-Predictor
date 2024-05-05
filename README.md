# Модель предсказания поступления в вуз по ЕГЭ

---

### [Парсинг и все данные](https://github.com/2reckey/EGE_Score_Admission_Predictor/tree/main/Parser%20%26%20Full%20Data)

Данные конкурсных списков парсил с сайта [admlist.ru](https://web.archive.org/web/20210821061126/http://admlist.ru/)

Данные по проходным баллам получал с веб архива официальных сайтов вузов, приказов о зачислении вузов, а также сайтов [vuzoteka.ru](https://vuzoteka.ru/) и [tabiturient.ru](https://tabiturient.ru/)


---

### [Модель и статистика](https://github.com/2reckey/EGE_Score_Admission_Predictor/tree/main/Stats%20%26%20Prediction%20Model)

Для предсказания модели использовал:

- Средний балл __ЕГЭ__ определенного человека `[Avg_score]`
- КЦП направления (Максимальное количество людей которые могут поступить на бюджет по данному направлению) `[Quota]`
- Конкурс для данного направления (Все заявления / КЦП) `[All_app]`
- Конкурс по оригиналам (Все оригиналы / КЦП) `[Orig_all]`
- Доля БВИ (Оригиналы БВИ / КЦП) `[BVI]`
- Доля оригиналов над (у которых больше баллов) определенным человеком (Ко-во Оригиналов над человеком / КЦП) `[Orig_above]`
- Квантили распределения для данного направления `[q10 ... q90]`
- 25% Квантили распределения среди первых (1 ... 10) * КЦП абитуриентов `[q25_by_1Q ... q25_by_10Q]`

---

Использовал классификацию для предсказания баллов __ЕГЭ__ вместо регрессии, так как метрика доли верно предсказанных реальных людей является более объективной чем _MSE_ от проходного балла

---

Итоговая модель состоит из блендинга моделей  `CatBoost` , `XGBoost` , `LightGBM`

Результаты на тесте:

```
Accuracy: 0.8952246239540339
AUC: 0.9621777680187374
Precision: 0.8673438061907394
Recall: 0.8439591014611498
F1: 0.8554916795355939
```

При максимизации _F1_:

```
Лучший порог: 0.39503919493225403
Лучший precision: 0.8442936845927833
Лучший recall: 0.8730882152123447
Лучший F1: 0.8584495577597636
```

---

Вектор Шепли `LightGBM` на тесте:

![lgb_model_shap](https://github.com/2reckey/EGE_Score_Admission_Predictor/blob/main/Stats%20%26%20Prediction%20Model/Assets/Shap/LightGBM_Shap.png)

---
### [График зависимостей предсказания модели от `Avg_score` и `Orig_above`](https://github.com/2reckey/EGE_Score_Admission_Predictor/tree/main/Stats%20%26%20Prediction%20Model/Assets)
![plot](https://github.com/2reckey/EGE_Score_Admission_Predictor/blob/main/Stats%20%26%20Prediction%20Model/Assets/Test/2018%20-%20%D0%A0%D0%A2%D0%A3%20%D0%9C%D0%98%D0%A0%D0%AD%D0%90%20-%20%D0%98%D0%A2%20-%20%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%B0%D1%8F%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D1%8F%20(09.03.04).png)
