from PIL import Image, ImageDraw
import copy
import random
import numpy as np

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


def make_png_list(next_board_list):
  grid_size = 40
  mode = 1 #0は相手の役がわかる。1はわからない。
  s = 0
  L = len(next_board_list)
  for board in next_board_list:
    img = Image.new("RGB", (grid_size * 6 + 1, grid_size * 6 + 1), "white")
    draw = ImageDraw.Draw(img)
    for i in range(7):
      draw.line([(0, grid_size * i), (240, grid_size * i)], "black")
      draw.line([(grid_size * i, 0), (grid_size * i, 240)], "black")

    draw.rectangle([(0, 0), (grid_size, grid_size)], outline = "green", width = 2)
    draw.rectangle([(grid_size * 5, 0), (grid_size * 6, grid_size)], outline = "green", width = 2)
    draw.rectangle([(0, grid_size * 5), (grid_size, grid_size * 6)], outline = "green", width = 2)
    draw.rectangle([(grid_size * 5, grid_size * 5), (grid_size * 6, grid_size * 6)], outline = "green", width = 2)

    for i in range(6):
      for j in range(6):
        ghost_type = board[i][j]
        if ghost_type == 1:
          color, enemy = "blue", 0
        elif ghost_type == 2:
          color, enemy = "red", 0
        elif ghost_type == -1:
          if mode == 0:
            color, enemy = "blue", 180
          else:
            color, enemy = "purple", 180
        elif ghost_type == -2:
          if mode == 0:
            color, enemy = "red", 180
          else:
            color, enemy = "purple", 180
        else:
          color = None

        if color != None:
          x, y = grid_size * j, grid_size * i
          draw.arc([(x + 4, y + 9), (x + 16, y + 21)], 90, 180, "black")
          draw.arc([(x + 4, y + 12), (x + 16, y + 18)], 90, 180, "black")
          draw.arc([(x + 24, y + 18), (x + 36, y + 30)], 270, 360, "black")
          draw.arc([(x + 24, y + 21), (x + 36, y + 27)], 270, 360, "black")
          draw.arc([(x + 10, y + 8), (x + 30, y + 28)], 180, 360, "black")
          if enemy == 180:
            draw.chord([(x + 10, y + 8), (x + 30, y + 28)], 180, 360, fill = "black")
          draw.arc([(x + 10, y + 30), (x + 14, y + 34)], 0, 180, "black")
          draw.arc([(x + 14, y + 30), (x + 18, y + 34)], 180, 360, "black")
          draw.arc([(x + 18, y + 30), (x + 22, y + 34)], 0, 180, "black")
          draw.arc([(x + 22, y + 30), (x + 26, y + 34)], 180, 360, "black")
          draw.arc([(x + 26, y + 30), (x + 30, y + 34)], 0, 180, "black")
          draw.line([(x + 10, y + 18), (x + 10, y + 32)], "black")
          draw.line([(x + 30, y + 18), (x + 30, y + 32)], "black")
          draw.regular_polygon((x + 20, y + 23, 4), 3, enemy, fill = color)
    img.show()
    s += 1
    if s < L:
      print("or")
    else:
      print("end")


