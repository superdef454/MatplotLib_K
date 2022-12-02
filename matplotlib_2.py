import random
import math
import matplotlib.pyplot as plt


# По варианту:
Aa = 10 # заданная интенсивность потока покупателей
Y_strah_zapas = 120 # Величина страхового запаса
Y_max = 300 # Максимальный запас товариов (Хз где взять)
m = 6 # Поставки

# Для программы
Y_mas = [Y_max] # Лист точек Y
T_mas = [0] # Лист точек T
T_peresech = [] # Лист пересечений
Dif = 0
Prof = 0

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
    
# Подсчёт модели
for i in range(100): # Кол-во итераций
    Max_to_strah()
print(f'Количество случаев профицита: {Prof}\nКоличество случаев дефицита: {Dif}')


# Отрисовка

# Оси и текст
plt.title("Модель управления запасами")
plt.xlabel("Время", loc="right")
plt.ylabel("Товары", loc="top")
plt.text(0.2,122,"Y страховое", fontsize=10, color='orange')
plt.text(0.2,Y_max,"Y max", fontsize=10, color='green')

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