
class Game():
  
  MARKS = [':regional_indicator_x:', ':o2:']
  ROW_SIZE = 3
  COLUMN_SIZE = 3

  def __init__(self, challenger, challenged_player):
    self.id = f'{challenger.id}{challenged_player.id}'
    self.state = 0
    self.board = []
    self.turn = 0
    self.players = [
      { 'name': challenger.name, 'id': challenger.id, 'mark': self.MARKS[0] },
      { 'name': challenged_player.name, 'id': challenged_player.id, 'mark': self.MARKS[1] }
    ]
    self.channel = None

  def init_game(self):
    self.state = 1

    for _ in range(0, self.ROW_SIZE):
      columns = []

      for __ in range(0, self.COLUMN_SIZE):
        columns.append('')

      self.board.append(columns)
  
  async def print_board(self):
    for _, row in enumerate(self.board):
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
    for col in range(0, self.COLUMN_SIZE):
      column_values = [self.board[row][col] for row in range(0, self.ROW_SIZE)]

      if column_values.count(mark) == len(column_values):
        return player
      
    # Checking diagonals
    diag = [
      [self.board[row][row] for row in range(0, self.COLUMN_SIZE)],
      [self.board[row][abs(row - (self.COLUMN_SIZE - 1))] for row in range(0, self.COLUMN_SIZE)]
    ]
    if diag[0].count(mark) == len(diag[0]) or diag[1].count(mark) == len(diag[1]):
      return player

    return None
  
  def __repr__(self):
    return f'<@{self.players[0]["name"]}> vs <@{self.players[1]["name"]}>'