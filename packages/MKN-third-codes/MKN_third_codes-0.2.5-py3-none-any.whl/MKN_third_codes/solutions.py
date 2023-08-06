import math

class Box():
    """
    Класс урны (коробки) для задачи об урнах

    Args:
        white (int): кол-во белых шаров (не является параметром)
        black (int): кол-во черных шаров (не является параметром)
        grabbing (int): кол-во шаров, забираемых из коробки
    
    Parameters:
        balls (list): массив длиной 2, хранящий информация о количестве Б и Ч шаров ([Б, Ч])

    Methods:
        None
    """
    def __init__(self, white:int=0, black:int=0, grabbing:int=0):
        self.balls = [white, black]
        self.grabbing = grabbing

class Hypotes():
    """
    Класс гипотезы для задачи об урнах

    Args:
        balls (list): массив, длиной 2, обозначающий количество белых и чёрных шаров ([Б, Ч])
        probability (float): вероятность наступления гипотезы
        id (int): порядковый номер гипотезы
    
    Parameters:
        depend_probability (float): вероятность достать Б шар из урны с шарами self.balls
        hypo_text (str): строка формата 'H(id): nБ mЧ; P(H(id)) = p; P(A|H(id)) = p`'
        summary_text (str): строка, использующаяся для составления строки для уравнения суммы вероятностей гипотез

    Methods:
        None
    """
    def __init__(self, balls=None, probability=0, id=0):
        if balls == None:
            balls = [0,0]
        self.balls = balls
        self.probability = probability
        self.depend_probability = balls[0]/sum(balls)
        self.id = id
        self.hypo_text = f"H{self.id}: {self.balls[0]} Б, {self.balls[1]} Ч; P(H{self.id}) = {self.probability}; P(A|H{self.id}) = {self.depend_probability}"
        self.summary_text = f"P(A|H{self.id})P(H{self.id})"

class Hypoteses():
    """
    Класс, использующийся только для решения задачи об урнах. Бесполезен вне решения.

    Methods:
        check_correctly
        get_whites_n_blacks_from_boxes
        get_from_boxes
        get_zn
    """
    def __init__(self, boxes):
        self.U = boxes
        self.P = 0
        self.main_z = 1

    def check_correctly(self, mnoz, whites, totalWhite):#проверяет, что все предоставленные слагаемые
                                                        #содержат требуемое по условию количество шаров
        new_mnoz = []
        for i in range(0, len(mnoz)):
            if whites[i] == totalWhite:
                new_mnoz.append(mnoz[i])
        return(new_mnoz)
    
    def get_whites_n_blacks_from_boxes(self, wGrab=0, id=0, whites=None, mnoz=None, totalW=0):#посчитать для взятия "wGrab" белых шаров из
                                                                            #оставшихся урн, включая урну с индексом "id"
        if whites == None:
            whites = []
        if mnoz == None:
            mnoz = []
        if id >= len(self.U):
            return self.check_correctly(mnoz, whites, totalW)
        
        grabbing = self.U[id].grabbing#сколько всего берём шаров из урны

        mx_kW = self.U[id].balls[0]#сколько всего Б шаров
        mx_kB = self.U[id].balls[1]#сколько всего Ч шаров

        mn_kW = grabbing - mx_kB#сколько минимум Б шаров потребуется
        kW = max(mn_kW, 0)#старт Б шаров
        kB = min(mx_kB, grabbing)#старт Ч шаров

        mx_kW = max(min([mx_kW, grabbing]), 0)#максимум можно взять из этой урны Б шаров

        if mnoz == []:#если множество слагаемых гипотезы пусто
            while kW <= mx_kW:#перебираем все возможные варианты взятия шаров из этой урны
                mnoz.append(1)
                whites.append(kW)
                mnoz[-1] *= combinations(kW, self.U[id].balls[0])*combinations(kB, self.U[id].balls[1])
                kW += 1
                kB -= 1
        else:#если множество слагаемых гипотезы не пусто
            new_mnoz = []
            new_whites = []
            while kW <= mx_kW:#перебираем все возможные варианты взятия шаров из этой урны
                editor = combinations(kW, self.U[id].balls[0])*combinations(kB, self.U[id].balls[1])
                for i in range(0, len(mnoz)):#каждое из существующих слагаемых умножаем на результат
                                            #перемножения перестановок Kw из Nw и Kb из Nb шаров
                    new_mnoz.append(mnoz[i]*editor)
                    new_whites.append(whites[i] + kW)
                kW += 1
                kB -= 1
            mnoz = new_mnoz
            whites = new_whites
        return self.get_whites_n_blacks_from_boxes(wGrab-kW, id+1, whites, mnoz, totalW)

    def get_from_boxes(self):#решает задачу через теорему гипотез
        grabGlob = 0#сколько всего берём шаров из урн
        whiteGlob, blackGlob = 0, 0
        for box in self.U:
            grabGlob += box.grabbing
            whiteGlob += box.balls[0]
            blackGlob += box.balls[1]
        
        if grabGlob > whiteGlob+blackGlob:
            return

        revealing_after_B = max(grabGlob-blackGlob, 0)

        gW = max(0, revealing_after_B)#от скольки белых шаров может находиться в n+1 урне (куда их все складывают)
        gW_end = min(whiteGlob, grabGlob)#до скольки белых шаров может находиться в n+1 урне

        hypoteses_P_array = []
        while gW <= gW_end:#генерируем гипотезы для всех возможных количеств Белых и Черных шаров
            hypoteses_P_array.append([sum(self.get_whites_n_blacks_from_boxes(gW, 0, [], [], gW))/self.get_zn(), gW, grabGlob-gW])
            gW += 1
        return hypoteses_P_array#массив вероятностей для всех гипотез

    def get_zn(self):#получить общий знаменатель для формулы вероятности гипотезы
        if self.main_z == 1:
            for i in range(len(self.U)):
                self.main_z *= combinations(self.U[i].grabbing, sum(self.U[i].balls))
        return self.main_z

