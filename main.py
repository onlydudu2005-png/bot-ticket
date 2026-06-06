import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f"✅ Logado como {bot.user}")

async def main():
    try:
        async with bot:
            await bot.load_extension("ticket")
            print("✅ ticket.py carregado")
            await bot.start(TOKEN)

    except Exception as e:
        print(f"❌ ERRO: {e}")
        input("Pressione Enter...")

asyncio.run(main())

bot.run(TOKEN)