# 问题概述：求解某抽卡游戏中，（每一）单次抽卡获得
# 最高品质卡牌的期望概率。

# 问题详细描述：
#    1. 所有可能的单次抽卡结果，从其品质及稀有度上，由
# 低到高可分为 3 种：蓝色、紫色和橙色。橙色又可以细分为
# 两种：普通 与 UP。
#    2. 在不考虑 概率增加机制 及 保底机制 的情况下，各
# 结果的概率为：橙色为 0.6%，紫色恒定为 5.1%，其它为蓝
# 色。当一次抽卡结果为橙色时，系统会再次进行随机判定：二
# 分之一的概率，最终结果为 UP；否则为 普通。
#    3. 概率增加机制：在连续没能抽出 橙色 时，在前73次
# 抽取时，每次出 橙色 概率为 0.6%；在第 74 次及之后的
# 每一次抽取中，每次出 橙色 的概率都比前一次增加 6%。
# 例如，第 73 次出橙色概率为 0.6%，第 74 次为 6.6%，
# 第 75 次为 12.6%，依此类推（封顶为 100%）。优先占用蓝
# 色概率，其次才是紫色。在任意一次抽出橙色后，该机制次数
# 计数立即重置。
#    4. 紫色保底机制：连续 9 次抽出蓝色后，下一次抽取结
# 果必定为紫色或橙色（该次判定的实质是将蓝色替换为紫色。
# 就是说，橙色概率不受该保底影响）。在任意一次抽出紫色或
# 橙色后，该保底次数计数立即重置。
#    5. 橙色保底机制：连续 89 次没有抽出橙色时，下一次
# 抽取结果必定为橙色。在任意一次抽出橙色后，该保底次数
# 计数立即重置。
#    6. UP保底机制：上一次抽得橙色，结果为普通，那么下
# 一次抽得橙色时，结果必定为 UP。在任意一次抽出橙色且
# 结果为 UP 后，该保底次数计数立即重置。
#
# 解题思路：保底与概率增加机制环环相扣，以我们目前的概
# 率论知识储备，企图计算特定结果的期望概率，可能有些困
# 难。不过我们可以通过程序来模拟成千上万次抽取，即可通
# 过所获得的结果序列来计算相应概率。模拟的次数越多，那
# 么计算结果就越准确。
#


import platform
print('系统:',platform.system())

import time
# 用以计时


import random as rand
# 每次抽取（不考虑保底）时，随机生成一个范围（1~1000）的
# 整数。橙色占据 6 （或者更多）个点数，紫色恒定占据 51 个
# 点数。
# 此外，抽取结果为橙色时（不考虑保底），也需要生成一个随机
# 数来判定 UP 或 普通 的结果。


# 以下分别初始化三种保底机制的计数次数（或者说，连续未抽出相应结果的次数）
up = 0
orange = 0
purple = 0

# 以下分别初始化各类抽取结果的数目。
# 每一次模拟得到结果时，相应的计数就会加 1。
# 蓝色结果数量最后用总模拟抽取次数减去其它计数即可，故不单独设置其计数器。
orange_nor = 0
orange_up = 0
purple_num = 0

# 指定一个变量用以在之后储存生成的随机数
rand_num = 0

# 输入模拟抽取的次数。越大越好。
temp = input("Try times : ")
num = int(temp)

# 以下定义一个空列表，用以储存记录相邻橙色抽取之间的次数。
a_orange_pull = []


def pan_orange() :
    # 本函数用于计算 每一次抽取时，橙色 所占的点数（或者说，概率）。
    # 其依据是 概率增加机制。
    if orange <= 72 :    # 在函数内部查看而不改变全局变量时，无需使用 global 。
        return 6
    else :
        return ((60 * orange) - 4314)


def orange_up_pull() :
    # 抽出 橙色UP 时，调用本函数。
    # 本函数会被嵌套到其它函数（橙色抽取orange_pull）中。
    global up
    global orange
    global orange_up
    global purple
    # 相应结果计数增加，重置相关保底计数，并在控制台上显示相关信息。
    up = 0
    orange = 0
    purple = 0
    orange_up += 1
    print("----------orange_up\n")

