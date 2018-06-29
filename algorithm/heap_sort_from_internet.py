#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 堆排序适用于记录数很多的情况

"""
堆排序的思想: 堆是一种数据结构，可以将堆看作一棵完全二叉树，这棵二叉树满足，任何一个非叶节点的值都不大于（或不小于）其左右孩子节点的值。 将一个无序序列调整为一个堆，就可以找出这个序列的最大值（或最小值），然后将找出的这个值交换到序列的最后一个，这样有序序列就元素就增加一个，无序序列元素就减少一个，对新的无序序列重复这样的操作，就实现了排序。

堆排序的执行过程：

1.从无序序列所确定的完全二叉树的第一个非叶子节点开始，从右至左，从下至上，对每个节点进行调整，最终将得到一个大顶堆。

    对节点的调整方法：将当前节点（假设为a）的值与其孩子节点进行比较，如果存在大于a的值的孩子节点，则从中选出最大的一个与a交换。当a来到下一层的时候重复上述过程，直到a的孩子节点的值都小于a为止

2.将当前无序序列中的第一个元素（反映在数中是根节点b），与无序序列中的最后一个元素交换（假设为c），b进入有序序列，到达最终位置。无序序列元素减少1个，有序序列元素增加1个，此时只有节点c可能不满足堆的定义，对其进行调整。

3.重复2 的过程，直到无序序列的元素剩下一个时排序结束。
"""

"""
缺点：
    这里的排序思想时将一个队列分了两部分，一部分时有序区，一部分时无序区，这里进行排序的时候会对无序区进行len(number)-1次排序判断。 \
而该判断除了第一次的判断剩下都是重复的，与堆的思想和理念冲突。
优化方向：
    将每个元素和任意顶点的“三角元素”都看做一个堆，用以堆思想去减少重复排序。
"""


def element_exchange(numbers,low,high):
    """
    调整长度为high的number队列里父节点low与其孩子的位置
    :param numbers: 要排序的队列numbers
    :param low: 父节点下标
    :param high: 要排序队列numbers的长度
    :return: None
    """
    
    temp = numbers[low]

    # j 是low的左孩子节点(cheer!)
    i = low
    j = 2*i

    while j<=high:
        # 如果右节点较大，则把j指向右节点
        if j<high and numbers[j]<numbers[j+1]:
            j = j+1
        if temp<numbers[j]:
            # 将numbers[j]调整到双亲节点的位置上
            numbers[i] = numbers[j]
            i = j
            j = 2*i
        else:
            break

    # 被调整节点放入最终位置
    numbers[i] = temp

def top_heap_sort(numbers):

    length = len(numbers)-1

    # 指定第一个进行调整的元素的下标
    # 它即该无序序列完全二叉树的第一个非叶子节点
    # 它之前的元素均要进行调整
    # cheer up！
    first_exchange_element = length//2

    #建立初始堆
    for x in range(first_exchange_element):
        element_exchange(numbers,first_exchange_element-x,length)

    # 将根节点放到最终位置，剩余无序序列继续堆排序
    # length-1 次循环完成堆排序
    for y in range(length-1):
        # 取出number中最大的值
        temp = numbers[1]
        # 将number中1的值与number最后开始更换
        numbers[1] = numbers[length-y]
        # 将number中被更换的位置放上最大值
        numbers[length-y] = temp
        # 从1位置到被更换位置的数据重新排序
        element_exchange(numbers,1,length-y-1)

if __name__=='__main__':

    from collections import deque

    # 这里需要说明元素的存储必须要从1开始
    # 涉及到左右节点的定位，和堆排序开始调整节点的定位
    # 在下标0处插入0，它不参与排序
    L = deque([49, 38, 65, 97, 76, 13, 27, 49])
    L.appendleft(0)

    # L = [0,49,38,65,97,76,13,27,49]
    import time

    t10 = 0
    for i in range(10):
        stime = time.time()
        top_heap_sort(L)
        etime = time.time()
        t = etime - stime
        t10 += t

    print(t10, L)


