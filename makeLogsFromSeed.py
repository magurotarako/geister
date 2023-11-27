from PIL import Image, ImageDraw
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


#コマンドライン引数としてファイル名を指定　(python3 makeLogsFromSeed.py seed{0}_alpha{1}_match{2}_border{3}.yml)
yml_name = sys.argv[1]

#コマンドライン引数として指定したファイル名からseed値、alpha値、match値（１並列当たりの試合数）、border値（閾値）を取得
with open('{0}'.format(yml_name)) as file:
    params = yaml.safe_load(file)
    seed = params['seed']
    alpha = params['alpha']
    match = params['match']
    border = params['border']




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




def arrow_location(arrow, grid_size):
  a, b, c, d = arrow
  s_x, s_y = grid_size * (b + 1) + 20, grid_size * a + 20
  g_x, g_y = grid_size * (d + 1) + 20, grid_size * c + 20
  if c - a == 1: #down
    return [[s_x, s_y], [g_x, g_y], [g_x + 10, g_y - 10], [g_x - 10, g_y - 10]]
  elif c - a == -1: #up
    return [[s_x, s_y], [g_x, g_y], [g_x + 10, g_y + 10], [g_x - 10, g_y + 10]]
  elif d - b == 1: #right
    return [[s_x, s_y], [g_x, g_y], [g_x - 10, g_y - 10], [g_x - 10, g_y + 10]]
  elif d - b == -1: #left
    return [[s_x, s_y], [g_x, g_y], [g_x + 10, g_y - 10], [g_x + 10, g_y + 10]]

def count_ghosts(board):
  if np.any(board == -1) == False:
    return 1
  elif np.any(board == -2) == False:
    return 2
  else:
    return 0


def make_my_next_board_list(board):
  myghosts = find_myghosts(board)
  next_board_list, arrow_list = move(myghosts, board)
  return next_board_list, arrow_list


def find_myghosts(board):
  myghosts = []
  for i in range(6):
    for j in range(6):
      if board[i][j] in (1, 2):
        myghosts.append([i, j])
  return myghosts

def move(myghosts, board):
  next_board_list, arrow_list = [], []
  for ghost in myghosts:
    i, j = ghost
    for k in range(4):
      next_board = np.copy(board)
      if k == 0:
        can = move_up(ghost, myghosts, board)
        if can == True:
          next_board[i - 1][j] = next_board[i][j]
          next_board[i][j] = 0
          arrow_list.append([i, j, i - 1, j])
          next_board_list.append(next_board)
      elif k == 1:
        can = move_down(ghost, myghosts)
        if can == True:
          next_board[i + 1][j] = next_board[i][j]
          next_board[i][j] = 0
          arrow_list.append([i, j, i + 1, j])
          next_board_list.append(next_board)
      elif k == 2:
        can = move_left(ghost, myghosts)
        if can == True:
          next_board[i][j - 1] = next_board[i][j]
          next_board[i][j] = 0
          arrow_list.append([i, j, i, j - 1])
          next_board_list.append(next_board)
      else:
        can = move_right(ghost, myghosts)
        if can == True:
          next_board[i][j + 1] = next_board[i][j]
          next_board[i][j] = 0
          arrow_list.append([i, j, i, j + 1])
          next_board_list.append(next_board)
  return next_board_list, arrow_list

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


def choice_board(next_board_list, arrow_list):
  L = len(next_board_list)
  choice = random.randint(0, L - 1)
  return next_board_list[choice], arrow_list[choice]


def turn_switch(next_board):
  change = np.copy(next_board)
  change_2 = np.reshape(change, (1, 36))
  change_2_reverse = np.array(change_2[0][::-1])
  change_board = np.reshape(change_2_reverse, (6, 6))
  change_board *= -1
  return change_board

def reverse_arrow(arrow):
  a, b, c, d = arrow
  return [5 - a, 5 - b, 5 - c, 5 - d]



def game_play(times):
  turn_list, reason_list, log_list = [], [], []
  for _ in range(times):
    log = []
    board = make_board()
    #make_png(board, 0, 0, [])
    log.append(board)
    turn = 1
    while True:
      if turn % 2 == 1: #自分のターン
        if board[0][0] == 1:
          #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で勝ち）
          #board[0][0] = 0
          reason = 3
          #make_png(next_board, reason, turn, [0, 0, 0, -1])
          turn_list.append(turn - 1)
          reason_list.append(reason)
          log_list.append(log)
          break
        elif board[0][5] == 1:
          #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で勝ち）
          #board[0][5] = 0
          reason = 3
          #make_png(board, reason, turn, [0, 5, 0, 6])
          turn_list.append(turn - 1)
          reason_list.append(reason)
          log_list.append(log)
          break
        next_board_list, arrow_list = make_my_next_board_list(board)
        next_board, arrow = choice_board(next_board_list, arrow_list)
        log.append(next_board)
        if count_ghosts(next_board) == 1:
          #この時点でのnext_board = 決着ボード（「自分のターン終了時にこの盤面」で勝ち）
          reason = 1
          #make_png(next_board, reason, turn, arrow)
          turn_list.append(turn)
          reason_list.append(reason)
          log_list.append(log)
          break
        elif count_ghosts(next_board) == 2:
          #この時点でのnext_board = 決着ボード（「自分のターン終了時にこの盤面」で負け）
          reason = 2
          #make_png(next_board, reason, turn, arrow)
          turn_list.append(turn)
          reason_list.append(reason)
          log_list.append(log)
          break
        else:
          #make_png(next_board, 0, turn, arrow)
          board = turn_switch(next_board)
          turn += 1
      else: #相手のターン
        if board[0][0] == 1:
          board = turn_switch(board)
          #この時点でのboard = 決着ボード（「自分のターン終了時にこの盤面」で負け）
          #board[5][5] = 0
          reason = 6
          #make_png(board, reason, turn, [5, 5, 5, 6])
          turn_list.append(turn - 1)
          reason_list.append(reason)
          log_list.append(log)
          break
        elif board[0][5] == 1:
          board = turn_switch(board)
          #この時点でのboard = 決着ボード（「自分のターン終了時にこの盤面」で負け）
          #board[5][0] = 0
          reason = 6
          #make_png(board, reason, turn, [5, 0, 5, -1])
          turn_list.append(turn - 1)
          reason_list.append(reason)
          log_list.append(log)
          break
        next_board_list, arrow_list = make_my_next_board_list(board)
        next_board, arrow = choice_board(next_board_list, arrow_list)
        if count_ghosts(next_board) == 1:
          board = turn_switch(next_board)
          #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で負け）
          log.append(board)
          #arrow = reverse_arrow(arrow)
          reason = 4
          #make_png(board, reason, turn, arrow)
          turn_list.append(turn)
          reason_list.append(reason)
          log_list.append(log)
          break
        elif count_ghosts(next_board) == 2:
          board = turn_switch(next_board)
          #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で勝ち）
          log.append(board)
          #arrow = reverse_arrow(arrow)
          reason = 5
          #make_png(board, reason, turn, arrow)
          turn_list.append(turn)
          reason_list.append(reason)
          log_list.append(log)
          break
        else:
          board = turn_switch(next_board)
          log.append(board)
          #arrow = reverse_arrow(arrow)
          #make_png(board, 0, turn, arrow)
          turn += 1
  return turn_list, reason_list, log_list


