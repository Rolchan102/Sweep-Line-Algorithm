from point import *


class Event:
    """
    Событие в очереди алгоритма заметающей прямой.
    В каждом объекте Event хранится точка события и
    ассоциированные с ней отрезки.
    """
    def __init__(self, p=None):
        self.edges = []  # отрезки, ассоциированные с событием
        self.p = p  # event point

    def __repr__(self):
        return "{0}{1}".format(self.p, self.edges)


class EventQueue:
    """
    Очередь событий в алгоритме заметающей прямой.
    """
    def __init__(self, lset):  # инициализировать очередь событий
        """
        Конструктор EventQueue.
        Вход
        lset: список объектов Segment. По левому концу каждого отрезка
        создается событие
        Выход
        Отсортированный список событий, который является членом класса
        """
        if lset == None:
            return
        self.events = []
        for l in lset:
            e0 = Event(l.lp)
            inx = self.find(e0)
            if inx == -1:
                e0.edges.append(l)
                self.events.append(e0)
            else:
                self.events[inx].edges.append(l)
            e1 = Event(l.rp)
            if self.find(e1) == -1:
                self.events.append(e1)
        self.events.sort(key=lambda e: e.p)

    def add(self, e):
        """
        Добавляет событие e в очередь, обновляет список событий
        """
        self.events.append(e)
        self.events.sort(key=lambda e: e.p)

    def find(self, t):
        """
        Возвращает индекс события t, если оно присутствует в очереди.
        В противном случае возвращает –1.
        """
        if isinstance(t, Event):
            p = t.p
        elif isinstance(t, Point):
            p = t
        else:
            return -1
        for e in self.events:
            if p == e.p:
                return self.events.index(e)
        return -1

    def is_empty(self):
        return len(self.events) == 0
