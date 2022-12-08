

def compare_array(array_one, array_two):
    """
        compare 2 arrays return bool
    """
    if len(array_one) == len(array_two):
        count = 0
        for i in array_one:
            for j in array_two:
                if i == j:
                    count = count + 1
        if count == len(array_one):
            return True
        else:
            return False
    else:
        return False


def get_common_element(array_one, array_two):
    """
        Get common element from 2 arrays
    """
    count = []
    for i in array_one:
        for j in array_two:
            if i == j:
                count.append(i)
    return count


def get_lables(utility_list):
    """
        select labels from a list
    """
    items = []
    for row in utility_list:
        items = items + row["item"]
    labels_temp = set(items)
    labels = []
    for item in labels_temp:
        labels.append([item])
    return labels


class HUIMiner:
    def __init__(self, data_chess, data_util, min_util):
        self.data_chess = data_chess
        self.data_util = data_util
        self.min_util = min_util
        self.get_list_item_set_result = self.get_list_item_set
        self.utility_list_result = self.utility_list(self.get_list_item_set_result)
    @property
    def get_list_item_set(self):
        """
            list item set single
        """
        data_chess, data_util = self.reverse_data_chess_and_data_util(self.data_chess, self.data_util)
        tid = 1
        arr = []
        for row in data_chess:
            Ru = 0
            n = 0
            for item in row:
                u = data_util[tid - 1][n]
                arr.append({"tid": tid, "item": [item], "Ru": Ru, "u": u})
                Ru = Ru + u
                n = n + 1
            tid = tid + 1
        return arr

    @staticmethod
    def reverse_data_chess_and_data_util(data_chess, data_util):
        """
            reverse data chess
            reverse data util
        """
        new_data_chess = []
        for row in data_chess:
            numpy_list = row[::-1]
            new_data_chess.append(numpy_list)

        new_data_util = []
        for row in data_util:
            numpy_list = row[::-1]
            new_data_util.append(numpy_list)

        return new_data_chess, new_data_util

    @staticmethod
    def utility_list(utility_list):
        lables = get_lables(utility_list)
        arr_all = []
        for item in lables:
            arr_temp = []
            for row in utility_list:
                result = set(row["item"]) & set(item)
                if result:
                    arr_temp.append(row)
            arr = [item, arr_temp]
            arr_all.append(arr)
        return arr_all

    @staticmethod
    def construct(up, upx, upy):
        pxy = []
        arr = []
        for ex in upx[1]:
            for ey in upy[1]:
                if ex["tid"] == ey["tid"]:
                    items_dic = {}
                    arrLable = list(ex['item']) + list(ey['item'])
                    s = set(arrLable)
                    unique_l = list(s)
                    if up:
                        for row in up[1]:
                            if row["tid"] == ey["tid"]:
                                items_dic = {
                                    "tid": ex["tid"],
                                    "item": unique_l,
                                    "Ru": ey["Ru"],
                                    "u": (ex["u"] + ey["u"] - row["u"])
                                }
                    else:
                        items_dic = {
                            "tid": ex["tid"],
                            "item": unique_l,
                            "Ru": ey["Ru"],
                            "u": (ex["u"] + ey["u"])
                        }

                    arr.append(items_dic)
                    pxy.append(unique_l)
                    pxy.append(arr)
        return pxy

    def hui_miner(self, pUL, uls):
        """
            pUL: the utility-list of item-set P, initially empty;
            uls: the set of utility-lists
        """
        for i in range(0, len(uls)):
            countU = 0
            countRu = 0
            X = uls[i]
            if uls[i]:
                for item in X[1]:
                    countU += item["u"]
                    countRu += item["Ru"]
                if countU >= self.min_util:
                    print(X, "\n")
                # if (countU + countRu) >= self.min_util:
                exUls = []
                for j in range(i + 1, len(uls)):
                    result = self.construct(pUL, X, uls[j])
                    if result:
                        exUls.append(result)
            self.hui_miner(X, exUls)

    def run(self):
        self.hui_miner([], self.utility_list_result)
