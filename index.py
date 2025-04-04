import os

import discord
from discord.ext import commands
from discord import app_commands
import deepl
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_TOKEN")


intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

translator = deepl.Translator(DEEPL_API_KEY)

flag_to_lang = {
    "🇫🇷": "FR", "🇬🇧": "EN-GB", "🇺🇸": "EN-US", "🇩🇪": "DE", "🇪🇸": "ES",
    "🇮🇹": "IT", "🇵🇹": "PT-PT", "🇳🇱": "NL", "🇷🇺": "RU", "🇯🇵": "JA",
    "🇰🇷": "KO", "🇨🇳": "ZH", "🇮🇳": "HI", "🇹🇷": "TR"
}


message_cache = {}

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_cache[message.id] = message.content
    print(f"💾 Message enregistré : {message.id} → {message.content}")

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji = reaction.emoji
    message = reaction.message

    print(f"🔄 Réaction détectée : {emoji} par {user.name} sur '{message.content}'")

    if emoji in flag_to_lang and message.id in message_cache:
        target_lang = flag_to_lang[emoji]
        original_text = message_cache[message.id]

        try:
            translated_text = translator.translate_text(original_text, target_lang=target_lang).text

            await message.reply(f"🔹 **Traduction ({emoji}) :** {translated_text}")
        except Exception as e:
            await message.reply(f"⚠️ Erreur de traduction : {str(e)}")

@bot.tree.command(name="remaining", description="Envoie le nombre d'utilisation de l'API Deepl restante.")
@app_commands.describe()
async def remaining(interaction: discord.Interaction):
    try:
        remain = translator.get_usage()
        remaining = (str(remain).split(" "))[4]
        max = (str(remain).split(" "))[6]
        await interaction.response.send_message(f"Il reste : {int(max)-int(remaining)} caractère a pouvoir traduire")
    except Exception as e:
        await interaction.response.send_message(f"An Error occured : {str(e)}.\nPlease contact <@584680265134243854>")

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées : {synced}")
        print(f"Connecté en tant que {bot.user}")
    except Exception as e:
        print(f"Erreur de synchronisation : {e}")




bot.run(TOKEN)