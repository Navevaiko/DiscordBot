class Invite():
  id = 0
  challenger = ''
  challenged_player = ''

  def __init__(self, challenger, challenged_player):
    self.id = f'{challenger}{challenged_player}'
    self.challenger = challenger
    self.challenged_player = challenged_player
  
  def __repr__(self):
      return f'{self.challenger} vs {self.challenged_player}'