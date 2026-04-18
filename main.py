from flask import Flask, render_template, request, jsonify
import discord
from discord.ext import commands
import threading

app = Flask(__name__)

def run_bot(token, source_id, target_id):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Бот іске қосылды: {bot.user}")
        source_guild = bot.get_guild(int(source_id))
        target_guild = bot.get_guild(int(target_id))
        
        if source_guild and target_guild:
            print("Көшіру басталды...")
            for channel in source_guild.channels:
                try:
                    if isinstance(channel, discord.TextChannel):
                        await target_guild.create_text_channel(channel.name)
                    elif isinstance(channel, discord.VoiceChannel):
                        await target_guild.create_voice_channel(channel.name)
                except:
                    continue
            print("Дайын!")
        await bot.close()

    bot.run(token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clone', methods=['POST'])
def clone():
    data = request.json
    thread = threading.Thread(target=run_bot, args=(data['token'], data['source'], data['target']))
    thread.start()
    return jsonify({"status": "Success", "message": "Бот жіберілді! Бірнеше минут күте тұрыңыз..."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