def make_png(board, reason, turn, arrow):
  grid_size = 40
  if turn == 0:
    edgeColor = "black"
  elif turn % 2 == 1:
    edgeColor = "blue"
  else:
    edgeColor = "red"
  mode = 1 #0は相手の役がわかる。1はわからない。
  if reason != 0:
    mode = 0
  img = Image.new("RGB", (grid_size * 8, grid_size * 6 + 1), "white")
  draw = ImageDraw.Draw(img)
  for i in range(7):
    if i == 0 or i == 6:
      draw.line([(grid_size, grid_size * i), (grid_size * 7, grid_size * i)], edgeColor)
      draw.line([(grid_size * (i + 1), 0), (grid_size * (i + 1), grid_size * 6)], edgeColor)
    else:
      draw.line([(grid_size, grid_size * i), (grid_size * 7, grid_size * i)], "black")
      draw.line([(grid_size * (i + 1), 0), (grid_size * (i + 1), grid_size * 6)], "black")

  draw.rectangle([(grid_size, 0), (grid_size * 2, grid_size)], outline = "green", width = 2)
  draw.rectangle([(grid_size * 6, 0), (grid_size * 7, grid_size)], outline = "green", width = 2)
  draw.rectangle([(grid_size, grid_size * 5), (grid_size * 2, grid_size * 6)], outline = "green", width = 2)
  draw.rectangle([(grid_size * 6, grid_size * 5), (grid_size * 7, grid_size * 6)], outline = "green", width = 2)

  if turn != 0:
    ar_l = arrow_location(arrow, grid_size)
    draw.line([(ar_l[0][0], ar_l[0][1]), (ar_l[1][0], ar_l[1][1])], edgeColor, width = 2)
    draw.line([(ar_l[1][0], ar_l[1][1]), (ar_l[2][0], ar_l[2][1])], edgeColor, width = 2)
    draw.line([(ar_l[1][0], ar_l[1][1]), (ar_l[3][0], ar_l[3][1])], edgeColor, width = 2)

  for i in range(6):
    for j in range(6):
      ghost_type = board[i][j]
      if ghost_type == 1:
        color, enemy = "blue", 0
      elif ghost_type == 2:
        color, enemy = "red", 0
      elif ghost_type == -1:
        if mode == 0:
          color, enemy = "blue", 180
        else:
          color, enemy = "purple", 180
      elif ghost_type == -2:
        if mode == 0:
          color, enemy = "red", 180
        else:
          color, enemy = "purple", 180
      else:
        color = None

      if color != None:
        x, y = grid_size * (j + 1), grid_size * i
        draw.arc([(x + 4, y + 9), (x + 16, y + 21)], 90, 180, "black")
        draw.arc([(x + 4, y + 12), (x + 16, y + 18)], 90, 180, "black")
        draw.arc([(x + 24, y + 18), (x + 36, y + 30)], 270, 360, "black")
        draw.arc([(x + 24, y + 21), (x + 36, y + 27)], 270, 360, "black")
        draw.arc([(x + 10, y + 8), (x + 30, y + 28)], 180, 360, "black")
        if enemy == 180:
          draw.chord([(x + 10, y + 8), (x + 30, y + 28)], 180, 360, fill = "black")
        draw.arc([(x + 10, y + 30), (x + 14, y + 34)], 0, 180, "black")
        draw.arc([(x + 14, y + 30), (x + 18, y + 34)], 180, 360, "black")
        draw.arc([(x + 18, y + 30), (x + 22, y + 34)], 0, 180, "black")
        draw.arc([(x + 22, y + 30), (x + 26, y + 34)], 180, 360, "black")
        draw.arc([(x + 26, y + 30), (x + 30, y + 34)], 0, 180, "black")
        draw.line([(x + 10, y + 18), (x + 10, y + 32)], "black")
        draw.line([(x + 30, y + 18), (x + 30, y + 32)], "black")
        draw.regular_polygon((x + 20, y + 23, 4), 3, enemy, fill = color)

  if reason == 3 or reason == 6:
    if reason == 3:
      if arrow[1] == 0:
        x, y = 0, 0
        color, enemy = "blue", 0
      else:
        x, y = grid_size * 7, 0
        color, enemy = "blue", 0
    else:
      if arrow[1] == 0:
        x, y = 0, grid_size * 5
        color, enemy = "blue", 180
      else:
        x, y = grid_size * 7, grid_size * 5
        color, enemy = "blue", 180
    draw.arc([(x + 4, y + 9), (x + 16, y + 21)], 90, 180, "black")
    draw.arc([(x + 4, y + 12), (x + 16, y + 18)], 90, 180, "black")
    draw.arc([(x + 24, y + 18), (x + 36, y + 30)], 270, 360, "black")
    draw.arc([(x + 24, y + 21), (x + 36, y + 27)], 270, 360, "black")
    draw.arc([(x + 10, y + 8), (x + 30, y + 28)], 180, 360, "black")
    if enemy == 180:
      draw.chord([(x + 10, y + 8), (x + 30, y + 28)], 180, 360, fill = "black")
    draw.arc([(x + 10, y + 30), (x + 14, y + 34)], 0, 180, "black")
    draw.arc([(x + 14, y + 30), (x + 18, y + 34)], 180, 360, "black")
    draw.arc([(x + 18, y + 30), (x + 22, y + 34)], 0, 180, "black")
    draw.arc([(x + 22, y + 30), (x + 26, y + 34)], 180, 360, "black")
    draw.arc([(x + 26, y + 30), (x + 30, y + 34)], 0, 180, "black")
    draw.line([(x + 10, y + 18), (x + 10, y + 32)], "black")
    draw.line([(x + 30, y + 18), (x + 30, y + 32)], "black")
    draw.regular_polygon((x + 20, y + 23, 4), 3, enemy, fill = color)

  img.show()

  if reason == 0:
    if turn % 2 == 0:
      print("↓ Your turn")
    else:
      print("↓ Enemy turn")
  elif reason == 1:
    print("You win! You got all of enemy's blue ghosts. (by "+ str(turn) + " turns)")
  elif reason == 2:
    print("You lose. You got all of enemy's red ghosts. (by " + str(turn) + " turns)")
  elif reason == 3:
    print("You win! Your blue ghost escaped. (by "+ str(turn) + " turns)")
  elif reason == 4:
    print("You lose. Enemy got all of your blue ghosts. (by "+ str(turn) + " turns)")
  elif reason == 5:
    print("You win! Enemy got all of your red ghosts. (by " + str(turn) + " turns)")
  elif reason == 6:
    print("You lose. Enemy's blue ghost escaped. (by "+ str(turn) + " turns)")

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

