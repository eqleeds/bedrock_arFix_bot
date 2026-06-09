import os
import telebot
from arabic_reshaper import reshape
from bidi.algorithm import get_display

API_TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not API_TOKEN:
    print("Error: TELEGRAM_TOKEN environment variable is missing!")
    exit(1)

bot = telebot.TeleBot(API_TOKEN)
print("Arabic Bedrock Chat Fixer with Tellraw formatting is running...")

@bot.message_handler(func=lambda message: True)
def fix_arabic_chat(message):
    user_text = message.text
    
    # Check if the user included a username prefix (e.g., "Amirkh888: message")
    if ":" in user_text:
        parts = user_text.split(":", 1)
        username = parts[0].strip() + ": "
        actual_message = parts[1].strip()
    else:
        # Default fallback if you just type text without a username
        username = "Server: "
        actual_message = user_text
        
    try:
        # Step 1: Contextually shape connected Arabic letters
        reshaped_text = reshape(actual_message)
        
        # Step 2: Reverse the string text direction for Bedrock
        fixed_text = get_display(reshaped_text)
        
        # Step 3: Construct the exact Minecraft tellraw command structure
        # We escape quotes properly so the server console accepts it without syntax errors
        tellraw_command = f'/exec tellraw @a[team=1] ["",{{\"text\":\"{username}\",\"color\":\"dark_aqua\"}},{{\"text\":\"{fixed_text}\",\"color\":\"white\"}}]'
        
        # Step 4: Reply with the exact command inside a clickable copy box
        bot.reply_to(message, f"```\n{tellraw_command}\n
```", parse_mode='MarkdownV2')
        
    except Exception as e:
        print(f"Error handling message: {e}")
        bot.reply_to(message, "An error occurred while formatting.")

bot.polling(none_stop=True)
