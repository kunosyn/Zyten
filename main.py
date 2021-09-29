# General Imports #
import discord, qikdb, os, random, requests, urllib, youtube_dl, bs4;

# From Imports #
from bs4 import BeautifulSoup;
from server import ping_server;
from qikdb import DB;
from time import sleep as wait;
from datetime import datetime;
from cmds import cmds_ as commands_list;
from pygelbooru import Gelbooru as Gel;

# Discord Imports #
import discord.ext;
from discord.utils import get;
from discord.ext import commands, tasks;
from discord.ext.commands import has_permissions,  CheckFailure, check;

# Discord Configuration #
client = discord.Client();
bot = commands.Bot(command_prefix = os.environ["PREFIX"], case_insensitive = True, help_command = None);

# Essential Variables #
timestamp = datetime.now().strftime("%H:%M");
colors = {"err": discord.Color.from_rgb(250, 65, 77), "mod": discord.Color.from_rgb(87, 64, 255), "nsfw": discord.Color.from_rgb(168, 52, 235)};

# Class Configurations #
qik = DB(config = {
  "name": "database",
  "directory": "DB"
});


# Functions #
def isadmin(ctx):
    if not qik.exists(f"adminrole.{ctx.guild.id}"):
      qik.set(f"adminrole.{ctx.guild.id}", "Zyten Admin");
    a_role = qik.get(f"adminrole.{ctx.guild.id}");

    if "Zyten Admin" in ctx.author.roles or a_role in ctx.author.roles:
      return True;
    else:
      return False;

    
# START OF EVENTS #
@bot.event
async def on_ready():
    os.system("clear");
    print(f"Logged in as {bot.user} at {timestamp}.");

@bot.event
async def on_message(msg):
    if not qik.exists(f"automod.{msg.guild.id}"):
      qik.set(f"automod.{msg.guild.id}", False);
    
    automod = qik.get(f"automod.{msg.guild.id}");

    if automod:
        if not qik.exists(f"banned_words.{msg.guild.id}"):
            qik.set(f"banned_words.{msg.guild.id}", []);
        banned_words = qik.get(f"banned_words.{msg.guild.id}");

        split_content = msg.content.lower.split(" ");

        for i in range(split_content):
            if split_content[i] == "!" or split_content[i] == "." or split_content[i] == "," or split_content[i] == "?":
                split_content.pop(i);
        
        joined_content = " ".join(split_content);
          
        for word in banned_words:
            if word in joined_content:
                msg.delete();
                break;
    else:
        pass;
    await bot.process_commands(msg);
    
# END OF EVENTS #


# START OF COMMANDS #
@bot.command(name = "help", aliases = ["commands", "cmds"])
async def help(ctx, *args):
    args = args.lower();

    help_embed = discord.Embed(title = "***help:***", color = discord.Color.from_rgb(255, 255, 255));
    if len(args) >= 1:
        if args[0] == "misc":
            for command in commands_list:
                if hasattr(command, "type") and command["type"] == "Misc":
                  if hasattr(command, "args"):
                      help_embed.add_field(name = f"**{os.environ['PREFIX']}  {command['name']} {command['args']}**", value = f"*{command['description']}*");
                  else:
                      help_embed.add_field(name = f"**{os.environ['PREFIX']}{command['name']}**", value = f"*{command['description']}*");
        elif args[0] == "mod" or args[0] == "moderation":
            for command in commands_list:
                if hasattr(command, "type") and command["type"] == "Moderation":
                    if hasattr(command, "args"):
                        help_embed.add_field(name = f"**{os.environ['PREFIX']}{command['name']} {command['args']}**", value = f"{command['description']}");
                    else:
                        help_embed.add_field(name = f"**{os.environ['PREFIX']}{command['name']} {command['args']}**", value = f"*{command['description']}*");
        elif args[0] == "nsfw" or args[0] == "adult":
            for command in commands_list:
                if hasattr(command, "type") and command["type"] == "NSFW":
                    if hasattr(command, "args"):
                        help_embed.add_field(name = f"**{os.environ['PREFIX']}{command['name']} {command['args']}**", value = f"{command['description']}");
                    else:
                        help_embed.add_field(name = f"**{os.environ['PREFIX']}{command['name']}**", value = f"{command['description']}");
    else:
        help_embed.add_field(name = "**Misc:**", value = "*Misc Commands.*", inline = True);
        help_embed.add_field("**Moderation:***", value = "*Moderation Commands.*", inline = True);
        help_embed.add_field(name = "NSFW", value = "NSFW Commands.", inline = True);

    await ctx.send(embed = help_embed);

# MISC Commands #
@bot.command(name = "predict", aliases = ["8ball", "guess"])
async def predict(ctx):
    responses = ["Yes.", "No.", "Maybe.", "Certainly.", "For sure.", "Never.", "In your dreams."];
    
    predict_embed = discord.Embed(title = "***Prediction:***", description = f"{random.choice(responses)}", color = discord.Color.from_rgb(255, 255, 255));
    predict_embed.set_footer(text = f"Sent at {timestamp}");

    await ctx.send(embed = predict_embed);

# VC Commands #
@bot.command(name = "join", aliases = ["summon", "connect"])
async def join(ctx):
    if ctx.author.voice:
        try:
            channel = ctx.author.voice.channel;
            await channel.connect();
        except Exception as err:
            ctx.send(f"I could not connect to the voice channel.\n\nDiscord PY Exception: {err}");
    else:
        ctx.send("You are not connected to a VC.");

