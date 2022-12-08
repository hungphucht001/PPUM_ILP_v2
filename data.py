from datetime import date
from math import exp
import pandas as pd
import csv
#from itertools import zip_longest
import copy
import json
import pickle
import os
import random
import time

# Đọc dataset dạng data : sum util : item util
def load_dataset_util(filename):
    with open(filename) as f:
        lines = f.readlines()

    data = []
    data_util = []
    sum_util = []
    item_list = []
    for line in lines:
        part = line.split(':')
        
        # Tách phần đầu
        items = part[0].split()
        tran = []
        for item in items:
            tran.append(item)
            if item not in item_list:
                item_list.append(item)
        data.append(tran)
        
        # Tách phần 2
        sum_util.append(int(part[1]))

        # Tách phần 3
        items = part[2].split()
        tran_util = []
        for item in items:
            tran_util.append(int(item))
        data_util.append(tran_util)
    
    # Kết quả: 
    # data: list of list
    # sum_util: list
    # data_util: list of list
    # item_list: list
    return data, sum_util, data_util, sorted(item_list)

##Read csv
def load_dataset(filename):
    "Load tập dữ liệu mẫu. Định dạng: List of lists"
    
    dataset = pd.read_csv(filename, header = None, dtype=str)
    transactions = []
    for i in range(0,len(dataset.values)):
        tran = list(map(str, dataset.values[i].tolist()))
        #while(tran[len(tran) - 1] == 'nan'):
        while('nan' in tran):
            tran.remove('nan')
        transactions.append(tran)
    return transactions

def write_dataset(filename, dataset):
    "Ghi dataset vào file csv. dataset ở dạng list of list"
    
    my_df = pd.DataFrame(dataset)
    my_df.to_csv(filename, index=False, header=False)
    return

def convert(list):   
    for item in list:
        int(item)
    return item

#hàm dictionary các item trong bảng profit
def dic(name,profit_table):
    #name: tên của item truyền vào
    item_dict = {}
    #[int(item) for item in item[1:]]
    for item in profit_table:
        item_dict[item[0]] = convert(item[1:])
    return (item_dict[name])

# def util_item_in_tran(item, tran, profit_table):

#Hàm tính TU của từng trans
# def TUofTrans(dataset,profit):
#     res = list()
#     for i in range(len(dataset)):
#         sumitem=0
#         for j in range(len(dataset[i])):
#             s=dataset[i][j].split(':')        
#             sumitem=sumitem + (int(s[1]) * int(dic(s[0],profit)))
#         res.append(sumitem) 
#     return res

# def TWU_item(profit_item,TUa,item):
#    # for k in range(len(profit)):
#     TWU=0  
#     for i in range(len(item)):             
#         for j in range(len(item[i])):
#             s=item[i][j].split(':') 
#             fist_char=s[0]
#             if(fist_char== profit_item):
#                 TWU=TWU + TUa[i] 
#     return TWU

#Hàm tính twu của từng item khác nhau
# def TWU_item(item, TUa, dataset):
#     TWU = 0  
#     for i in range(len(dataset)):
#         for it in dataset[i]:
#             s = it.split(':') 
#             if(s[0] == item):
#                 TWU = TWU + TUa[i]
#     return TWU

def TWU_item(item, dataset, tran_util):
    TWU = 0  
    for i in range(len(dataset)):
        if item in dataset[i]:
            TWU += tran_util[i]

    return TWU

# def TWUofQuality_value(profit_table, minutility, TUa, dataset):
#     T = []
#     for items in profit_table:
#         twu_item = TWU_item(items[0], TUa, dataset)
#         if (twu_item > minutility):
#             T.append(twu_item)             
#     return T      

# def TWUofQuality(profit_table, minutility, TUa, dataset):
#     T = []
#     for items in profit_table:
#         twu_item = TWU_item(items[0], TUa, dataset)
#         if (twu_item > minutility):
#             T.append(items[0])             
#     return T

#Hàm lấy name và values của các item có twu > minutility
# def TWUofQuality(profit_table, minutility, TUa, dataset):
#     #TUa: TU của từng trans
#     name = []
#     value = []
#     for items in profit_table:
#         twu_item = TWU_item(items[0], TUa, dataset)
#         if (twu_item > minutility):
#             name.append(items[0])
#             value.append(twu_item)         
#     return name, value

