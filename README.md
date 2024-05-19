# Модель для предсказания поступления в вуз по ЕГЭ

---

### [Парсинг и все данные](https://github.com/2reckey/EGE_Score_Admission_Predictor/tree/main/Parser%20%26%20Full%20Data)

Данные конкурсных списков парсил с сайта [admlist.ru](https://web.archive.org/web/20210821061126/http://admlist.ru/)

Данные по проходным баллам получал с веб архива официальных сайтов вузов, приказов о зачислении вузов, а также сайтов [vuzoteka.ru](https://vuzoteka.ru/) и [tabiturient.ru](https://tabiturient.ru/)


---

### [Модель и статистика](https://github.com/2reckey/EGE_Score_Admission_Predictor/tree/main/Stats%20%26%20Prediction%20Model)

Для предсказания модели использовал:

- Средний балл __ЕГЭ__ определенного человека `[Avg_score]`
- КЦП направления _(Максимальное количество людей которые могут поступить на бюджет по данному направлению)_ `[Quota]`
- Конкурс для данного направления _(Все заявления / КЦП)_ `[All_app]`
- Конкурс по оригиналам _(Все оригиналы / КЦП)_ `[Orig_all]`
- Доля БВИ _(Оригиналы БВИ / КЦП)_ `[BVI]`
- Доля оригиналов над _(у которых больше баллов)_ определенным человеком _(Ко-во Оригиналов над человеком / КЦП)_ `[Orig_above]`
- Квантили распределения для данного направления `[q10 ... q90]`
- 25% Квантили распределения среди абитуриентов от $(i = 0 \dots 9) \cdot \textbf{КЦП}$ до $(i + 1 = 1 \dots 10) \cdot \textbf{КЦП}$  `[q25_by_1Q ... q25_by_10Q]`

---

Использовал классификацию для предсказания баллов __ЕГЭ__ вместо регрессии, так как метрика доли верно предсказанных реальных людей является более объективной чем _MSE_ от проходного балла

---

Итоговая модель состоит из блендинга моделей  `CatBoost` , `XGBoost` , `LightGBM`

Результаты на тесте:

```
Accuracy: 0.8993010772500031
AUC: 0.9639012251197426
Precision: 0.8626136679506016
Recall: 0.8751661845635691
F1: 0.8688445909192718
```

При максимизации _F1_:

```
Лучший порог: 0.47672671314044734
Лучший precision: 0.8577793815403442
Лучший recall: 0.8810642258015132
Лучший F1: 0.8692659000663786
```

---

Вектор Шепли `LightGBM` на тесте:

![lgb_model_shap](https://github.com/2reckey/EGE_Score_Admission_Predictor/blob/main/Stats%20%26%20Prediction%20Model/Assets/Shap/LightGBM_Shap.png)

---
### [График зависимостей предсказания модели от `Score` и `Orig_above`](https://github.com/2reckey/EGE_Score_Admission_Predictor/tree/main/Stats%20%26%20Prediction%20Model/Assets)
![plot](https://github.com/2reckey/EGE_Score_Admission_Predictor/blob/main/Stats%20%26%20Prediction%20Model/Assets/Test/2018%20-%20%D0%A0%D0%A2%D0%A3%20%D0%9C%D0%98%D0%A0%D0%AD%D0%90%20-%20%D0%98%D0%A2%20-%20%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%B0%D1%8F%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D1%8F%20(09.03.04).png)
