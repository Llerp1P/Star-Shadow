import os
import discord
from discord import app_commands

# =====================
# CONFIG
# =====================

TOKEN = os.environ["TOKEN"]

# あなたのサーバーID
GUILD_ID = 1497104058987708547

# =====================
# INTENTS
# =====================

intents = discord.Intents.default()
intents.guilds = True

# =====================
# CLIENT
# =====================

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        print("[SETUP] setup_hook started")

        guild = discord.Object(id=GUILD_ID)

        try:
            synced = await self.tree.sync(guild=guild)

            print(
                f"[SETUP] Synced {len(synced)} command(s) "
                f"to guild {GUILD_ID}"
            )

            for cmd in synced:
                print(f"[COMMAND] /{cmd.name}")

        except Exception as e:
            print(f"[ERROR] Command sync failed: {e}")

client = MyClient()

# =====================
# READY
# =====================

@client.event
async def on_ready():
    print("=" * 50)
    print("[READY] Bot connected")
    print(f"[READY] Logged in as {client.user}")
    print(f"[READY] User ID: {client.user.id}")

    print("[READY] Guilds:")
    for guild in client.guilds:
        print(f" - {guild.name} ({guild.id})")

    print("=" * 50)

# =====================
# COMMAND
# =====================

@client.tree.command(
    name="rename",
    description="ユーザーのニックネームを変更します"
)
@app_commands.guilds(discord.Object(id=GUILD_ID))
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

        print(
            f"[RENAME] "
            f"{interaction.user} -> "
            f"{member} = {new_name}"
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
        print(f"[ERROR] {e}")

        await interaction.response.send_message(
            f"❌ エラー: {e}",
            ephemeral=True
        )

# =====================
# START
# =====================

print("[BOOT] Starting bot...")
client.run(TOKEN)
