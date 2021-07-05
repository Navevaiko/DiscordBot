import utils

ROW_SIZE=3
COLUMN_SIZE=3
MARKS = [':regional_indicator_x:', ':o2:']

turn = 0
board = []
players = []

def add_user(user_id, accepted):
  players.append({
    'id': user_id,
    'acceppted': accepted,
    'mark': MARKS[len(players)]
  })

def init_game():
  for row in range(0, 3):
    columns = []

    for col in range(0, 3):
      columns.append('')

    board.append(columns)

async def print_board(ctx):
  for r_index, row in enumerate(board):
    columns = ''
      
    for c_index, col in enumerate(row):
      end = '' if c_index == len(row) - 1 else '  '
      empty_char = ':white_large_square:'
      col_value = f'{col}' if col != '' else empty_char

      columns += f'{col_value}{end}'

    await ctx.send(f'{columns}')

def get_current_player():
  return players[turn % 2]

def add_to_board(row, column, player_id):
  global turn
  
  mark = [player['mark'] for player in players if player['id'] == player_id][0]
  board[row][column] = mark

  turn += 1

def position_available(row, column):
  return board[row - 1][column - 1] == ''

def check_winner(current_player_id):
  player = [player for player in players if player['id'] == current_player_id][0]
  mark = player['mark']

  # Checking rows
  for row in board:
    if row.count(mark) == len(row):
      return player
  
  # Checking columns
  for col in range(0, COLUMN_SIZE):
    column_values = [board[row][col] for row in range(0, ROW_SIZE)]

    if column_values.count(mark) == len(column_values):
      return player
    
  # Checking diagonals
  diag = [
    [board[row][row] for row in range(0, COLUMN_SIZE)],
    [board[row][abs(row - (COLUMN_SIZE - 1))] for row in range(0, COLUMN_SIZE)]
  ]
  if diag[0].count(mark) == len(diag[0]) or diag[1].count(mark) == len(diag[1]):
    return player

  return None

def end_game():
  global board
  global players
  global turn

  board = []
  players = []
  turn = 0