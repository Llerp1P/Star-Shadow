import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def rename(ctx, member: discord.Member, *, new_name: str):
    try:
        await member.edit(
            nick=new_name,
            reason=f"Changed by {ctx.author}"
        )

        await ctx.send(
            f"{member.mention} のサーバーニックネームを\n"
            f"『{new_name}』に変更しました。"
        )

    except discord.Forbidden:
        await ctx.send(
            "権限不足です。\n"
            "BOTのロールを対象ユーザーより上にしてください。"
        )

    except Exception as e:
        await ctx.send(f"エラー: {e}")

bot.run(TOKEN)
