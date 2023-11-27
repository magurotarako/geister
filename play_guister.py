'''
得た辞書データをもとにゲームをプレイできるようにする

「盤面が与えられたとき、次の盤面の候補を全て表し、
その候補全てに対して辞書データから評価値を持ってくる
辞書データにない盤面に関しては、全盤面の平均値を適用する
その後、重みをつけてランダムに盤面を選択する」

上記のことができるようになれば、
最初の盤面生成、手番ごとの盤面の入れ替えと組み合わせることによって、
AI同士でのゲームプレイを行うことができる
仮に片方を辞書データを使用したAI、もう片方を全選択肢からランダムに盤面を選択するAI
とすれば、どちらの方が勝率が高くなるかなどを調べることができる

↓辞書データ例 (180桁のone-hot vector表現の数字の「文字列」に対し、評価値が対応)
{'001001000000100100000010010000000010010000100001000010000100001000010000100001000100000100001000010000100010000010000100001000010000001001000001000100001000010000001001000010000001': 0.786101455202694}

'''
from statistics import mean
import copy
import random
import numpy as np
import sys
import re
import pickle
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper





#python3 play_guister.py data_seed1to{0}_alpha{1}_match{2}_border{3}_fBorder{4}.pklの形で実行
def load_data_and_average():
    #data_seed1to{0}_alpha{1}_match{2}_border{3}_fBorder{4}.pklが辞書データ
    data_file_name = sys.argv[1]
    with open("{0}".format(data_file_name), 'rb') as tf:
        data = pickle.load(tf) 
        if len(data) == 0:
            print("データが一つも残っていません")
            average = 0
        else:
            average = mean(data.values())
    return data, average


gravity = 10
data, average = load_data_and_average()


def make_board():
  board = []
  a = [-1, -1, -1, -1, -2, -2, -2, -2]
  random.shuffle(a)
  b = [a[0], a[1], a[2], a[3]]
  c = [a[4], a[5], a[6], a[7]]
  board_1 = [0] + b + [0]
  board_2 = [0] + c + [0]
  board_3, board_4 = [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]
  d = [1, 1, 1, 1, 2, 2, 2, 2]
  random.shuffle(d)
  e = [d[0], d[1], d[2], d[3]]
  f = [d[4], d[5], d[6], d[7]]
  board_5 = [0] + e + [0]
  board_6 = [0] + f + [0]
  board.append(board_1)
  board.append(board_2)
  board.append(board_3)
  board.append(board_4)
  board.append(board_5)
  board.append(board_6)
  return np.array(board)

#次の盤面の候補を羅列
def make_my_next_board_list(board):
  myghosts = find_myghosts(board)
  next_board_list = move(myghosts, board)
  return next_board_list

#自分のゴーストがどこにいるか
def find_myghosts(board):
  myghosts = []
  for i in range(6):
    for j in range(6):
      if board[i][j] in (1, 2):
        myghosts.append([i, j])
  return myghosts

def move(myghosts, board):
  next_board_list = []
  for ghost in myghosts:
    i, j = ghost
    for k in range(4):
      next_board = np.copy(board)
      if k == 0:
        can = move_up(ghost, myghosts, board)
        if can == True:
          next_board[i - 1][j] = next_board[i][j]
          next_board[i][j] = 0
          next_board_list.append(next_board)
      elif k == 1:
        can = move_down(ghost, myghosts)
        if can == True:
          next_board[i + 1][j] = next_board[i][j]
          next_board[i][j] = 0
          next_board_list.append(next_board)
      elif k == 2:
        can = move_left(ghost, myghosts)
        if can == True:
          next_board[i][j - 1] = next_board[i][j]
          next_board[i][j] = 0
          next_board_list.append(next_board)
      else:
        can = move_right(ghost, myghosts)
        if can == True:
          next_board[i][j + 1] = next_board[i][j]
          next_board[i][j] = 0
          next_board_list.append(next_board)
  return next_board_list

def move_up(ghost, myghosts, board):
  i, j = ghost
  if i == 0 or [i - 1, j] in myghosts:
    can = False
  else:
    can = True
  return can

def move_down(ghost, myghosts):
  i, j = ghost
  if i == 5 or [i + 1, j] in myghosts:
    can = False
  else:
    can = True
  return can

def move_left(ghost, myghosts):
  i, j = ghost
  if j == 0 or [i, j - 1] in myghosts:
    can = False
  else:
    can = True
  return can

def move_right(ghost, myghosts):
  i, j = ghost
  if j == 5 or [i, j + 1] in myghosts:
    can = False
  else:
    can = True
  return can

def make_one_hot(board):
    #print(board)
    one_hot = ""
    for i in range(6):
        for j in range(6):
            if board[i][j] == -2:
                one_hot += "10000"
            elif board[i][j] == -1:
                one_hot += "01000"
            elif board[i][j] == 0:
                one_hot += "00100"
            elif board[i][j] == 1:
                one_hot += "00010"
            else:
                one_hot += "00001"
    return one_hot

#盤面をひっくり返す
def turn_switch(next_board):
  change = np.copy(next_board)
  change_2 = np.reshape(change, (1, 36))
  change_2_reverse = np.array(change_2[0][::-1])
  change_board = np.reshape(change_2_reverse, (6, 6))
  change_board *= -1
  return change_board

#ゴーストがいるか、すなわち決着がついたか
def count_ghosts(board):
  if np.any(board == -1) == False:
    #このとき、相手側の青ゴーストがいなくなった
    return 1
  elif np.any(board == -2) == False:
    #このとき、相手側の赤ゴーストがいなくなった
    return 2
  else:
    #特に変化なし
    return 0

