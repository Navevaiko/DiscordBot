MARKS = [':regional_indicator_x:', ':o2:']

class Game():
  id = 0
  state = 0
  board = []
  turn = 0
  players = []
  challenged_user_id = ''
  channel = None
  row_size = 0
  column_size = 0

  def __init__(self, challenged_user_id, row_size = 3, column_size = 3):
    self.challenged_user_id = challenged_user_id
    self.row_size = row_size
    self.column_size = column_size
  
  def add_user(self, user_id):
    self.players.append({
      'id': user_id,
      'mark': MARKS[len(self.players)]
    })

  def init_game(self):
    self.state = 1

    for _ in range(0, self.row_size):
      columns = []

      for __ in range(0, self.column_size):
        columns.append('')

      self.board.append(columns)
  
  async def print_board(self):
    for r_index, row in enumerate(self.board):
      columns = ''
        
      for c_index, col in enumerate(row):
        end = '' if c_index == len(row) - 1 else '  '
        empty_char = ':white_large_square:'
        col_value = f'{col}' if col != '' else empty_char

        columns += f'{col_value}{end}'

      await self.channel.send(f'{columns}')

  def get_current_player(self):
    return self.players[self.turn % 2]

  def add_to_board(self, row, column, player_id):
    mark = [player['mark'] for player in self.players if player['id'] == player_id][0]
    self.board[row][column] = mark

    self.turn += 1

  def position_available(self, row, column):
    return self.board[row - 1][column - 1] == ''

  def check_winner(self, current_player_id):
    player = [player for player in self.players if player['id'] == current_player_id][0]
    mark = player['mark']

    # Checking rows
    for row in self.board:
      if row.count(mark) == len(row):
        return player
    
    # Checking columns
    for col in range(0, self.column_size):
      column_values = [self.board[row][col] for row in range(0, self.row_size)]

      if column_values.count(mark) == len(column_values):
        return player
      
    # Checking diagonals
    diag = [
      [self.board[row][row] for row in range(0, self.column_size)],
      [self.board[row][abs(row - (self.column_size - 1))] for row in range(0, self.column_size)]
    ]
    if diag[0].count(mark) == len(diag[0]) or diag[1].count(mark) == len(diag[1]):
      return player

    return None