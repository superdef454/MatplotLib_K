import random
import math
import matplotlib.pyplot as plt


# По варианту:
Aa = 10 # заданная интенсивность потока покупателей
Y_strah_zapas = 120 # Величина страхового запаса
Y_max = 300 # Хз где взять
m = 6 # Поставки

Y_mas = [] # Лист точек Y
T_mas = [] # Лист точек T
T_peresech = [] # Лист пересечений

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
    Mx = 0 # математическое ожидание времени подвоза
    Sigmax = 0 # среднее квадратическое отклонение
    Zz = sum(R() for _ in range(1, 12)) - 6    # нормально распределенная случайная величина с параметрами

def Max_to_strah(): # Функция покупок товаров до страхового
    global Y_mas, T_mas
    Yy = Y_max
    t = 0
    T_mas.append(0)
    Y_mas.append(Yy)
    while(Yy >= Y_strah_zapas):
        t += ExpZakon()
        T_mas.append(t)
        Y_mas.append(Yy)
        Yy -= x()
        T_mas.append(t)
        Y_mas.append(Yy)
    T_peresech.append(T_mas[-1])
    
Max_to_strah()
# Отрисовка
plt.title("Модель управления запасами")
plt.xlabel("Время", loc="right")
plt.scatter(T_peresech, [Y_strah_zapas for _ in range(len(T_peresech))]) # Можно сделать список пересечений list_per = [] \n list_per.append(t_mas[-1])
plt.plot(T_mas, Y_mas)
plt.plot([-1, T_mas[-1]],[Y_strah_zapas,Y_strah_zapas])
plt.show()
# Х - t || Y - Товар 