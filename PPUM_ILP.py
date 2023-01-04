from readData import load_dataset_util
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, LpAffineExpression
# from HUI import HUI, data, D, utility_Dic, utility
from utils import convert_dict_to_array, check_list_in_list, check_list_equal_list, check_str_in_str, compare_array

import time

from HUI import HUIMiner


class PPUM_ILP:
    def __init__(self, data_chess, HUI, min_utility, external_utility):
        """
            HUI: HUIMiner
            M: min_util
            Is:
            NHI_TB:
            SHI_TB:
        """
        self.min_utility = min_utility
        self.D_ = []
        self.Is = [[1, 2]]
        # self.Is = [[1, 2], [1, 3], [1, 4]]
        self.HUI = HUI
        self.data_chess = data_chess
        self.external_utility = external_utility

        # self.D = D
        # self.data = data
        # self.utility = utility
        # self.utility_Dic = utility_Dic
        # self.HUI_TIDs = dict(**self.NHI_TB, ** self.SHI_TB)

    def filter_NHI_and_SHI_to_HUI(self):
        """
            HUI -> SHI_TB and NHI_TB
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

    def arr_sum(self, item):
        """

        """
        arr_sum = {}
        for X in item:
            dict_aa = {}
            dict_aa[X] = LpAffineExpression()
            arr_sum.update(dict_aa)
        return arr_sum

    def index_TIDs(self, i):
        for item in self.HUI:
            if item[0] == i:
                arr = []
                for row in item[1]:
                    arr.append(row['tid'])
                return arr
                break

    def arr_Si(self, arr, temp, deci_variables):
        """
            {'A': 1*A1 + 1*A5 + 1*A7 + 0, 'B': 1*B1 + 1*B5 + 1*B7 + 0}
            {'A': 1*A2 + 1*A8 + 1*A9 + 0, 'C': 1*C2 + 1*C8 + 1*C9 + 0}
            {'A': 1*A1 + 1*A5 + 1*A8 + 0, 'D': 1*D1 + 1*D5 + 1*D8 + 0}
        """
        for item_vb in deci_variables:
            for item in arr:
                if (item == item_vb):
                    for i in self.Is:
                        if temp == i:
                            for j in self.index_TIDs(i):
                                arr[item] += deci_variables[item][j + 1]
        return arr

    def check_nhi_in_shi(self, item):
        """
            kiểm tra Nhi có trong Shi hay không
        """
        strItem = []
        for a in self.Is:
            for i in a:
                for j in item:
                    if j not in strItem and (i == j):
                        strItem.append(j)
        return strItem

    def right_side(self, item, arr):
        """
            Tính vế phải
        """
        sum_ = 0
        temp = self.check_nhi_in_shi(item)
        for x in arr:
            if item in self.HUI_TIDs and self.HUI_TIDs[item][x - 1] != 0:
                sum_ += self.HUI_TIDs[temp][x - 1]
        return (self.HUI[item] - sum_)

    def arr_X(self, TIDs, item):
        arr = []
        for X in self.Is:
            for i in self.index_TIDs(X):
                for j in range(len(TIDs[item])):
                    if i == j and TIDs[item][j] != 0:
                        arr.append(i + 1)
        return arr

    def algorithm(self):
        """
            The PPUM-ILP algorithm
        """
        # Table constructions:
        NHI_TB, SHI_TB = self.filter_NHI_and_SHI_to_HUI()

        # Preprocessing:
        NHI_TB_Temp = NHI_TB.copy()
        NHI_TB = []
        for ni in NHI_TB_Temp:

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

        """
            CSP formulation:
            Biến quyết định x, y, z
        """
        deci_variables = {}
        for item_is in self.Is:
            for X in item_is:
                temp = {X: {i: LpVariable(name=f"{X}_{i}", lowBound=1) for i in range(1, len(self.data_chess) + 1)}}
                deci_variables.update(temp)

        """
            Khởi tạo model:
            model : Lable : 5 * A1 + 5 * A5 + 5 * A7 + 3 * B1 <= min_utility
        """
        model = LpProblem(name="resource-allocation-ILP", sense=LpMinimize)

        """
            model SHI_TB:
            AB ∶ 5(u11 + u51 + u71) + 3(u12 + u52 + u72) < 80
        """
        sum_AB = 0
        for item_is in self.Is:
            sum = 0
            result = self.arr_Si(self.arr_sum(item_is), item_is, deci_variables)
            for item_lable in result:
                sum += external_utility[item_lable] * result[item_lable]
                sum_AB += result[item_lable]
            model += (sum <= self.min_utility - 1, item_is)
        print("model", model)

        """
            model NHI_TB:
            A ∶ 5(u11 + u51 + u71) ≥ 80 − 70,
            AD ∶ 5(u11 + u51) ≥ 80 − 75,
            BD ∶ 3(u12 + u52) ≥ 80 − 42,
            ABDE ∶ 5u11 + 3u12 ≥ 80 − 34
        """
        for item in NHI_TB:
            X = self.check_nhi_in_shi(item[0])
            sum_item = 0
            # arr = self.arr_X(NHI_TB, item)
            # arr = list(set(arr))
            # for i in X:
            #     util_ = external_utility[i]
            #     sum_item_2 = 0
            #     for j in arr:
            #         for k in deci_variables:
            #             if (k == i):
            #                 sum_item_2 += deci_variables[k][j]
            #     sum_item += util_ * sum_item_2
            # model += ((sum_item) >= self.M - self.VP(item, arr), item)

        # Solve the optimization problem
        # model.solve()

    def run(self):
        self.algorithm()


def TWU_item(item, dataset, tran_util, data_util):
    """
        Calc item TWU
        Calc item external utility
    """
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
    data_chess, sum_util, data_util, item_list = load_dataset_util('test.txt')

    # print('Dataset: ')
    # print(data_chess)
    # print('data_chess data')
    # print(data_util)
    # print('Item list')
    # print(item_list)

    print("Đọc data xong.")

    delta = 0.25
    min_utility = sum(sum_util) * delta
    min_utility = 80
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

    print("External Utility:")
    print(external_utility)

    len_data = len(data_chess)
    data_chess_copy = []
    data_util_copy = []

    """
        Loại bỏ từng item có TWU < min-utility)
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

    print("PPUM_ILP:")
    PPUM_ILP(data_chess_copy, hui, min_utility, external_utility).run()
    print('Tổng thời gian: %s giây' % (time.time() - start))
