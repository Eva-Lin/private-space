#!/usr/bin/env python
# -*- coding:utf-8 -*-


def heap_sort(L, i):
    """
    从L的父节点i开始重新排序
    :param L: 传入要排序的列表
    :param i: 要排序的父节点
    :return: 排序后的L
    """
    temp_L = [L[i]]
    leftchild_i =  2*i+1
    right_child_i = 2*i+2

    temp_L.extend(L[leftchild_i:right_child_i+1])

    # 获取最大数
    max_item = max(temp_L)

    # 删除最大数后的列表
    temp_L.remove(max_item)

    if L[i] != max_item:
        L[i] = max_item

        for temp_L_i, temp_L_v in enumerate(temp_L):
            child_i = leftchild_i + temp_L_i

            if L[child_i] != temp_L[temp_L_i]:

                L[child_i] = temp_L[temp_L_i]
                L = heap_sort(L, child_i)
    return L


def create_heap(L):
    """
    构造一个大顶堆
    :param L:
    :return:
    """
    range_num = len(L)//2 - 1
    for i in range(range_num, -1, -1):
        L = heap_sort(L, i)
    return L


def add_item(L, v):
    """
    往L中的i下标插入v
    :param L: 要插入的列表
    :param i: 要插入的位置
    :param v: 要插入的值
    :return: 更改后的L
    """
    L.append(v)
    fater_i = (len(L)-2) // 2   # -2 里一个是长度本身减去1，一个是计算需要减1
    flag = True
    while flag:
        if fater_i > 0:
            L = heap_sort(L, fater_i)
            fater_i = (fater_i - 1) // 2
        elif fater_i == 0:
            L = heap_sort(L, fater_i)
            flag = False
    return L


def del_item(L, v):
    """
    从L中删除v
    :param L: 要更改的列表
    :param v: 要删除的值
    :return: 更改后的L
    """
    i = (L.index(v) - 1) // 2
    L.remove(v)
    for change_i in range(i, len(L)):
        L = heap_sort(L, change_i)
    return L


def random_int_list(start, stop, length):
    """
    创建随机队列
    :param start: 起始值
    :param stop: 终止值
    :param length: 长度
    :return: 随机列表
    """
    import random
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


if __name__ == '__main__':

    L = random_int_list(1, 100, 10)
    # L = [20, 17, 14, 16, 15, 10, 8, 13]
    print(L)

    # 轮训次数（顶点个数）
    L = create_heap(L)
    print(L)

    # 添加一个元素（由于会重新排序，这里不考虑插入位置，一律append）
    L = add_item(L, 100)
    print(L)

    # 删除一个元素(涉及到从该节点的父节点到最后一个节点的所有排序)
    L = del_item(L, 100)
    print(L)