#hàm khởi tạo bảng toàn giá trị 0
# def Partical(n,v):
#     list_v=[]
#     for i in range(n):
#         list_r=[]
#         for j in range(len(v)):
#             r=0
#             list_r.append(r)
#         list_v.append(list_r)
#     return list_v

#Hàm random partical theo phương thưc roulette
# '''def random_partical(numberpartical,v_value):
#     #par:bảng partical toàn giá trị 0
#     #v_value:list các giá trị sau khi tinh twu của từng item 
#     Par = [[0] * len(v_value)] * numberpartical     
#     for i in range(len(Par)):
#         for j in range(len(Par[i])):
#             rd_partical= random.randint(1,sum(v_value))
#             value=0
#             m=0
#             for k in range(-1,len(v_value)-1):
#                 value=value+v_value[k+1]
#                 if(rd_partical<value):
#                     Par[i][m]=1             
#                     break                                                          
#                 else:                   
#                     m=m+1                                    
#     return Par'''

def random_partical(number_particle, v_value):
    tong = sum(v_value)
    tempSum = 0
    xac_suat = []
    for i in range(len(v_value)):
        tempSum += v_value[i]
        xac_suat.append(tempSum / tong)
    print(xac_suat)
    # xac_suat = [i / tong for i in v_value]
    # he_so_chuan_hoa = 0.2 / max(xac_suat)
    # chuan_hoa = [he_so_chuan_hoa*i for i in xac_suat]
    
    Par = []
    # for i in range(number_particle):
    #     lst = [] 
    #     for j in range(len(v_value)):
    #         rd = random.random()
    #         x = 0
    #         if (rd < chuan_hoa[j]):
    #             x = 1
    #         lst.append(x)
    #     Par.append(lst)

    for i in range(number_particle):
        lst = [0] * len(v_value) 
        k = int(random.random() * len(v_value))
        j = 0
        while j < k :
            # roulette select
            index = 0
            rd = random.random()
            for x in range(len(xac_suat)):
                if x == 0:
                    if (rd <= xac_suat[0]):
                        index = 0
                        break
                elif (rd > xac_suat[x-1]) and (rd <= xac_suat[x]):
                    index = x
                    break
            #
            if lst[index] == 0:
                j += 1
                lst[index] = 1
        Par.append(lst)

    return Par

# '''def Best(rd_P,v):
#     best=[]
#     for i in range(len(rd_P)):
#         b=[]
#         for j in range(len(rd_P[i])):
#             if(rd_P[i][j]==1): 
#                 if(j== x for x in range(10)):
#                     j=v[j]
#                 b.append(str(j))
#         best.append(b)
#     return best'''

#hàm chuyển đổi trans thành name trong bảng v
def ConverToChar(trans, v):
    #trans: truyền vao 1 trans
    #v: lấy name của item mà có twu > minutility  
    best=[]
    for k in range(len(trans)):
        if(trans[k]==1): 
            if(k == x for x in range(10)):
                k = v[k]
            best.append(str(k))
    return best

def ConverToItemset(particle, v_name):
    # particle: 1 hạt dưới dạng [0, 1, ...]
    # v_name : tên của các item mà có twu > minutility  
    best = []
    for k in range(len(particle)):
        if(particle[k] == 1): 
            best.append(v_name[k])
    return best

#Hàm lấy value(Tmp_item trước dấu (:)) (Tmp_value sau dấu (:)) của item trong bảng dataset
def convertItemToChar(dataset):
    Tmp_item=[]
    Tmp_value=[]
    for i in range(len(dataset)):
        tmp_item=[]   
        tmp_value=[]                   
        for j in range(len(dataset[i])):
            s=dataset[i][j].split(':') 
            tmp_item.append(s[0])
            tmp_value.append(s[1])
        Tmp_item.append(tmp_item)
        Tmp_value.append(tmp_value)
    return Tmp_item,Tmp_value

# ConvertItem=convertItemToChar()


'''def convertValueToChar(dataset):
    Tmp_item=[]
    Tmp_value=[]
    for i in range(len(dataset)):
        tmp=[]                      
        for j in range(len(dataset[i])):
            s=dataset[i][j].split(':') 
            tmp.append(s[1])
            tmp.append(s[0])
        Tmp_item.append(tmp)
    return Tmp_item'''