class EttaTableCell():
    """
    Ячейка таблицы Етта, со значением и вероятностью
    """
    def __init__(self, etta_value:int=0, good_th:int=1, bad_th:int=1, probability:float=None):
        self.etta_value = etta_value
        self.good_th = good_th
        self.bad_th = bad_th
        self.probability = probability
        if self.probability == None:
            self.probability = good_th/(good_th+bad_th)

class EttaTable():
    """
    Таблица значений Етта
    """
    def __init__(self, cells=None):
        self.cells = cells
        if self.cells == None:
            self.cells=[]


def combinations(k:float=0,n:float=0):
    """
    Функция, считающая число сочетаний из n по k

    Args:
        k (float): аргумент k - количество повторений
        n (float): аргумент n - всего элементов

    Returns:
        float: результат применения формулы числа сочетаний
    """
    if k < 0 or n < 0:
        raise ValueError("ERROR: one or more argument's values are less than 0")
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def buckets_n_balls_solution(boxes):
    """
    Находит ответ для вопроса 'какова вероятность достать Белый шар из n+1 урны' для задачи о n урнах с белыми и чёрными шарами, когда из каждой урны берут Ki шаров, перекладывают их в n+1 урну.
    Для решения используется теорема гипотез

    Args:
        boxes (list): массив объектов класса Box

    Returns:
        list: [list: массив объектов Hypotes, float: итоговая пероятность искомого события]
    """
    myHyp = Hypoteses(boxes)

    hypot_prob = myHyp.get_from_boxes()

    prob_final = 0
    ready_hipoteses = []
    for i in range(0, len(hypot_prob)):
        ready_hipoteses.append(Hypotes([hypot_prob[i][1], hypot_prob[i][2]], hypot_prob[i][0], i+1))
        prob_final += hypot_prob[i][0]*hypot_prob[i][1]/(hypot_prob[i][1]+hypot_prob[i][2])
    
    return(ready_hipoteses, prob_final)

