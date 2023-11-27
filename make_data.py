import pickle
import sys
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


#いくつoutputファイルを読み込むかとalpha値をコマンドライン引数で指定（python3 make_data.py number alpha match border fBorderの形で指定）
def get_params():
    number = int(sys.argv[1])
    alpha = float(sys.argv[2])
    match = int(sys.argv[3])
    border = int(sys.argv[4])
    fBorder = int(sys.argv[5])
    return number, alpha, match, border, fBorder

def get_outputs(number, alpha, match, border):
    data = {}
    for i in range(number):
        #print(i)
        #print("output_seed{0}_alpha{1}_match{2}_border{3}.pkl".format(i + 1, alpha, match, border))
        with open("output_seed{0}_alpha{1}_match{2}_border{3}.pkl".format(i + 1, alpha, match, border), 'rb') as tf:
            output = pickle.load(tf)
            #print(output)
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

def make_data(data, fBorder):
    final_data = {}
    for key, value in data.items():
        if value[0] >= fBorder:
            final_data[key] = value[1] / value[0]
    return final_data


number, alpha, match, border, fBorder = get_params()
data = get_outputs(number, alpha, match, border)
final_data = make_data(data, fBorder)
#print(final_data)
with open("data_seed1to{0}_alpha{1}_match{2}_border{3}_fBorder{4}.pkl".format(number, alpha, match, border, fBorder), 'wb') as tf:
    pickle.dump(final_data, tf)