#学習AIの行動
def next_choice_ai(next_board_list):
    evaluate_list = []
    for board in next_board_list:
        #次の候補盤面を全てone-hot vector表現にする
        one_hot = make_one_hot(board)
        #データ内にあればその評価値を、無ければデータにある全盤面の評価値の平均で代用
        if one_hot in data:
            evaluate_list.append(data[one_hot])
        else:
            evaluate_list.append(average)
    evaluate_array = np.array(evaluate_list)
    #weightsを重みとして1つ値を選んでくる(random.choices()を使うと、重みでk回選び、長さkのリストとして出るのでk=1かつ[0]が必要)
    exp_weights = np.exp(evaluate_array * gravity)
    next_board = random.choices(next_board_list, k = 1, weights = exp_weights)[0]
    return next_board


def choice_board(next_board_list, turn, mode):
    if (turn % 2 == 1 and mode == 0) or (turn % 2 == 0 and mode == 1):
        #この場合、学習AIの行動ターン
        next_board = next_choice_ai(next_board_list)
    else:
        #この場合、ランダムAIの行動ターン
        L = len(next_board_list)
        choice = random.randint(0, L - 1)
        next_board = next_board_list[choice]
    return next_board


def game(times, mode):
  turn_list, reason_list, log_list = [], [], []
  for _ in range(times):
    log = []
    board = make_board()
    log.append(board)
    turn = 1
    while True:

      if turn % 2 == 1: #先手のターン
        if board[0][0] == 1 or board[0][5] == 1:
            #この時点でのboard = 決着ボード（1手前の後手のターン終了時点で勝ち確定済み）
            reason = 3
            turn_list.append(turn - 1)
            reason_list.append(reason)
            log_list.append(log)
            break
        
        #まだ結果が定まっていないため次の行動選択
        next_board_list = make_my_next_board_list(board)
        next_board = choice_board(next_board_list, turn, mode)
        log.append(next_board)

        #行動選択後、盤面を見て決着がついたかを判断
        if count_ghosts(next_board) == 1:
            #この時点でのnext_board = 決着ボード（先手のターン終了時に勝ち確定）
            reason = 1
            turn_list.append(turn)
            reason_list.append(reason)
            log_list.append(log)
            break
        elif count_ghosts(next_board) == 2:
            #この時点でのnext_board = 決着ボード（先手のターン終了時に負け確定）
            reason = 2
            turn_list.append(turn)
            reason_list.append(reason)
            log_list.append(log)
            break
          
        else:
            board = turn_switch(next_board)
            turn += 1


      else: #後手のターン
        if board[0][0] == 1 or board[0][5] == 1:
            #決着がついた場合、先手視点になるように盤面をひっくり返している
            board = turn_switch(board)
            #この時点でのboard = 決着ボード（1手前の先手のターン終了時点で勝ち確定済み）
            reason = 6
            turn_list.append(turn - 1)
            reason_list.append(reason)
            log_list.append(log)
            break
        

        #まだ結果が定まっていないため次の行動選択
        next_board_list = make_my_next_board_list(board)
        next_board = choice_board(next_board_list, turn, mode)

        #行動選択後、盤面を見て決着がついたかを判断
        if count_ghosts(next_board) == 1:
            #↓ここで盤面をひっくり返しているのはあくまで先手視点でlogを作成するため
            board = turn_switch(next_board)
            #この時点でのboard = 決着ボード（「後手のターン終了時にこの盤面」で負け）
            log.append(board)
            reason = 4
            turn_list.append(turn)
            reason_list.append(reason)
            log_list.append(log)
            break
        elif count_ghosts(next_board) == 2:
            #↓ここで盤面をひっくり返しているのはあくまで先手視点でlogを作成するため
            board = turn_switch(next_board)
            #この時点でのboard = 決着ボード（「後手のターン終了時にこの盤面」で勝ち）
            log.append(board)
            reason = 5
            turn_list.append(turn)
            reason_list.append(reason)
            log_list.append(log)
            break
        else:
            board = turn_switch(next_board)
            log.append(board)
            turn += 1
  return turn_list, reason_list, log_list

#勝率の計算
def make_win_rate(mode, times, reason_list):
    count = []
    for i in [1, 2, 3, 4, 5, 6]:
        #1~6のreasonごとの決着数をリストにする
        count.append(reason_list.count(i))
    #先手の勝ち数
    f_win = count[0] + count[2] + count[4]
    #後手の勝ち数
    l_win = count[1] + count[3] + count[5]

    if mode == 0:
        #先手の勝率
        win_rate = f_win / times
    else:
        #後手の勝率
        win_rate = l_win / times
    return win_rate



#mode = random.randint(0, 1)
#mode = 0 なら学習AIが先手、mode = 1 ならランダムAIが先手
mode = 0
times = 100 #試合数
turn_list, reason_list, log_list = game(times, mode)
win_rate = make_win_rate(mode, times, reason_list)
print("学習AIが先手の場合の勝率:", win_rate)

mode = 1
turn_list, reason_list, log_list = game(times, mode)
win_rate = make_win_rate(mode, times, reason_list)
print("学習AIが後手の場合の勝率:", win_rate)
print(win_rate)

#reasonは、
# 1→先手が最後の行動により勝ち、 2→先手が最後の行動により負け
# 3→後手が最後の行動により負け、 4→後手が最後の行動により勝ち
# 5→後手が最後の行動により負け、 6→先手が最後の行動により負け

