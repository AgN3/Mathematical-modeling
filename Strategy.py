import math
import numpy as np
import pandas as pd
from scipy.optimize import leastsq
from matplotlib import pyplot as plt

path_gold = r'E:\大学\数学建模\2022年美赛\2022_Problem_C_DATA\LBMA-GOLD.xlsx'
path_bit = r'E:\大学\数学建模\2022年美赛\2022_Problem_C_DATA\BCHAIN-MKPRU.xlsx'

plt.rcParams['font.family'] = ['STZhongsong']

gold_df = pd.read_excel(path_gold)
bit_df = pd.read_excel(path_bit)

gold = gold_df['Value'].tolist()
bit = bit_df['Value'].tolist()

for i in range(len(gold)):
    gold[i] = round(gold[i]/100,2)
    bit[i] = round(bit[i]/100,2)

def func(p, x):
    k, y = p
    return k * x + y

def error(p, x, y):
    return func(p, x) - y

def Date(t):
    if t % 7 == 1:
        print('Day{}, Mon'.format(t))
    elif t % 7 == 2:
        print('Day{}, Tues'.format(t))
    elif t % 7 == 3:
        print('Day{}, Wed'.format(t))
    elif t % 7 == 4:
        print('Day{}, Thur'.format(t))
    elif t % 7 == 5:
        print('Day{}, Fri'.format(t))
    elif t % 7 == 6:
        print('Day{}, Sat'.format(t))
    else:
        print('Day{}, Sun'.format(t))

def Fit(t,data):
    Xi = np.array(range(t-3,t+3))
    Yi = np.array(data[t-3:t+3])
    p0 = np.array([t, data[t]])
    Para = leastsq(error, p0, args=(Xi, Yi))
    k, y = Para[0]
    if np.abs(k)<0.025:
        return 0
    else:
        return k

def Asset_State(state, t):
    return round(state[0] + state[1] * gold[t] + state[2] * bit[t], 2)

def Market_state(data):
    value = sum(data[-5:len(data)])
    if -3 <=value<=3:
        return 0
    elif value>3:
        return 1
    elif value<-3:
        return -1

#投资初始状态
invest_state = [1000,0,0]
#黄金市场初始状态 稳定 牛市 熊市
market_state_g = 0
#比特币市场初始状态 稳定 牛市 熊市
market_state_b = 0
#黄金佣金率
g = 0.01
#比特币佣金率
b = 0.02
#黄金涨跌趋势
g_trend = []
#比特币涨跌趋势
b_trend = []

