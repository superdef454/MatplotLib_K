import random
import math
import matplotlib.pyplot as plt

import json

def load_data():
    with open("config.txt", 'r') as json_data:
        return json.loads(json_data.read())

def save_data(name, value):
    existing_data = load_data()
    existing_data[name] = value
    with open("config.txt", 'w') as w:
        w.write(json.dumps(existing_data, indent=4, sort_keys=True))

# По варианту:
Aa = 10 # заданная интенсивность потока покупателей
Y_strah_zapas = 120 # Величина страхового запаса
Y_max = 300 # Максимальный запас товариов (Хз где взять)
m = 6 # Поставки

save_data('Aa', Aa)

print(load_data())

# Данные для оценки прибыли
a1 = 50 # Продажа 1 ед. товара
b1 = 10 # Убыток за хранение (профицит)
c1 = 40 # Штраф за дефицит

# Для программы
Y_mas = [Y_max] # Лист точек Y
T_mas = [0] # Лист точек T
T_peresech = [] # Лист пересечений
T_iter = []
Dif = 0 # Дефицит
Prof = 0 # Профицит
# Цит

def R():
    # случайная величина, имеющая равномерное распределение на отрезке [0, 1]
    return random.random()

def ExpZakon(): # (t)
    # Экспоненциальный закон
    return -1/Aa*math.log(1 - R())

def x():
    # Каждый покупатель приобретает x единиц товара,
    # определяется по равномерному закону
    a = 1 # минимальное количество покупаемого товара
    b = 3 # максимальное количество покупаемого товара
    return int(a+R()*(b-a))

def T(): # Время подвоза T определяется по нормальному закону
    Mx = 8 # математическое ожидание времени подвоза
    Sigmax = 0.5 # среднее квадратическое отклонение
    Zz = sum(R() for _ in range(1, 12)) - 6    # нормально распределенная случайная величина с параметрами
    return Mx+Sigmax*Zz

def Max_to_strah(): # Функция покупок товаров до страхового
    global Y_mas, T_mas, Dif, Prof
    Yy = Y_max
    t = T_mas[-1]
    T_mas.append(t)
    Y_mas.append(Yy)
    T_start = t
    while(Yy >= Y_strah_zapas):
        t += ExpZakon()
        T_mas.append(t)
        Y_mas.append(Yy)
        Yy -= x()
        T_mas.append(t)
        Y_mas.append(Yy)
    T_peresech.append(T_mas[-1])
    T_Podvoza = T() + t
    while(t <= T_Podvoza):
        t += ExpZakon()
        T_mas.append(t)
        Y_mas.append(Yy)
        Yy -= x()
        T_mas.append(t)
        Y_mas.append(Yy)
    if Y_mas[-1] < 0:
        Dif += 1
    else:
        Prof += 1
    T_end = T_mas[-1]
    Pr = Y_max - Y_mas[-1]
    if Y_mas[-1] >= 0:
        Pr -= (Y_max - Pr) * b1
        print("Профицит, ", end='')
    else:
        Pr -= c1 * (abs(Y_mas[-1]))
        print("Дефицит,  ", end='')
    T_iter.append((T_end + T_start) / 2)
    print(f'Прибыль: {Pr}')
    # return Pr
    
# Подсчёт модели
for i in range(8): # Кол-во итераций
    print(f'{i+1}: ', end='')
    Max_to_strah()
print(f'Количество случаев профицита: {Prof}\nКоличество случаев дефицита: {Dif}')


# Отрисовка

# Оси и текст
plt.title("Модель управления запасами")
plt.xlabel("Время", loc="right")
plt.ylabel("Товары", loc="top")
plt.text(0.2,122,"Y страховое", fontsize=10, color='orange')
plt.text(0.2,Y_max,"Y max", fontsize=10, color='green')

for i in range(len(T_iter)):
    plt.text(T_iter[i], 285, f'{i+1}')

# Ограничение на экране
plt.xlim([0, T_mas[-1]])
# Добавление точек пересечений с У_страх
plt.scatter(T_peresech, [Y_strah_zapas for _ in range(len(T_peresech))]).set_color('orange') # цвет 
# График эксперимента
plt.plot(T_mas, Y_mas)
# У_страховое
plt.plot([-1, T_mas[-1] + 1],[Y_strah_zapas,Y_strah_zapas], color='orange')
# Y_max
plt.plot([-1, T_mas[-1] + 1],[Y_max,Y_max], color='green')
# 0
plt.hlines(0, -1, T_mas[-1] + 1, color='black')
# Отображение окна
plt.show()