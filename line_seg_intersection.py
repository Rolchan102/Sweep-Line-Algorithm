from bintrees import AVLTree
from point import *
from intersection import *
from line_seg_eventqueue import *


def get_edges(t, p):
    """
    Возвращает отрезки, для которых точка p является
    внутренней или правым концом.
    """
    lr = []
    lc = []
    for s in AVLTree(t):
        if s.rp == p:
            lr.append(s)
        elif s.lp == p and s.status == INTERIOR:
            lc.append(s)
        elif sideplr(p, s.lp, s.rp) == 0:
            lc.append(s)
    return lr, lc


def get_lr(T, s):
    """
    Возвращает левого и правого соседа (ветви) узла p в дереве T
    """
    try:
        sl = T.floor_key(s)
    except KeyError:
        sl = None
    try:
        sr = T.ceiling_key(s)
    except KeyError:
        sr = None
    return sl, sr


def get_lrmost(T, segs):
    """
    Находит в дереве T самый левый и самый правый отрезок из присутствующих в списке segs
    """
    l = []
    for s in list(T):
        if s in segs:
            l.append(s)
    if len(l) < 1:
        return None, None
    return l[0], l[-1]


def find_new_event(s1, s2, p, q):
    """
    Проверяет, пересекает ли s1 s2 в точке, которой нет в очереди событий.
    Когда будет найдена новая точка пересечения, будет создано новое событие
    и добавлено в очередь событий.

    Input:
       s1: линейный сегмент
       s2: линейный сегмент
       p: точка текущего события
       q: очередь событий

    Вывод:
       True, если найдена новая точка, False в противном случае.

    Изменение: содержимое очереди (q) может измениться.
    """
    ip = intersectx(s1, s2)
    if ip is None:
        return False
    if q.find(ip) != -1:
        return False
    if ip.x > p.x or (ip.x == p.x and ip.y >= p.y):
        e0 = Event()
        e0.p = ip
        e0.edges = [s1, s2]
        q.add(e0)
    return True


def intersectx(s1, s2):
    """
    Проверяет, пересекаются ли два отрезка, и возвращает
    точку их пересечения.
    """
    if not test_intersect(s1, s2):
        return None
    p = getIntersectionPoint(s1, s2)  # an intersection
    return p


def intersections(psegs):
    """
    Реализация алгоритма Бентли–Оттмана.
    Вход
    psegs: список отрезков
    Выход
    intpoints: список точек пересечения
    """
    eq = EventQueue(psegs)
    intpoints = []
    T = AVLTree()
    L = []
    while not eq.is_empty():    # для каждого события
        e = eq.events.pop(0)    # удалить событие
        p = e.p                 # получить точку события
        L = e.edges             # отрезки, для которых p – левый конец
        R, C = get_edges(T, p)  # p: правый конец (R) или внутренняя (C)
        if len(L + R + C) > 1:  # пересечение в p принадлежит L+R+C
            for s in L + R + C:
                if not s.contains(p):  # если p внутренняя
                    s.lp = p  # изменить lp и
                    s.status = INTERIOR  # статус
            intpoints.append(p)
            R, C = get_edges(T, p)
        for s in R + C:
            T.discard(s)
        for s in L + C:
            T.insert(s, str(s))
        if len(L + C) == 0:
            s = R[0]
            if s is not None:
                sl, sr = get_lr(T, s)
                find_new_event(sl, sr, p, eq)
        else:
            sp, spp = get_lrmost(T, L + C)
            try:
                sl = T.prev_key(sp)
            except KeyError:  # только для первого ключа
                sl = None
            try:
                sr = T.succ_key(spp)
            except KeyError:  # только для последнего ключа
                sr = None
            find_new_event(sl, sp, p, eq)
            find_new_event(sr, spp, p, eq)
    return intpoints


if __name__ == "__main__":
    s = [[[20, 15], [0, 16]], [[3, 18], [2, 3]], [[4, 14], [6, 19]],
         [[10, 17], [0, 6]], [[8, 3], [5, 10]], [[6, 6], [11, 9]],
         [[16, 14], [10, 6]], [[16, 10], [10, 11]],
         [[14, 8], [16, 12]]]

    psegs = [Segment(i, Point(s[i][0][0], s[i][0][1]),
                     Point(s[i][1][0], s[i][1][1]))
             for i in range(len(s))]

    ints = intersections(psegs)
    rounded_ints = [(round(point.x, 1), round(point.y, 1)) for point in ints]
    print("Число точек пересечения: ", len(rounded_ints))
    print(rounded_ints)
