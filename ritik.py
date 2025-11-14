import telebot
import os
import time
import random
import threading

# Bot Token
token = "8565663576:AAFnaC-qxL2WC0ELRRk8wJhDS_86BJm23gwM"
bot = telebot.TeleBot(token)

APPROVED_USERS_FILE = "approved_users.txt"
RITIK_FILE = "ritik.txt"  # New file for ritik
approved_users = []
admins = [6437994839]
owner_id = 6437994839
stop_gali = False

CHANNEL_LINK = "https://t.me/+9JdOjZL-vko5MmRl"
GROUP_LINK = "https://t.me/+mv4H3ozeHD82ZDM1"
OWNER_LINK = "https://t.me/Ritikxyz099"

def load_approved_users():
    users = []
    if os.path.exists(APPROVED_USERS_FILE):
        with open(APPROVED_USERS_FILE, "r") as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) == 2:
                    users.append({'id': int(data[0]), 'username': data[1]})
    return users

def save_approved_users():
    with open(APPROVED_USERS_FILE, "w") as f:
        for user in approved_users:
            f.write(f"{user['id']},{user['username']}\n")

def init_ritik_file():
    """Initialize ritik.txt file if it doesn't exist"""
    if not os.path.exists(RITIK_FILE):
        with open(RITIK_FILE, "w", encoding="utf-8") as f:
            f.write("This is ritik.txt file\nCreated automatically by the bot\n")
        print(f"✅ {RITIK_FILE} created successfully!")
    else:
        print(f"✅ {RITIK_FILE} already exists!")

def read_ritik_file():
    """Read content from ritik.txt"""
    try:
        with open(RITIK_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_to_ritik_file(content):
    """Write content to ritik.txt"""
    try:
        with open(RITIK_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def append_to_ritik_file(content):
    """Append content to ritik.txt"""
    try:
        with open(RITIK_FILE, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return True
    except Exception as e:
        return False

# Initialize files
approved_users = load_approved_users()
init_ritik_file()  # Create ritik.txt when bot starts

# ... (rest of your existing code remains the same until commands section)

@bot.message_handler(commands=["start"])
def welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    name = message.from_user.first_name

    if any(user['id'] == user_id for user in approved_users) or user_id in admins or user_id == owner_id:
        bot.reply_to(message,
            "✨ 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙏𝙝𝙚 𝙐𝙡𝙩𝙞𝙢𝙖𝙩𝙚 𝙂𝙖𝙡𝙞 𝘽𝙤𝙩 ✨\n\n"
            "👑 Owner Commands:\n"
            "- /admin <user_id>\n"
            "- /remove_admin <user_id>\n"
            "- /list_admins\n\n"
            "🛡️ Admin Commands:\n"
            "- /approve <user_id>\n"
            "- /remove <user_id>\n"
            "- /remove_all\n"
            "- /list_approved\n\n"
            "📁 File Commands:\n"
            "- /ritik_read - Read ritik.txt\n"
            "- /ritik_write <text> - Write to ritik.txt\n"
            "- /ritik_append <text> - Append to ritik.txt\n\n"
            "🔥 User Commands:\n"
            "- /fuck <username>\n"
            "- /stop\n"
            "- /ping"
        )
    else:
        bot.send_message(user_id,
            f"⚠️ To use this bot, follow these steps:\n\n"
            f"1️⃣ Join our Channel 👉 [Join Channel]({CHANNEL_LINK})\n"
            f"2️⃣ Join our Group 👉 [Join Group]({GROUP_LINK})\n"
            f"3️⃣ After joining, send a DM to the owner.\n\n"
            f"👑 Owner: [Click to DM]({OWNER_LINK})\n\n"
            f"⏳ Once approved, you'll be able to use the bot features.",
            parse_mode="Markdown")

        if user_id != owner_id:
            try:
                bot.send_message(owner_id, f"👤 New user started the bot:\n• Name: {name}\n• Username: @{username}\n• ID: `{user_id}`", parse_mode="Markdown")
            except:
                pass

# New commands for ritik.txt file management
@bot.message_handler(commands=["ritik_read"])
def ritik_read(message):
    if message.from_user.id not in [u['id'] for u in approved_users] and message.from_user.id not in admins and message.from_user.id != owner_id:
        bot.reply_to(message, "🚫 You are not approved to use this command.")
        return
    
    content = read_ritik_file()
    if len(content) > 4000:  # Telegram message limit
        content = content[:4000] + "\n\n... (content truncated)"
    
    bot.reply_to(message, f"📄 Content of ritik.txt:\n\n{content}")

@bot.message_handler(commands=["ritik_write"])
def ritik_write(message):
    if message.from_user.id not in admins and message.from_user.id != owner_id:
        bot.reply_to(message, "🚫 Only admins can write to ritik.txt")
        return
    
    text = message.text.replace('/ritik_write', '').strip()
    if not text:
        bot.reply_to(message, "Usage: /ritik_write <text>")
        return
    
    if write_to_ritik_file(text):
        bot.reply_to(message, "✅ Successfully wrote to ritik.txt")
    else:
        bot.reply_to(message, "❌ Failed to write to ritik.txt")

@bot.message_handler(commands=["ritik_append"])
def ritik_append(message):
    if message.from_user.id not in [u['id'] for u in approved_users] and message.from_user.id not in admins and message.from_user.id != owner_id:
        bot.reply_to(message, "🚫 You are not approved to use this command.")
        return
    
    text = message.text.replace('/ritik_append', '').strip()
    if not text:
        bot.reply_to(message, "Usage: /ritik_append <text>")
        return
    
    if append_to_ritik_file(text):
        bot.reply_to(message, "✅ Successfully appended to ritik.txt")
    else:
        bot.reply_to(message, "❌ Failed to append to ritik.txt")

# ... (rest of your existing commands remain the same)

print("Bot is running...")
print(f"Checking {RITIK_FILE}...")
init_ritik_file()  # Ensure file exists when bot starts
bot.infinity_polling()