@bot.command(name = "leave", aliases = ["disconnect", "unsummon", "fuckoff"])
async def leave(ctx):
    if ctx.author.voice.channel and ctx.voice_client:
      try:
          await ctx.voice_client.disconnect();
      except Exception as err:
          ctx.send(f"I could not disconnect from the voice channel.\n\nDiscord PY Exception: {err}");   

@bot.command(name = "play")
async def play(ctx, *args):
    title = " ".join(args);

# Automation Commands #
@bot.command(name = "automod", aliases = ["amod"])
async def automod(ctx, *args):
    args = args.lower();
    admin = ctx.author.guild_permissions.administrator;

    if admin or isadmin(ctx):
        if len(args) >= 1:
            if args[0] == "enabled" or args[0] == "true" or args[0] == "on":
                qik.set(f"automod.{ctx.guild.id}", True);
            elif args[0] == "disabled" or args[0] == "false" or args[0] == "off":
                qik.set(f"automod.{ctx.guild.id}", False);
            else:
                error_embed = discord.Embed(title = "***Error:***", description = "*Error - Invalid argument provided (enabled/disables).", color = colors["err"]);

                await ctx.send(embed = error_embed);
        else:
            error_embed = discord.Embed(title = "***Invalid Args Amount:**", description = "*Error - `Invalid amount of arguments provided.`*");
    else:
        error_embed = discord.Embed(title = "***Invalid Permissions:***", description = "*Error - `You do not have valid permissions to enable/disable automod in this guild.`*", color = colors["err"]);

        await ctx.send(embed = error_embed);

@bot.command(name = "bannedwords", aliases = ["bw", "wordsbanned"])
async def bannedwords(ctx, *args):
    words = qik.get(f"banned_words.{ctx.guild.id}");
    admin = ctx.author.guild_permission.administrator;

    if admin or isadmin(ctx):
        if len(args) >= 1:
            if args[0] == "add":
                words.append(args[1]);
            elif args[0] == "remove" or args[0] == "delete":
                num = words.index(args[1])
                words.pop(num);
                qik.set(f"banned_words.{ctx.guild.id}", words);

# Moderation Commands #
@bot.command(name = "kick", aliases = ["boot", "italy", "shapeofitaly"])
async def kick(ctx, member : discord.Member, *args):
    kick_perms = ctx.author.guild_permissions.kick_members;

    if kick_perms or isadmin(ctx):
        try:
            given_reason = " ".join(args[0:]);
            await member.kick(reason = given_reason);

            kicked_embed = discord.Embed(title = "**Moderation:***", description = f"*Kicked: {member.mention}\nReason: `{given_reason}`*", color = colors["mod"]);
            kicked_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = kicked_embed);
        except Exception as err:
            error_embed = discord.Embed(title = "***Error:***", description = f"*Error Message - `{err}`*");
            error_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = error_embed);

@bot.command(name = "ban")
async def ban(ctx, member: discord.Member, *args):
    ban_perms = ctx.author.guild_permissions.ban_members;
    
    if ban_perms or isadmin(ctx):
        try:
            given_reason = " ".join(args[0:]);
            await member.ban(reason = given_reason);

            banned_embed = discord.Embed(title = "***Moderation:***", description = f"*Banned: {member.mention}\nReason: `{given_reason}`*", color = discord.Color.from_rgb(87, 64, 255));
            banned_embed.set_footer(text = f" Sent at: {timestamp}");

            await ctx.send(embed = banned_embed);
        except Exception as err:
            error_embed = discord.Embed(title = "***Error:***", description = f"*Error Message - `{err}`*");
            error_embed.set_footer(text = f"Sent at: {timestamp}");

            await ctx.send(embed = error_embed);
    else:
        error_embed = discord.Embed(title = "***Invalid Permissions:***", description = "*Error - `You do not have the permissions to ban this user.`*", color = colors["err"]);
        error_embed.set_footer(text = f" Sent at: {timestamp}");

        await ctx.send(embed = error_embed);

# NSFW Commands #
@bot.command(name = "neko")
async def neko(ctx):
    if ctx.channel.nsfw:
        res = requests.get("https://nekos.life/lewd");
        bs = BeautifulSoup(res.content, "html.parser");
        img_url = bs.find("img").attrs["src"];

        neko_embed = discord.Embed(title = "***Neko:***", color = colors["nsfw"], url = img_url)
        neko_embed.set_image(img_url);
        neko_embed.set_footer(text = f"Sent at {timestamp} || Scraped from https://nekos.life/lewd");

        await ctx.send(embed = neko_embed)
    else:
      error_embed = discord.Embed(title = "***error:***", description = "*error - `this command can only be used in NSFW channels.`*", color = colors['err'])

      await ctx.send(embed = error_embed);

@bot.command(name = "hentai")
async def hentai(ctx, *args):
    gb = Gel();
    if ctx.channel.nsfw:
        if len(args) < 1:
            posts = await gb.search_posts(tags = ["hentai"], exclude_tags = ["video", "mp4"]);
            img_url = random.choice(posts);

        else:
            posts = await gb.search_posts(tags = args, exclude_tags = ["video", "mp4"]);
            img_url = random.choice(posts);
        
        hentai_embed = discord.Embed(title = "***Hentai:***", color = colors["nsfw"], url = img_url);
        hentai_embed.set_image(img_url);
        hentai_embed.set_footer(text = f"Sent at {timestamp} || Scraped from https://gelbooru.com");

        await ctx.send(embed = hentai_embed);
    else:
        error_embed = discord.Embed(title = "***error:***", description = "*error - `this command can only be used in NSFW channels.`*", color = colors['err'])

        await ctx.send(embed = error_embed);
# END OF COMMANDS #

# COGS #
ping_server();
bot.run(os.environ["TOKEN"]); 