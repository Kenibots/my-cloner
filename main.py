import discord
from discord.ext import commands
from flask import Flask, render_template, request, jsonify
import threading
import asyncio

app = Flask(__name__)

async def clone_task(token, s_id, t_id):
    # self_bot=True маңызды!
    bot = commands.Bot(command_prefix=".", self_bot=True)

    @bot.event
    async def on_ready():
        try:
            source = bot.get_guild(int(s_id))
            target = bot.get_guild(int(t_id))
            
            if source and target:
                # Очистка
                for c in target.channels: await c.delete()
                # Роли
                for r in reversed(source.roles):
                    if r.name != "@everyone":
                        try: await target.create_role(name=r.name, color=r.color, permissions=r.permissions)
                        except: continue
                # Каналы
                for cat in source.categories:
                    new_cat = await target.create_category(name=cat.name)
                    for ch in cat.channels:
                        if isinstance(ch, discord.TextChannel): await new_cat.create_text_channel(name=ch.name)
                        elif isinstance(ch, discord.VoiceChannel): await new_cat.create_voice_channel(name=ch.name)
            await bot.close()
        except:
            await bot.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clone', methods=['POST'])
def clone():
    data = request.json
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(clone_task(data['token'], data['source'], data['target']))
    threading.Thread(target=run).start()
    return jsonify({"status": "Success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    
