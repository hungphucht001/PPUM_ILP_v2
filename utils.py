def convert_dict_to_array(dict):
    arr_list_utility = []
    arr_list_utility_label = []
    for row in dict:
        newRow = []
        newLable = []
        for i in row:
            newRow.append(row[i])
            newLable.append(i)
        arr_list_utility.append(newRow)
        arr_list_utility_label.append(newLable)
    return arr_list_utility, arr_list_utility_label[0]

def check_list_in_list(arr1, arr2):
    for i in arr2:
        if i in arr1:
            return True
    return False


def check_list_equal_list(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    else:
        count = 0
        for i in arr2:
            if i in arr1:
                count += 1
        if count == len(arr1):
            return True
        return False


def check_str_in_str(str_1, str_2):
    for i in str_1:
        if i in str_2:
            return True
    return False

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