save = []
Assets = []
for i in range(1, 1820):
    if i <= 14:  # 观望14天
        Date(i)
        g_trend.append(0)
        b_trend.append(0)
        assets = Asset_State(invest_state, i)
        print('The current investment volume status is: {}, and the asset is: {} USD '.format(invest_state, assets))
    else:  # 开始购买
        Date(i)
        g_k = Fit(i, gold)
        b_k = Fit(i, bit)
        print('g_k:{},b_k:{}'.format(g_k, b_k))
        if i == 15:  # 第15天购买
            g_ch = 40
            b_ch = 50
            g_trend.append(0)
            b_trend.append(0)
            cash = g_ch * gold[i] * (1 + g) + b_ch * bit[i] * (1 + b)
            invest_state[0] = invest_state[0] - cash
            invest_state[1] = invest_state[1] + g_ch
            invest_state[2] = invest_state[2] + b_ch
            assets = Asset_State(invest_state, i)
            print('The current investment volume status is: {}, and the asset is: {} USD '.format(invest_state, assets))
        else:
            if 1 <= i % 7 <= 5:  # 黄金和比特币均可以交易
                # 黄金
                if np.abs(g_k) <= 0.05:
                    g_trend.append(0)
                    invest_state[1] = invest_state[1]
                elif g_k > 0.05:
                    if 0.05 < g_k <= 0.075:
                        g_trend.append(1)
                        g_ch = math.ceil(invest_state[1] * 0.05)
                    elif 0.075 < g_k <= 0.1:
                        g_trend.append(2)
                        g_ch = math.ceil(invest_state[1] * 0.1)
                    else:
                        g_trend.append(3)
                        g_ch = math.ceil(invest_state[1] * 0.15)
                    g_cash = g_ch * gold[i] * (1 + g)
                    if invest_state[0] > g_cash:
                        invest_state[0] = invest_state[0] - g_cash
                        invest_state[1] = invest_state[1] + g_ch
                else:
                    if -0.075 < g_k <= -0.05:
                        g_trend.append(-1)
                        g_ch = math.ceil(invest_state[1] * 0.05)
                    elif -0.1 < g_k < -0.75:
                        g_trend.append(-2)
                        g_ch = math.ceil(invest_state[1] * 0.1)
                    else:
                        g_trend.append(-3)
                        g_ch = math.ceil(invest_state[1] * 0.15)
                    g_cash = g_ch * gold[i] * (1 - g)
                    invest_state[0] = invest_state[0] + g_cash
                    invest_state[1] = invest_state[1] - g_ch

                # 比特币
                if np.abs(b_k) <= 1:
                    b_trend.append(0)
                    invest_state[2] = invest_state[2]
                elif b_k > 1:
                    if 1 < b_k <= 5:
                        b_trend.append(1)
                        b_ch = math.ceil(invest_state[2] * 0.05)
                    elif 5 < g_k <= 10:
                        b_trend.append(2)
                        b_ch = math.ceil(invest_state[2] * 0.1)
                    else:
                        b_trend.append(3)
                        b_ch = math.ceil(invest_state[2] * 0.15)
                    b_cash = b_ch * bit[i] * (1 + b)
                    if invest_state[0] > b_cash:
                        invest_state[0] = invest_state[0] - b_cash
                        invest_state[2] = invest_state[2] + b_ch
                else:
                    if -5 <= b_k < -1:
                        b_trend.append(-1)
                        b_ch = math.ceil(invest_state[2] * 0.05)
                    elif -10 <= b_k < -5:
                        b_trend.append(-2)
                        b_ch = math.ceil(invest_state[2] * 0.1)
                    else:
                        b_trend.append(-3)
                        b_ch = math.ceil(invest_state[2] * 0.15)
                    b_cash = b_ch * bit[i] * (1 - b)
                    invest_state[0] = invest_state[0] + b_cash
                    invest_state[2] = invest_state[2] - b_ch

            else:
                # 比特币
                if np.abs(b_k) <= 1:
                    b_trend.append(0)
                    invest_state[2] = invest_state[2]
                elif b_k > 1:
                    if 1 < b_k <= 5:
                        b_trend.append(1)
                        b_ch = math.ceil(invest_state[2] * 0.05)
                    elif 5 < g_k <= 10:
                        b_trend.append(2)
                        b_ch = math.ceil(invest_state[2] * 0.1)
                    else:
                        b_trend.append(3)
                        b_ch = math.ceil(invest_state[2] * 0.15)
                    b_cash = b_ch * bit[i] * (1 - b)
                    if invest_state[0] > b_cash:
                        invest_state[0] = invest_state[0] - b_cash
                        invest_state[2] = invest_state[2] + b_ch
                else:
                    if -5 <= b_k < -1:
                        b_trend.append(-1)
                        b_ch = math.ceil(invest_state[2] * 0.05)
                    elif -10 <= b_k < -5:
                        b_trend.append(-2)
                        b_ch = math.ceil(invest_state[2] * 0.1)
                    else:
                        b_trend.append(-3)
                        b_ch = math.ceil(invest_state[2] * 0.15)
                    b_cash = b_ch * bit[i] * (1 - b)
                    invest_state[0] = invest_state[0] + b_cash
                    invest_state[2] = invest_state[2] - b_ch

            if invest_state[0] >= 200:
                if b_k > 0:
                    b_ch = int(invest_state[0] / (bit[i] * (1 + b)))
                    b_cash = bit[i] * b_ch
                    invest_state[0] = invest_state[0] - b_cash
                    invest_state[2] = invest_state[2] + b_ch

            if invest_state[1]<10:
                if g_k > 0:
                    g_ch = 10
                    g_cash = g_ch*gold[i]*(1+g)
                    if invest_state[0] > g_cash:
                        invest_state[0] = invest_state[0]-g_cash
                        invest_state[1] = invest_state[1]+g_ch

        assets = Asset_State(invest_state, i)
        print('The current investment volume status is: {}, the asset is equal to {} USD '.format(invest_state, assets))

