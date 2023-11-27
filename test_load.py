import pickle
import sys
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("test_output.pkl", 'rb') as tf:
    output = pickle.load(tf)
    print(output)

'''
def get_outputs(number, alpha, match, border):
    data = {}
    for i in range(number):
        print(i)
        with open("output_seed{0}_alpha{1}_match{2}_border{3}.pkl".format(i + 1, alpha, match, border), 'rb') as tf:
            output = pickle.load(tf)
            print(output)
            for key, value in output.items():
                if key not in data:
                    data[key] = value
                else:
                    v_0, v_1 = value[0], value[1]
                    a = data[key]
                    a[0] += v_0
                    a[1] += v_1
                    data[key] = [a[0], a[1]]
    return data
'''