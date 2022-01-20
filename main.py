import discord
from discord.ext import commands
import os
import ast
import asyncio
import inspect
import requests
import re
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, create_button, wait_for_component

from discord_slash import SlashCommand, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from typing import Union, Any



intents = discord.Intents().all()
client = commands.Bot(command_prefix='s!', intents=intents)
color = 0x5865F2
#0xb062a9
footertext = "made with ❤"
slash = SlashCommand(client, sync_commands=True)


async def change_pres():
  await client.wait_until_ready()
  
  while not client.is_closed():


    await client.change_presence(activity=discord.Game(name='/help for help'))
    await asyncio.sleep(5)

    await client.change_presence(activity=discord.Streaming(name=f"to {len(client.users)} users", url='https://twitch.tv/tiktoknoteason'))
    await asyncio.sleep(5)

    await client.change_presence(activity=discord.Game(name='discord.gg/noteason'))
    await asyncio.sleep(5)
    guildcount=len(client.guilds) + 2
    await client.change_presence(activity=discord.Game(name=f'In {guildcount} Servers'))
    await asyncio.sleep(5)

@client.event
async def on_ready():
  print(f'client ready as {client.user.name}#{client.user.discriminator}')

@slash.slash(description="help command")
async def help(ctx):
  embed=discord.Embed(title="Stitch Help | 📋", color=color)
  embed.add_field(name="Support | Help", value="[Support Server](https://discord.gg/noteason) | [invite](https://discord.com/api/oauth2/authorize?client_id=892078548234403891&permissions=8&scope=bot%20applications.commands)")
  await ctx.send(embed=embed)

@slash.slash(description="Get Fortnite Cosmetic")
async def item(ctx, *, item):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={item}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(title=sub_dict['name'], description=sub_dict['description'], color=color)
      embed.add_field(name='ID', value=sub_dict['id'])
      embed.add_field(name='Type', value=f"{sub_dict['type']['value']}")
      embed.add_field(name='Rarity', value=f"{sub_dict['rarity']['value']}")
      #embed.add_field(name='Set', value=f"{sub_dict['set']['text']}")
      
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=sub_dict['introduction']['text'])
        embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png")
        embed.set_footer(text=footertext)
        message = await ctx.send(embed=embed)
  else:
    embed = discord.Embed(color=color)
    embed.add_field(name='Error', value=f"```{rr['error']}```", inline=False)
    embed.set_footer(text=footertext)
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

@slash.slash(description="Search Up A Creator Code")
async def creator(ctx, *, code):
  await ctx.defer()
  r = requests.get(f'https://fortnite-api.com/v2/creatorcode?name={code}')
  if r.status_code == 200:
    data = r.json()
    embed=discord.Embed(title=f"Creator Code - {code}", color=color)
    embed.add_field(name="Epic Games Name", value=data['data']['account']['name'], inline=False)
    embed.add_field(name="Epic Games ID", value=data['data']['account']['id'], inline=False)
    embed.add_field(name="Status", value=data['data']['status'], inline=False)
    embed.add_field(name="Verified", value=data['data']['verified'], inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send("Creator Not Found!")

@slash.slash(description="invite me!")
async def invite(ctx):
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=892078548234403891&permissions=8&scope=bot%20applications.commands")

@slash.slash(description="battle royale news")
async def brnews(ctx):
 
    response = requests.get(f'https://fortnite-api.com/v2/news/br?language=en')

    geted = response.json()
        
    if response.status_code == 200:

        image = geted['data']['image']

        embed = discord.Embed(color=color)
        embed.set_image(url=image)
        embed.set_footer(text=footertext)

        await ctx.reply(embed=embed)

    elif response.status_code == 400:
 
        error = geted['error']

        embed = discord.Embed(title='Error', 
                description=f'`{error}`')

        await ctx.reply(embed=embed)

    elif response.status_code == 404:

        error =geted['error']

        embed = discord.Embed(title='Error', 
        description=f'``{error}``')

        await ctx.reply(embed=embed)

@slash.slash(description="Creative Map Info")
async def island(ctx, code):
  await ctx.defer()
  url = f"https://fortniteapi.io/v1/creative/island?code={code}"
  headers = {
      "Authorization": os.environ['fortniteio']
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


@slash.slash(description="Get A Weapons WID")
async def wid(ctx, *, weapon):
    await ctx.defer()

    embed=discord.Embed(title=f"All Weapons Matching: {weapon}", color=color)
    url = "https://fortniteapi.io/v1/loot/list?lang=en"
    headers = {
        "Authorization": os.environ['fortniteio']
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
client.loop.create_task(change_pres())
client.run(os.environ['token'])
