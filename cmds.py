import os;

pfx = os.environ["PREFIX"];

cmds_ = [
  {
    "name": "predict",
    "description": "Gives a random response to predict what you ask.",
    "args": "<question>"
  },
  {
    "name": "kick",
    "description": "Kicks mentioned user for optional given reason.",
    "args": "<@user> <(optional) reason>"
  },
  {
    "name": "ban",
    "description": "Bans mentioned user for optional given reason.",
    "args": "<@user> <(optional) reason>"
  }
]