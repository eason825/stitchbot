import discord
from discord.ext import commands
import os
import os
import ast
import inspect
import requests
import re
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, create_button, wait_for_component

from discord_slash import SlashCommand, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from typing import Union, Any


client = commands.Bot(command_prefix='s!')
color = 0x5865F2
#0xb062a9
footertext = "made with ❤"
slash = SlashCommand(client, sync_commands=True)
fortnite_api_key = "https://fortniteapi.io API key"

@client.event
async def on_ready():
  print(f'client ready as {client.user.name}')

@slash.slash(description="Creative Map Info")
async def island(ctx, code):
  await ctx.defer()
  url = f"https://fortniteapi.io/v1/creative/island?code={code}"
  headers = {
      "Authorization": fortnite_api_key
  }
  r = requests.post(url, headers=headers)
  data = r.json()
  embed=discord.Embed(title=data['island']['title'], description=f"Creator - {data['island']['creator']}", color=color)
  embed.add_field(name="Island Type", value=data['island']['islandPlotTemplate']['name'])
  embed.add_field(name="Published Date", value=data['island']['publishedDate'])
  embed.add_field(name="Description", value=data['island']['description'])
  embed.set_image(url=data['island']['image'])
  embed.set_footer(text=f"Tags - {data['island']['tags']}")
  embed.set_footer(text=footertext)
  await ctx.send(embed=embed)

# make sure that the battle star emoji is changed to an emoji from your own server
@slash.slash(description="Get A Weapons WID")
async def wid(ctx, *, weapon):
    await ctx.defer()

    embed=discord.Embed(title=f"All Weapons Matching: {weapon}", color=color)
    url = "https://fortniteapi.io/v1/loot/list?lang=en"
    headers = {
        "Authorization": fortnite_api_key
    }
    r = requests.post(url, headers=headers)
    data = r.json()
    wids = data['weapons']
    for item in wids:
      namee = item['name']
      if weapon.title() in namee:
        if item['rarity'] == "common":
          rarity = "common | <:battlestar:933052005331660920>"
        if item['rarity'] == "uncommon":
          rarity = "uncommon | <:battlestar:933052005331660920><:battlestar:933052005331660920>"
        if item['rarity'] == "rare":
          rarity = "rare | <:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920>"
        if item['rarity'] == "epic":
          rarity = "epic | <:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920>"
        if item['rarity'] == "legendary":
          rarity = "legendary | <:battlestar:933052005331660920><:battlestar:933052005331660920>"
        if item['rarity'] == "mythic":
          rarity = "mythic | <:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920>"
        if item['rarity'] == "exotic":
          rarity = "exotic | <:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920><:battlestar:933052005331660920>"
        embed.add_field(name=f"{namee} | {item['id']}", value=f"Rarity - **{rarity}**\n\n", inline=False)
    embed.set_footer(text=footertext)
    await ctx.send(embed=embed)


def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)

def ready():
  source_ = source(discord.gateway.DiscordWebSocket.identify)
  patched = re.sub(
      r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])',
      r"\1Discord Android\2",
      source_
  )

  loc = {}
  exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

  discord.gateway.DiscordWebSocket.identify = loc["identify"]


ready()
client.run("TOKEN")