def buckets_n_balls_terminal():
    """
    Решение задачи о n урнах с белыми и чёрными шарами, когда из каждой урны берут Ki шаров, перекладывают их в n+1 урну.
    """
    boxes = [Box() for _ in range(int(input("Введите количество урн: ")))]

    for i in range(len(boxes)):
        boxes[i].balls[0] = int(input(f"Кол-во Б шаров в {i+1} урне: "))
        print("\033[F                                                                       ", end="\r")
        boxes[i].balls[1] = int(input(f"Кол-во Ч шаров в {i+1} урне: "))
        print("\033[F                                                                       ", end="\r")
    print("Шары заданы.")

    for i in range(len(boxes)):
        boxes[i].grabbing = int(input(f"Сколько шаров берут из {i+1} урны: "))
        print("\033[F                                                                       ", end="\r")
    print("Кол-во взятых шаров задано.")

    result = buckets_n_balls_solution(boxes)

    print("Обозначим событие A - достать Белый шар")

    txt = "P(B) = "
    for hypo in result[0]:
        print(hypo.hypo_text)
        txt += hypo.summary_text + " + "
    
    print(f"Обозначим событие B - достать шар из {len(boxes)+1} урны")
    txt = txt[:-3]
    txt += f"\nP(B) = {result[1]}"
    print(txt)

def things_complexity_terminal():
    """
    Общее решение задачи о 'невнимательной секретарше' (сколько людей получат свои вещи)
    WARNING: Очень неоптимизированное! Не рекоммендую пытаться решить для количества людей > 9
    """
    humans = int(input("Введите количество человек: "))
    result = things_complexity_solution(humans)
    print("Таблица:")
    for cell in result.cells:
        print(f"E = {cell.etta_value}; P = {cell.probability} ({cell.good_th}/{cell.bad_th})")

def things_complexity_solution(humans:int = 0):
    """
    Решение задачи о 'невнимательной секретарше' (сколько людей получат свои вещи)
    WARNING: Очень неоптимизированное! Не рекоммендую пытаться решить для количества людей > 9

    Args:
        humans (int): кол-во людей

    Returns:
        EttaTable: таблица ячеек таблицы
    """
    tickets = [-1 for _ in range(humans)]
    #следующей строчкой находим количество всех перестановок
    allPerestan = math.factorial(humans)

    def editCopy(array, k, value):
        array[k] = value
        return array

    #Функция, позволяющая найти количество перестановок, удовлетворяющих условию:
    #"n человек получили нужные вещи"
    def findCountNumber(n, layer, tick, setting:set, i=0):
        #выход из рекурсии, когда все вещи рапределены
        if -1 not in tick:
            #если нам осталось распределить 0 вещей правильно
            if n == 0:
                #перевод массива в хэшируемый вид
                bigTick = 0
                for el in range(0, len(tick)):
                    bigTick += tick[el]*(humans**el)
                #добавляем новую перестановку в set()
                setting.add(bigTick)
            return setting
        start = min(tick)+1
        #если предемт ещё не выдан
        if tick[i] == -1:
            copy = []
            for el in tick:
                copy.append(el)
            #проходимся по всем вещам
            for k in range(start, humans):
                #если вещь ещё не выдана
                if k not in tick:
                    #если вещь принадлежит человку, которому сейчас выдаем
                    if i == k:
                        #проверяем, можем ли мы ему выдать (и выдаём, если да)
                        if n > 0:
                            #при этом в следующем шаге рекурсии уменьшаем n
                            setting = findCountNumber(n-1, layer+1, editCopy(copy,i,k), setting, i+1)
                    #иначе
                    else:
                        #в следующем шаге рекурсии n остаётся прежним
                        setting = findCountNumber(n, layer+1, editCopy(copy,i,k), setting, i+1)
        
        return setting
    
    myTable = EttaTable(cells=[])

    #для каждой "Этта" от 0 до humans вычисляем вероятность (Этта людей получили свои вещи)
    for j in range(0, humans+1):
        cnt = findCountNumber(j, 0, tickets, set())
        myTable.cells.append(EttaTableCell(j, len(cnt), allPerestan, len(cnt)/allPerestan))
    
    return myTable


__all__ = ['combinations', 'buckets_n_balls_solution', 'buckets_n_balls_terminal', 'things_complexity_terminal', 'things_complexity_solution']