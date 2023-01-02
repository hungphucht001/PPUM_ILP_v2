from readData import load_dataset_util
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, LpAffineExpression
# from HUI import HUI, data, D, utility_Dic, utility
from utils import convert_dict_to_array, check_list_in_list, check_list_equal_list, check_str_in_str, compare_array

import time

from HUI import HUIMiner


class PPUM_ILP:
    def __init__(self, data_chess, HUI, M):
        """
            HUI: HUIMiner
            M: min_util
            Is:
            NHI_TB:
            SHI_TB:
        """
        self.M = M
        self.D_ = []
        self.Is = [[1, 2]]
        # self.Is = [[1, 2], [1, 3], [1, 4]]
        self.HUI = HUI
        self.data_chess = data_chess

        # self.D = D
        # self.data = data
        # self.utility = utility
        # self.utility_Dic = utility_Dic
        # self.HUI_TIDs = dict(**self.NHI_TB, ** self.SHI_TB)

    def filter_NHI_and_SHI_to_HUI(self):
        """
            HUI -> SHI_TB and NHI_TB
            SHI_TB = (Is + tid)
            NHI_TB:
                +
                +
                +
        """
        NHI_TB = []
        SHI_TB = []
        for item in self.HUI:
            lable = item[0]
            isIs = False
            for item_Is in self.Is:
                if compare_array(lable, item_Is):

                    SHI_TB.append(item)
                    isIs = True
            if not isIs:
                if len(NHI_TB) == 0:
                    NHI_TB.append(item)
                else:
                    # lọc NHI table ra
                    # for nhi_item in self.NHI_TB:
                    NHI_TB.append(item)
        return NHI_TB, SHI_TB

    def get_tid(self, array):
        result = []
        for item in array:
            result.append(item["tid"])
        return result

    def algorithm(self):
        """
            The PPUM-ILP algorithm
        """
        # Table constructions:
        NHI_TB, SHI_TB = self.filter_NHI_and_SHI_to_HUI()

        # # Preprocessing:
        index = 0
        NHI_TB_Temp = NHI_TB.copy()
        NHI_TB = []
        for ni in NHI_TB_Temp:
            L = []  # Khởi tạo L rỗng
            a = np.array(ni[0])
            c = np.array(self.get_tid(ni[1]))

            for si in SHI_TB:
                b = np.array(si[0])
                d = np.array(self.get_tid(si[1]))
                inter = np.intersect1d(a, b)
                inter2 = np.intersect1d(c, d)
                inter3 = np.setdiff1d(a, b)

                if len(inter) > 0 and len(inter2) > 0:
                    if len(inter3) == 0 and np.array_equal(c, d):
                        break
                    else:
                        NHI_TB.append(ni)
                        break

        NHI_TB_Temp = NHI_TB.copy()
        NHI_TB = []
        for ni in NHI_TB_Temp:
            c = np.array(self.get_tid(ni[1]))
            isDelete = False
            for nj in NHI_TB_Temp:
                inter3 = np.setdiff1d(nj[0], ni[0])
                d = np.array(self.get_tid(nj[1]))
                if not np.array_equal(ni[0], nj[0]) and len(inter3) == 0 and np.array_equal(c, d):
                    isDelete = True
                    break
            if not isDelete:
                NHI_TB.append(ni)

        print("/////////////////////////////")
        print("NHI_TB: ")

        for a in NHI_TB:
            print(a[0])

        #  CSP formulation:
        #  Biến quyết định x, y, z

        deci_variables = {}
        for item in self.Is:
            for X in item:
                dict_aa = {}
                dict_aa[X] = {i: LpVariable(name=f"{X}_{i}", lowBound=1) for i in range(1, len(self.data_chess) + 1)}
                deci_variables.update(dict_aa)

        # Khởi tạo model
        model = LpProblem(name="resource-allocation-ILP", sense=LpMinimize)

        # model SHI_TB
        sum_AB = 0

        # for item in self.Is:
        #     sum = 0
            # arr = self.arr_Si(self.arr_sum(item), item, deci_variables)
        #     for i in arr:
        #         sum += utility_Dic[i] * arr[i]
        #         sum_AB += arr[i]
        #     model += ((sum) <= self.M - 1, item)

        # Solve the optimization problem
        # model.solve()

    def run(self):
        self.algorithm()

def TWU_item(item, dataset, tran_util, data_util):
    TWU = 0
    array_util = []
    for i in range(len(dataset)):
        try:
            index = dataset[i].index(int(item))
        except:
            index = -1
        if index >= 0:
            array_util.append(data_util[i][index])
        if int(item) in dataset[i]:
            TWU += tran_util[i]
    gcd = np.gcd.reduce(array_util)  # Ước chung lớn nhất
    return TWU, gcd

if __name__ == "__main__":
    start = time.time()
    print("Đọc data từ file txt.")
    data_chess, sum_util, data_util, item_list = load_dataset_util('chess_quan.txt')

    # print('Dataset: ')
    # print(data_chess)
    # print('data_chess data')
    # print(data_util)
    # print('Item list')
    # print(item_list)

    print("Đọc data xong.")

    delta = 0.25
    min_utility = sum(sum_util) * delta
    # min_utility = 80
    print('====================')
    print('TWU từng item (>= minutil)')
    twu_name = []
    twu_value = []
    external_utility = {}  # table 02

    for item in item_list:
        twu, gcd = TWU_item(item, data_chess, sum_util, data_util)
        if twu >= min_utility:
            temp = {int(item): gcd}
            external_utility.update(temp)
            twu_name.append(int(item))
            twu_value.append(twu)

    len_data = len(data_chess)

    data_chess_copy = []
    data_util_copy = []

    """
        Loại bỏ từng item có TWU < min-utility)
    """
    for i in range(len(data_chess)):
        arr_data = []
        arr_util = []
        for j in range(len(data_chess[i])):
            if data_chess[i][j] in twu_name:
                arr_data.append(data_chess[i][j])
                arr_util.append(data_util[i][j])
        data_chess_copy.append(arr_data)
        data_util_copy.append(arr_util)

    print("Min utility: ", min_utility)

    print("Khai thác tập hữu ích cao.")
    hui_miner = HUIMiner(data_chess_copy, data_util_copy, min_utility, twu_name)
    hui = hui_miner.run()
    print("Khai thác xong.")

    print("Sử dụng ILP:")
    PPUM_ILP(data_chess_copy, hui, min_utility).run()
    print('Tổng thời gian: %s giây' % (time.time() - start))
