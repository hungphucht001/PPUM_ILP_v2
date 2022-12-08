from readData import data as data_chess, sum_util, data_util, item_list
import time

from HUI import HUIMiner

if __name__ == "__main__":
    start = time.time()
    delta = 0.25
    min_util = 30
    print(min_util)
    hui = HUIMiner(data_chess, data_util, min_util)
    hui.run()
    print('Tổng thời gian: %s giây' % (time.time() - start))
