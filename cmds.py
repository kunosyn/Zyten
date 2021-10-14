import os;
pfx = os.environ["PREFIX"];

cmds_ = [
  {
    "name": "predict",
    "description": "Gives a random response to predict what you ask.",
    "type": "Misc", 
    "args": "<question>"
  },

  {
    "name": "snipe",
    "description": "Sends the most recently deleted message.",
    "type": "Misc"
  },
  
  {
    "name": "kick",
    "description": "Kicks mentioned user for optional given reason.",
    "type": "Moderation",
    "args": "<@user> <(optional) reason>"
  },

  {
    "name": "ban",
    "description": "Bans mentioned user for optional given reason.",
    "type": "Moderation",
    "args": "<@user> <(optional) reason>"
  },
  
  {
    "name": "join",
    "description": "Joins VC that message author is connected to.",
    "type": "Voice"
  },

  {
    "name": "leave",
    "description": "Leaves VC that client is currently connected to.",
    "type": "Voice"
  },

  {
    "name": "neko",
    "description": "Posts an image of a NSFW neko to the channel.",
    "type": "NSFW",
  },

  {
    "name": "hentai",
    "description": "Posts a hentai image to the channel.",
    "type": "NSFW"
  }
  
]