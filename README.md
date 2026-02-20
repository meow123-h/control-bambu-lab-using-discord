# _**Control your **Bambu Lab printer** from Discord using MQTT.**_

This bot allows you to:
 Check printer status
 
 **Start prints** 

 **Pause prints**
 
 **Stop prints**
 
 **View temperature info**

**And more!** 

Tested with:
* Bambu Lab A1 Mini
* Python 3.10+
 *Discord.py
*Paho MQTT



 ⚙️ Requirements

- Python 3.10 or newer
- A Discord Bot Token
- Bambu Lab printer on same network
- Printer Access Code (from Bambu Studio)**

Install dependencies:


pip install discord.py paho-mqtt

Setup
**1.** Clone the repo. using this "git clone https://github.com/meow123-h/control-bambu-lab-using-discord.git"

**2.** Edit the config section

Open bambu_discord_bot.py and edit:

DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
PRINTER_IP = "192.168.X.XXX"
ACCESS_CODE = "YOUR_BAMBU_ACCESS_CODE"

**3️.** Run the bot
python bambu_discord_bot.py.
If successful, you should see:

"Bot is online!
Connected to printer.


💬 Discord Commands


 Bambu Discord Bot – Command Cheat Sheet
 Lighting
!light on
!light off


Print Control
!pause
!resume
!stop
!force stop


!pause – pauses the current print

!resume – resumes a paused print

!stop – asks for confirmation

!force stop – immediately stops the print

Speed Modes
!speed normal
!speed sport
!speed ludicrous


Changes print speed on the fly.

 Temperatures
!temp


Shows current nozzle & bed temperatures.

 Progress & Time
!progress


Shows:

% complete

Elapsed time

Time remaining

Full Status
!status


One message with:

Print state

Temps

Progress

Remaining time

 Fan Control
!fan 100
!fan 75
!fan 50
!fan off


Controls the part cooling fan.

 Emergency Kill Switch
!kill


Immediately:

Stops the print

Turns lights off

Shuts everything down



 Automatic Alerts (No Commands Needed)

The bot will automatically send messages when:

Print starts / resumes

Print pauses

Print finishes

 Print fails or stops

Alerts are sent to:

 Your Discord channel

 Your DMs

 Quick Test Sequence



 **Security Warning**


 Never upload your real:

Discord Bot Token

Printer Access Code

IP Address



The bot connects to your Bambu printer using MQTT.