# ConvertValue=convertValueToChar()

'''def Cal_u(pBest):   
    List_pBest=[]
    for n in range(len(pBest)):
        CTC=ConverToChar(pBest[n])
        ValueBest=0
        for i in range(len(ConvertItem)):
            if(all(x in ConvertItem[i] for x in CTC)):
                for m in range(len(CTC)):                   
                    id=ConvertItem[i].index(CTC[m])
                    ValueBest=ValueBest+(int(dic(CTC[m]))* int(ConvertValue[i][id]))                    
        print(n)
        List_pBest.append(ValueBest)
    return List_pBest'''

# Tính utility của 1 itemset theo định nghĩa 3
def Cal_uItemset(itemset, dataset, data_util):
    # itemset: itemset cần tính util
    # dataset: tập dữ liệu 
    # data_util: util của các item trong tập dữ liệu 
    util = 0
    for i in range(len(dataset)):
        if set(itemset) <= set(dataset[i]):
            for item in itemset:
                for j in range(len(dataset[i])):
                    if item == dataset[i][j]:
                        util += data_util[i][j]
                        break
    return util

#Random vận tốc tỏng khoảng (0,1)
def Random_V(numberpartical, v_value):
    list_v=[]
    for i in range(numberpartical):
        list_r=[]
        for j in range(len(v_value)):
            r=random.random()
            list_r.append(round(r, 2))
        list_v.append(list_r)
    return list_v

# def gBest(pBest, ConvertItem, dataset, profit_table, v):
#     #ConvertItem: lấy name của item trong bảng dataset
#     #v:lấy name của item mà có twu > minutility
#     #pBest: bảng pbest
#     list_pbest=[]
#     for i in range(len(pBest)):
#         t=Cal_uItem(pBest[i],ConvertItem,dataset,profit_table,v)
#         list_pbest.append(t)
#     #Tìm giá trị lớn nhất trong bảng pbest để lấy làm gBest
#     gbest_max=max(list_pbest)
#     gbest_index=list_pbest.index(gbest_max)
#     return pBest[gbest_index]

# Tìm tốt nhất trong các pBest
def Best(pBest, dataset, data_util, v_name):
    # pBest: bảng pbest
    # dataset: tập dữ liệu
    # data_util: util của các item
    # v_name: tên của bảng 1-itemset
    best = pBest[0]
    util_max = Cal_uItemset(ConverToItemset(best, v_name), dataset, data_util)
    for par in pBest:
        itemset = ConverToItemset(par, v_name)
        util = Cal_uItemset(itemset, dataset, data_util)
        if util > util_max :
            best = par
            util_max = util
    
    return best

# Update vận tốc ở thời gian t
def Update_velocities(velocities, pBest, p, gBest, w, c1, c2):
    # velocities: vận tốc của các hạt ở thời điểm trước
    # pBest: bảng pBest
    # p : các hạt ở thời điểm trước
    # gBest: global best
    # ver: bảng vận tốc thời gian trước đó

    V = []
    for i in range(len(velocities)):
        vi=[]
        r1 = random.random()
        r2 = random.random()
        for j in range(len(velocities[i])):
            velocity = velocities[i][j]
            velocity += c1 * r1 * (pBest[i][j] -p[i][j]) 
            velocity += c2 * r2 * (gBest[j]- p[i][j]) 
            if (velocity < -2):
                velocity = -2.0
            elif (velocity > 2):
                velocity = 2.0
            vi.append(round(velocity, 2))
        V.append(vi)
    return V

#update partical sau khi update vận tốc
def Update_partical(velocities):
    #velocities:bảng vận tốc sau khi được cập nhật
    p_up=[]
    for i in range(len(velocities)):
        pi=[]
        for j in range(len(velocities[i])):
            temp = random.random()
            t = 1 / (1 + exp(-velocities[i][j]))
            if (temp < t):
                partical = 1
            else:
                partical = 0
            pi.append(partical)
        p_up.append(pi)
    return p_up

