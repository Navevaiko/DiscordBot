from models.GameModel import Game

def get_id_from_mention(user_mentioned):
  return int(user_mentioned[3:21])

def get_game_by_players(games, challenger, challenged):
  try:
    game_id = f'{challenger}{challenged}'
    inverted_game_id = f'{challenged}{challenger}'
    return [game for game in games if game.id in [game_id, inverted_game_id]][0]
  except IndexError:
    return None

def get_game_by_channel_name(games, channel_name):
  try:
    return [game for game in games if game.channel.name == channel_name][0]
  except IndexError:
    return None

def get_invite_by_players(pending_invites, challenger, challenged):
  try:
    invite_id = f'{challenger}{challenged}'
    inverted_invite_id = f'{challenged}{challenger}'
    return [invite for invite in pending_invites if invite.id in [invite_id, inverted_invite_id]][0]
  except IndexError:
    return None

def get_user_invites(pending_invites, user_id):
  return [invite for invite in pending_invites if invite.challenged_player == user_id]