def gameplay_png():
  board = make_board()
  make_png(board, 0, 0, [])
  turn = 1
  while True:
    if turn % 2 == 1: #自分のターン
      if board[0][0] == 1:
        #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で勝ち）
        board[0][0] = 0
        make_png(next_board, 3, turn, [0, 0, 0, -1])
        return
      elif board[0][5] == 1:
        #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で勝ち）
        board[0][5] = 0
        make_png(board, 3, turn, [0, 5, 0, 6])
        return
      next_board_list, arrow_list = make_my_next_board_list(board)
      next_board, arrow = choice_board(next_board_list, arrow_list)
      if count_ghosts(next_board) == 1:
        #この時点でのnext_board = 決着ボード（「自分のターン終了時にこの盤面」で勝ち）
        make_png(next_board, 1, turn, arrow)
        return
      elif count_ghosts(next_board) == 2:
        #この時点でのnext_board = 決着ボード（「自分のターン終了時にこの盤面」で負け）
        make_png(next_board, 2, turn, arrow)
        return
      else:
        make_png(next_board, 0, turn, arrow)
        board = turn_switch(next_board)
        turn += 1
    else: #相手のターン
      if board[0][0] == 1:
        board = turn_switch(board)
        #この時点でのboard = 決着ボード（「自分のターン終了時にこの盤面」で負け）
        board[5][5] = 0
        make_png(board, 6, turn, [5, 5, 5, 6])
        return
      elif board[0][5] == 1:
        board = turn_switch(board)
        #この時点でのboard = 決着ボード（「自分のターン終了時にこの盤面」で負け）
        board[5][0] = 0
        make_png(board, 6, turn, [5, 0, 5, -1])
        return
      next_board_list, arrow_list = make_my_next_board_list(board)
      next_board, arrow = choice_board(next_board_list, arrow_list)
      if count_ghosts(next_board) == 1:
        board = turn_switch(next_board)
        #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で負け）
        arrow = reverse_arrow(arrow)
        make_png(board, 4, turn, arrow)
        return
      elif count_ghosts(next_board) == 2:
        board = turn_switch(next_board)
        #この時点でのboard = 決着ボード（「相手のターン終了時にこの盤面」で勝ち）
        arrow = reverse_arrow(arrow)
        make_png(board, 5, turn, arrow)
        return
      else:
        board = turn_switch(next_board)
        arrow = reverse_arrow(arrow)
        make_png(board, 0, turn, arrow)
        turn += 1

'''
def game_play(times):
  turn_list, reason_list, log_list, log = [], [], [], []
  for _ in range(times):
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
'''


board = make_board()

'''
make_png(board, 0, 0, [])
next_board_list, arrow_list = make_my_next_board_list(board)
make_png_list(next_board_list)

'''

random.seed(0)
gameplay_png()


