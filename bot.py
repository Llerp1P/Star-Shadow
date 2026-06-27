import os
import discord
from discord import app_commands

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.guilds = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.tree.command(
    name="rename",
    description="ユーザーのサーバーニックネームを変更します"
)
@app_commands.describe(
    member="名前を変更するユーザー",
    new_name="新しいニックネーム"
)
async def rename(
    interaction: discord.Interaction,
    member: discord.Member,
    new_name: str
):
    if not interaction.user.guild_permissions.manage_nicknames:
        await interaction.response.send_message(
            "❌ ニックネーム変更権限がありません。",
            ephemeral=True
        )
        return

    try:
        await member.edit(
            nick=new_name,
            reason=f"Changed by {interaction.user}"
        )

        await interaction.response.send_message(
            f"✅ {member.mention} の名前を「{new_name}」に変更しました。"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ BOTのロールを対象ユーザーより上に配置してください。",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ エラー: {e}",
            ephemeral=True
        )

client.run(TOKEN)
