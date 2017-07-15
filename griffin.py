from discord import Embed, Color
from random import randint

def repost(msgtxt, msgtime):
  return Embed(title="Pros don't delete messages! Here's Griffin's last message:", description=msgtxt, color=Color(randint(0, 16777215)), timestamp=msgtime)