def orange_pull(a_list) :
    # 抽得橙色（包括触发橙色保底） 时，结果可能为 UP 或 普通，调用本函数用以进行再次判定。
    # 参数位 a_list 用于填入 a_orange_pull 。
    # 本函数会被嵌套到其它函数（紫色保底purple_pull）中。
    global up
    global orange
    global purple
    global orange_up
    global orange_nor
    global rand_num
    
    # 在列表 a_orange_pull 中，记录本次抽得 橙色 所耗费的抽取次数。
    a_list.append(orange + 1)

    if up >= 1 : # 若UP保底机制触发，则直接判定结果为UP 。
        orange_up_pull()
    else : # 若UP保底机制尚未触发，则需要进行随机判定。
        rand_num = rand.randint(1, 2)
        if rand_num == 1 :
            orange_up_pull()
        else : # 抽得橙色普通。相应结果计数增加，增加或重置相关保底计数，并在控制台上显示相关信息。
            up += 1
            orange = 0
            purple = 0
            orange_nor += 1
            print("---------orange_nor\n")

def purple_pull():
    # 触发紫色保底时，结果可能为紫色或橙色。调用本函数用以判定。
    global up
    global orange
    global purple
    global orange_up
    global orange_nor
    global purple_num
    global rand_num
    rand_num = rand.randint(1, 1000)

    if rand_num <= pan_orange() :
        orange_pull(a_orange_pull)
    else : # 抽得紫色。相应结果计数增加，增加或重置相关保底计数，并在控制台上显示相关信息。
        orange += 1
        purple = 0
        purple_num += 1
        print("----purple\n")

def rand_pull():
    # 各个保底均未触发时，调用本函数进行判定
    global up
    global orange
    global purple
    global orange_up
    global orange_nor
    global purple_num
    global rand_num
    rand_num = rand.randint(1, 1000)

    g = pan_orange()
    if rand_num <= g : # 抽得橙色。
        orange_pull(a_orange_pull)
    elif rand_num >= 950 and rand_num > g: # 抽得紫色。and 后面的内容是考虑了橙色概率挤占紫色概率的情况。
        orange += 1
        purple = 0
        purple_num += 1
        print("----purple\n")
    else :
        # 抽得蓝色，各保底计数增加。
        orange += 1
        purple += 1
        print("blue\n")

# 即将模拟，开始计时。
T1 = time.perf_counter()

# 以下开始通过循环计数来多次模拟抽取。
for each in range(num) :
    print("N0. {0}".format(each + 1))
    if orange >= 89 : # 若橙色保底与紫色保底同时触发，那么由前者覆盖后者。故前者判定在外层。
        orange_pull(a_orange_pull)
    else :
        if purple >= 9 : # 仅触发了紫色保底。
            purple_pull()
        else : # 未触发任何保底。
            rand_pull()

# 模拟完毕，计时完成。
T2 =time.perf_counter()

# 计算橙色总量
orange_num = orange_nor + orange_up

# 计算橙色期望概率
orange_rate = float(orange_num) / float(num)

# 计算橙色UP期望概率
orange_up_rate = float(orange_up) / float(num)

# 计算紫色期望概率
purple_rate = float(purple_num) / float(num)

# 计算列表a_orange_pull中所有元素的平均值（即抽得橙色期望花费抽数）
orange_pull_num = 0.
orange_pull_all = 0
length = 0
for i in a_orange_pull :
    length += 1
    orange_pull_all += i
orange_pull_num = float(orange_pull_all) / float(length)

# 在控制台上显示各计算数据。
print("橙色数量 orange_num = ", orange_num, '\n')
print("橙色期望概率 orange_rate = {0:.4f}%\n".format(orange_rate * 100.))
print("橙色UP数量 orange_up = ", orange_up, '\n')
print("橙色UP期望概率 orange_up_rate = {0:.4f}%\n".format(orange_up_rate * 100.))
print("橙色所需抽取次数期望 orange_pull_num = {0:.3f}\n".format(orange_pull_num))
print("紫色数量 purple_num = ", purple_num, '\n')
print("紫色期望概率 purple_rate = {0:.4f}%\n".format(purple_rate * 100.))

# 在控制台上显示程序用时。
mock_time = (T2 - T1)*1000.
eve_mock_time = mock_time / float(num)
print('模拟抽取耗费时间:%s毫秒' % (mock_time))
print('单次抽取耗费时间:%s毫秒' % (eve_mock_time))

# 在生成的控制台可执行文件中，程序完成全部运算后，会自动退出，导致用户无法看到运算结果。
# 通过 input 使程序在最后“卡住”，用户才有时间查看结果。
input("Press any button to end.")