def make_one_hot(board):
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


def make_switch_log(log):
  switch_log = []
  for i in log:
    switch_log.append(turn_switch(i))
  return switch_log

#board = make_board()

#logからoutputを算出
def make_output(turns, reasons, logs, alpha, match):
  output_log = {}
  for i in range(match):
    turn = turns[i]
    reason = reasons[i]
    #先手視点
    log = logs[i]
    #後手視点
    switch_log = make_switch_log(log)

    if reason % 2 == 1: 
      #奇数なら先手が勝ち≒最後の盤面は先手にとって良い盤面（評価値1）
      start = 1
      #最後の盤面は後手にとって悪い盤面（評価値-1）
      switch_start = -1
    else: 
      #偶数なら後手が勝ち≒最後の盤面は先手にとって悪い盤面（評価値-1）
      start = -1
      #最後の盤面は後手にとって良い盤面（評価値1）
      switch_start = 1
    
    #先手視点でoutput作成
    for j in range(turn + 1):
      point = start * (alpha ** j)
      m = (j + 1) * (-1)
      one_hot = make_one_hot(log[m])
      if one_hot not in output_log:
        output_log[one_hot] = [1, point]
      else:
        value = output_log[one_hot]
        value[0] += 1
        value[1] += point
        output_log[one_hot] = [value[0], value[1]]

    #後手視点でoutput作成
    for k in range(turn + 1):
      point = switch_start * (alpha ** k)
      n = (k + 1) * (-1)
      one_hot = make_one_hot(switch_log[n])
      if one_hot not in output_log:
        output_log[one_hot] = [1, point]
      else:
        value = output_log[one_hot]
        value[0] += 1
        value[1] += point
        output_log[one_hot] = [value[0], value[1]] 
        
  return output_log

#閾値でoutputを一部削除（登場回数が閾値未満の盤面を削除）
def output_cut(output_log, border):
  output = {}
  for key, value in output_log.items():
    if value[0] >= border:
      output[key] = value
  return output



def logToPickle(output, seed, alpha, match, border):
  with open("output_seed{0}_alpha{1}_match{2}_border{3}.pkl".format(seed, alpha, match, border), 'wb') as tf:
    pickle.dump(output, tf)
  return


#最初の盤面があるので、ログの1要素の長さ(len)はそのゲームにおけるターン数+1になる。ずれを考慮すると最後の盤面のindex番号とターン数が一致する。
#ゆえにn回目のゲームのターン数はturns[n - 1] （= t_nとする）、
#n回目のゲームの最後の盤面はlogs[n - 1][t_n]、　（logs[n - 1][turns[n - 1]]とも書ける）
#n回目のゲームの決着理由は、reasons[n - 1]である。
#reasonsは、「1→先手（自分）が最後の行動により勝ち、 2→先手が最後の行動により負け、 3→後手（相手）が最後の行動により負け」
#「4→後手が最後の行動により勝ち、 5→後手が最後の行動により負け、 6→先手が最後の行動により負け」であり、
#勝者にとって、最後の行動（盤面）は評価が高く、敗者にとっては評価が低い、となる。
#ただし、logsのすべての要素は、先手側から見たときの盤面として表されていることに注意する。
#つまり、相手側から見た評価のために視点を変えるときは逆にする必要アリ。
#ターン数は結果が決まるまでのターンであり、奇数なら先手が、偶数なら後手が決定打を（勝敗問わず）打ったことになる。

#yaml_seed = 1
#myDict = dict()
#ハッシュごと配列に吐く、pickle dump

'''
seed = 2
alpha = 0.99
match = 5
border = 2
'''


random.seed(seed)
turns, reasons, logs = game_play(match)
#print(turns)
#print(reasons)
output_log = make_output(turns, reasons, logs, alpha, match)
#print(output_log)
#print("/////////////////")
output = output_cut(output_log, border)
#print(output)
logToPickle(output, seed, alpha, match, border)



#print(logs[-1][0])
#print(logs)
#print(len(turns))
#print(len(reasons))
#print(len(logs))
#print(turns[1000 - 1])
#print(logs[1000 - 1][turns[1000 - 1]])
#print(reasons[1000 - 1])
