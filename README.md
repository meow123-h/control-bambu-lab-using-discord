**Control your **Bambu Lab printer** from Discord using MQTT.**

This bot allows you to:
 Check printer status
 
 **Start prints** 

 **Pause prints**
 
 **Stop prints**
 
 **View temperature info**

**And more!**

_Tested with:
 Bambu Lab A1 Mini
 Python 3.10+
 Discord.py
Paho MQTT
_
---

 ⚙️ Requirements

- Python 3.10 or newer
- A Discord Bot Token
- Bambu Lab printer on same network
- Printer Access Code (from Bambu Studio)**

Install dependencies:


pip install discord.py paho-mqtt

Setup
1. Clone the repo
   
using this "git clone https://github.com/meow123-h/control-bambu-lab-using-discord.git"



1. Edit the config section

Open bambu_discord_bot.py and edit:

DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
PRINTER_IP = "192.168.X.XXX"
ACCESS_CODE = "YOUR_BAMBU_ACCESS_CODE"

3️ Run the bot
python bambu_discord_bot.py

If successful, you should see:

Bot is online!
Connected to printer.
💬 Discord Commands



Example commands:

!status
!pause
!resume
!stop
!temps

(Commands depend on your implementation)



🔐 Security Warning



⚠️ Never upload your real:

Discord Bot Token

Printer Access Code

IP Address



The bot connects to your Bambu printer using MQTT.

