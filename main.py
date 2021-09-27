import discord, qikdb, os, random, requests;

from bs4 import BeautifulSoup;
from server import ping_server;
from qikdb import DB;

from time import sleep as wait;
from datetime import datetime;

from cmds import cmds_ as commands_list;

import discord.ext;
from discord.utils import get;
from discord.ext import commands, tasks;
from discord.ext.commands import has_permissions,  CheckFailure, check;

client = discord.Client();
bot = commands.Bot(command_prefix = os.environ["PREFIX"], case_insensitive = True, help_command = None);

timestamp = datetime.now().strftime("%H:%M");

@bot.event
async def on_ready():
    os.system("clear");
    print(f"Logged in as {bot.user}");
    
    
@bot.command(name = "help", aliases = ["commands", "cmds"])
async def help(ctx, *args):
    help_embed = discord.Embed(title = "***help:***", color = discord.Color.from_rgb(255, 255, 255));

    for command in commands_list:
        if hasattr(command, "args"):
            help_embed.add_field(name = f"{os.environ['prefix']}{command.name} {command.args}", value = f"{command.description}");
        else:
            help_embed.add_field(name = f"{os.environ['prefix']}{command.name}", value = f"{command.description}");

    await ctx.send(embed = help_embed);

@bot.command(name = "predict", aliases = ["8ball"])
async def predict(ctx):
    responses = ["Yes.", "No.", "Maybe.", "Certainly.", "For sure.", "Never.", "In your dreams."];
    
    predict_embed = discord.Embed(title = "***prediction:***", description = f"{random.choice(responses)}", color = discord.Color.from_rgb(255, 255, 255));
    predict_embed.set_footer(text = f"sent at {timestamp}");

    await ctx.send(embed = predict_embed);

@bot.command(name = "kick", aliases = ["boot"])
async def kick(ctx, member : discord.Member, *args):
    kick_perms = ctx.author.guild_permissions.kick_members;

    if kick_perms:
        try:
            given_reason = " ".join(args[0:]);
            await member.kick(reason = given_reason);

            kicked_embed = discord.Embed(title = "**Moderation:***", description = f"*Kicked: {member.mention}\nReason: `{given_reason}`*", color = discord.Color.from_rgb(87, 64, 255));
            kicked_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = kicked_embed);
        except Exception as err:
            error_embed = discord.Embed(title = "***Error:***", description = f"*Error Message - `{err}`*");
            error_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = error_embed);

@bot.command(name = "ban")
async def ban(ctx, member: discord.Member, *args):
    ban_perms = ctx.author.guild_permissions.ban_members;
    
    if ban_perms:
        try:
            given_reason = " ".join(args[0:]);
            await member.ban(reason = given_reason);

            banned_embed = discord.Embed(title = "***Moderation:***", description = f"*Banned: {member.mention}\nReason: `{given_reason}`*", color = discord.Color.from_rgb(87, 64, 255));
            banned_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = banned_embed);
        except Exception as err:
            error_embed = discord.Embed(title = "***Error:***", description = f"*Error Message - `{err}`*");
            error_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = error_embed);
    else:
        error_embed = discord.Embed(title = "***Invalid Permissions:***", description = "*Error - `You do not have the permissions to ban this user.`*", color = discord.Color.from_rgb(250, 65, 77));
        error_embed.set_footer(text = f" Sent at: {timestamp}");

        await ctx.send(error_embed);

@bot.command(name = "neko")
async def neko(ctx):
    channel_type = ctx.channel;

    res = requests.get(method = "GET", )
    bs = BeautifulSoup(res.content, "html.parser");
    img_url = bs.find("img").attrs["src"];

    neko_embed = discord.Embed(title = "***Neko:***", color = discord.Color.from_rgb(168, 52, 235))
    neko_embed.set_image(img_url);

    await ctx.send(embed = neko_embed)

ping_server();
bot.run(os.environ["TOKEN"]);