# Cập nhật bảng pBest
def Update_pBest(particles, pBest, dataset, data_util, v_name):
    # particles: bảng partice mới
    # pBest: pBest hiện tại
    new_pBest = []
    for i in range(len(pBest)):
        # Tính util của 2 thằng
        pBest_itemset = ConverToItemset(pBest[i], v_name)
        pBest_util = Cal_uItemset(pBest_itemset, dataset, data_util)
        par_itemset = ConverToItemset(particles[i], v_name)
        par_util = Cal_uItemset(par_itemset, dataset, data_util)

        # Thằng nào lớn thì lấy
        if (pBest_util < par_util) :
            new_pBest.append(particles[i])
        else :
            new_pBest.append(pBest[i])
    return new_pBest

#Hàm kiểm tra xem hui đó đã đươc lưu trữ chưa nếu đã có rồi thì return true    
# def Find_Hui(hui, xbest):
#     #hui:  giá trị hui có fitness > minutility
#     #xbest: list lưu trữ hui
#     if (xbest == []):
#         return False
#     for m in range(len(xbest)):
#         if( xbest[m] == hui):
#             return True
#     return False

# Kiểm tra itemset đã có trong data chưa
def kiem_tra_ton_tai(itemset, data):
    for tran in data:
        if set(tran) == set(itemset):
            return True
    return False

def Run():
    # Các thông số ban đầu
    w = 0.9
    c1 = 2
    c2 = 2
    delta = 0.25
    numberpartical = 20
    so_lan_lap = 10000

    # Đọc dữ liệu
    # dataset = load_dataset('Random_Quanlity.csv')
    # profit_data = load_dataset('Random_Profit.csv')

    # dataset = load_dataset('item.csv')
    # profit_data = load_dataset('profit.csv')

    data, tran_util, data_util, item_list = load_dataset_util('chess_quan.txt')

    # TUa = TUofTrans(dataset, profit_data)

    print('Dataset: ')
    print(data)
    print('Util data')
    print(data_util)
    print('Item list')
    print(item_list)
        
    # Tính minutility
    minutility = sum(tran_util)*delta 
    print('min utility: ', minutility)
    
    print('====================')
    print('TWU từng item (>= minutil)')
    v_name = []
    v_value = []
    for item in item_list:
        twu = TWU_item(item, data, tran_util)
        if twu >= minutility:
            v_name.append(item)
            v_value.append(twu)
            print(item, ': ', twu)

    # Các hạt khởi tạo ban đầu
    particles = random_partical(numberpartical, v_value)
    velocities = Random_V(numberpartical, v_value)
    pBest = copy.deepcopy(particles)
    gBest = Best(pBest, data, data_util, v_name)
    
    print('============================')
    # .....
    get_Hui = []
    for particle in pBest:
        itemset = ConverToItemset(particle, v_name)
        util = Cal_uItemset(itemset, data, data_util)
        # print('Hạt: ', particle, ' - Util: ', util)
        if (util >= minutility):
            print('HUI: Hạt: ', particle, ' - Util: ', util)
            if (kiem_tra_ton_tai(itemset, get_Hui)):
                continue
            else:
                get_Hui.append(itemset)
    # print('pause')
    # input()
    # Vòng lặp chính
    for t in range(1, so_lan_lap):
        print('Lan lap: ', t)
        velocities = Update_velocities(velocities, pBest, particles, gBest, w, c1, c2)
        particles = Update_partical(velocities)
        
        # Kiểm tra HUI trước rồi mới cập nhật pbest gbest
        for particle in particles:
            itemset = ConverToItemset(particle, v_name)
            util = Cal_uItemset(itemset, data, data_util)
            # print('Hạt: ', particle, ' - Util: ', util)
            if (util >= minutility):
                print('HUI: Hạt: ', particle, ' - Util: ', util)
                if (kiem_tra_ton_tai(itemset, get_Hui)):
                    continue
                else:
                    get_Hui.append(itemset)
        
        # cập nhật bảng pBest
        pBest = Update_pBest(particles, pBest, data, data_util, v_name)
        # Cập nhật gBest
        gBest_candidate = Best(pBest, data, data_util, v_name)
        if (Cal_uItemset(ConverToItemset(gBest_candidate, v_name), data, data_util) > Cal_uItemset(ConverToItemset(gBest, v_name), data, data_util)) :
            gBest = gBest_candidate         
    return get_Hui

if __name__ == "__main__":
    start = time.time()
    write_dataset('HUIm.csv', Run())
    print('Tổng thời gian: %s giây' % (time.time() - start))