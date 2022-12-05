import random
import math
import matplotlib.pyplot as plt
import os
# import configparser

# config = configparser.ConfigParser()
# config.add_section("settings")

# config = os.getcwd() + "config.txt"
# config = "C:/Users/user/Documents/учёба/git/MatplotLib_K/MatplotLib_Kconfig.txt"

# По варианту:
Aa = 10 # заданная интенсивность потока покупателей
Y_strah_zapas = 120 # Величи а страхового запаса
Y_max = 10000 # Максимальный запас товариов (Хз где взять)
m = 6 # Поставки по варианту
m = 8 # Для среднего

# Данные для оценки прибыли
a1 = 50 # Продажа 1 ед. товара
b1 = 10 # Убыток за хранение (профицит)
c1 = 40 # Штраф за дефицит

# Для программы
Y_mas = [Y_max] # Лист точек Y
T_mas = [0] # Лист точек T
T_peresech = [] # Лист пересечений
T_iter = [] # Позиция номера итерации для граффика
Dif = 0 # Дефицит
Prof = 0 # Профицит
# Цит

def R():
    # случайная величина, имеющая равномерное распределение на отрезке [0, 1]
    return random.random()

def ExpZakon(A = Aa): # (t)
    # Экспоненциальный закон
    return -1/A*math.log(1 - R())

def x():
    # Каждый покупатель приобретает x единиц товара,
    # определяется по равномерному закону
    a = 1 # минимальное количество покупаемого товара
    b = 3 # максимальное количество покупаемого товара
    return int(a+R()*(b-a))

def T(Mx = m): # Время подвоза T определяется по нормальному закону
    # Mx - математическое ожидание времени подвоза
    Sigmax = 0.5 # среднее квадратическое отклонение
    Zz = sum(R() for _ in range(1, 12)) - 6    # нормально распределенная случайная величина с параметрами
    return Mx+Sigmax*Zz

def Max_to_strah_print(): # Функция покупок товаров до страхового и запись в массив для отрисовки
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
    
def print_wiew(): # Подсчёт модели и отрисовка
    for i in range(8): # Кол-во итераций
        print(f'{i+1}: ', end='')
        Max_to_strah_print()
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
    
# print_wiew()

def Max_to_strah_model(Y_str = Y_strah_zapas, MM = m, Aa = Aa): 
    # Функция получения прибыли по законам теории вероятности
    Yy = Y_str
    t = 0
    T_Podvoza = T(Mx=MM) + t
    while(t <= T_Podvoza):
        t += ExpZakon(Aa)
        Yy -= x()
    Pr = Y_max - Yy
    if Yy >= 0:
        Pr -= (Y_max - Pr) * b1
    else:
        Pr -= c1 * (abs(Yy))
    return Pr # Возвращает прибыль
    
def model(iter, Aa, Mm, strah, Kol_vo = 10000):
    print(f'{iter}: lambda: {Aa:3d} | Y_страховое: {strah} | m: {Mm} | Прибыль: ', end='')
    pr = [] # Массив прибыли для подсчёта критеря Кохрена
     # Количество итераций
    Average = 0 
    for _ in range(Kol_vo):
        Average += Max_to_strah_model(strah, Mm, Aa)
    Average = Average / Kol_vo
    pr.append(Average)
    print(f'{pr[-1]:5}', end=', ')
    Average = 0 
    for _ in range(Kol_vo):
        Average += Max_to_strah_model(strah, Mm, Aa)
    Average = Average / Kol_vo
    pr.append(Average)
    print(f'{pr[-1]:5}', end=', ')
    Average = 0 
    for _ in range(Kol_vo):
        Average += Max_to_strah_model(strah, Mm, Aa)
    Average = Average / Kol_vo
    pr.append(Average)
    print(f'{pr[-1]:5}')
    return pr
    
def Regress():
    for _ in range(100):
        kol = 10000
        print(f"Количество итераций в каждом опыте: {kol}")
        mass_Pr = []
        mass_Pr.append(model(1, 6, 4, 100, kol))
        mass_Pr.append(model(2, 14, 4, 100, kol))
        mass_Pr.append(model(3, 6, 4, 140, kol))
        mass_Pr.append(model(4, 14, 4, 140, kol))
        mass_Pr.append(model(5, 6, 8, 100, kol))
        mass_Pr.append(model(6, 14, 8, 100, kol))
        mass_Pr.append(model(7, 6, 8, 140, kol))
        mass_Pr.append(model(8, 14, 8, 140, kol))
        print('\n\n\n')
        from statistics import mean
        disps = 0 # Сумма дисперсий
        dispmax = 0 # Максимальная дисперсия
        dispAv = 0
        for i in range(len(mass_Pr)):
            srednee = round(mean(mass_Pr[i]), 2)
            disp = 0 # Дисперсия
            for j in mass_Pr[i]:
                disp += (j-srednee)**2/(len(mass_Pr[i])-1)
            disp = round(disp, 2)
            disps += disp
            if disp > dispmax:
                dispmax = disp
            dispAv += disp
            print(f"{i}: Среднее: {srednee:7} | Дисперсия: {disp:10}")
        
        grasch = dispmax/disps
        gtabl = 0.5157
        print(f"Gрасч = {grasch}\nGтабл = {gtabl}\nGрасч < Gтабличного => гипотеза об однородности ряда выборочных дисперсии выходного параметра не отвергается")
        if grasch >= gtabl:
            os.system("cls")
            continue
        dispAv /= len(mass_Pr)
        print(f'Средняя дисперсия: {dispAv}')
        print("Уравнение регрессии: b0x0+b1x1+b2x2+b3x3")
        break

Regress()