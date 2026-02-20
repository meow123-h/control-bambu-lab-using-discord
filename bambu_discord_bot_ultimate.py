import discord
import paho.mqtt.client as mqtt
import ssl, json, time, asyncio

# ================= CONFIG =================
DISCORD_TOKEN = "MTQ2NzQwMzA3MzQ5OTQzNTA4MA.GxVq6B.V7cMO8Eh1Lcova51qTkiakf7p1xdvtVALvt_M8"
PRINTER_IP = "192.168.20.13"
PRINTER_SERIAL = "0309EA450600045"
ACCESS_CODE = "46729066"
ALLOWED_USER_ID = 1108331129292980284
ALERT_CHANNEL_ID = 1349634122502639638
# ==========================================

# ---------- PRINTER STATE ----------
printer_state = {
    "nozzle": "?",
    "bed": "?",
    "progress": "?",
    "remain": "?",
    "print_state": "Unknown",
    "fan_speed": "?"
}

# ---------- DISCORD ----------
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot online as {bot.user}")
    channel = bot.get_channel(ALERT_CHANNEL_ID)
    if channel:
        await channel.send("🟢 **Printer Bot Connected & Ready**")

# ---------- MQTT ----------
bambu = mqtt.Client(client_id=f"discord_{int(time.time())}")
bambu._callback_api_version = mqtt.CallbackAPIVersion.VERSION1 
bambu.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)
bambu.tls_insecure_set(True)
bambu.username_pw_set("bblp", ACCESS_CODE)

def send_cmd(cat, cmd, extra={}):
    payload = {
        cat: {
            "sequence_id": "0",
            "command": cmd,
            **extra
        }
    }
    topic = f"device/{PRINTER_SERIAL}/request"
    bambu.publish(topic, json.dumps(payload))

def on_connect(c, u, f, rc):
    if rc == 0:
        print("✅ MQTT Connected")
        c.subscribe(f"device/{PRINTER_SERIAL}/report")
        send_cmd("pushing", "pushall")
    else:
        print(f"❌ MQTT Failed: {rc}")

def on_message(c, u, msg):
    try:
        data = json.loads(msg.payload.decode())
        rpt = data.get("print", {})
        
        if "nozzle_temper" in rpt: printer_state["nozzle"] = rpt["nozzle_temper"]
        if "bed_temper" in rpt: printer_state["bed"] = rpt["bed_temper"]
        if "mc_percent" in rpt: printer_state["progress"] = rpt["mc_percent"]
        if "mc_remaining_time" in rpt: printer_state["remain"] = rpt["mc_remaining_time"]
        if "gcode_state" in rpt: 
            old_state = printer_state["print_state"]
            new_state = rpt["gcode_state"]
            printer_state["print_state"] = new_state
            
            # Simple State Alert
            if old_state != new_state and new_state in ["FINISH", "FAILED"]:
                 asyncio.run_coroutine_threadsafe(
                    alert_state(new_state), bot.loop
                )

    except:
        pass

async def alert_state(state):
    channel = bot.get_channel(ALERT_CHANNEL_ID)
    if channel:
        await channel.send(f"🔔 **Print Status Update:** {state}")

bambu.on_connect = on_connect
bambu.on_message = on_message
bambu.connect(PRINTER_IP, 8883, 60)
bambu.loop_start()

# ---------- COMMANDS ----------
@bot.event
async def on_message(message):
    if message.author == bot.user: return
    # Safety: Only you or people with admin perms
    # if message.author.id != ALLOWED_USER_ID: return 

    c = message.content.lower()

    # 💡 LIGHT
    if c == "!light on":
        send_cmd("system", "ledctrl", {"led_node": "chamber_light", "led_mode": "on", "led_on_time": 500, "led_off_time": 500, "loop_times": 0, "interval_time": 0})
        await message.channel.send("💡 Light ON")
    elif c == "!light off":
        send_cmd("system", "ledctrl", {"led_node": "chamber_light", "led_mode": "off", "led_on_time": 500, "led_off_time": 500, "loop_times": 0, "interval_time": 0})
        await message.channel.send("🌑 Light OFF")

    # ▶️ PRINT CONTROL
    elif c == "!pause":
        send_cmd("print", "pause")
        await message.channel.send("⏸️ Paused")
    elif c == "!resume":
        send_cmd("print", "resume")
        await message.channel.send("▶️ Resumed")
    elif c == "!force stop":
        send_cmd("print", "stop")
        await message.channel.send("🛑 STOPPED")
    
    # 🏎️ SPEED
    elif c == "!speed normal":
        send_cmd("print", "print_speed", {"param": "2"})
        await message.channel.send("🏎️ Speed: Normal")
    elif c == "!speed sport":
        send_cmd("print", "print_speed", {"param": "3"})
        await message.channel.send("🏎️ Speed: SPORT MODE")
    elif c == "!speed ludicrous":
        send_cmd("print", "print_speed", {"param": "4"})
        await message.channel.send("🚀 Speed: LUDICROUS MODE")
        
    # 🌬️ FAN
    elif c.startswith("!fan"):
        try:
            val = c.split(" ")[1]
            speed = 0 if val == "off" else int(val)
            # Bambu fan speed is 0-15 (for some fans) or 0-255 (percentage mapping)
            # We will use the common G-code style 0-255 mapping approx
            real_val = int((speed / 100) * 255)
            send_cmd("print", "gcode_line", {"sequence_id": "0", "command": f"M106 P1 S{real_val}"}) 
            # Note: M106 P1 is usually part fan. P2 is Aux. P3 is Chamber. 
            # This is experimental on Bambu MQTT, sometimes 'fan_ctrl' is better.
            await message.channel.send(f"🌬️ Fan set to {speed}%")
        except:
            await message.channel.send("Usage: !fan 100 or !fan off")

    # 🌡️ TEMPS
    elif c == "!temp":
        send_cmd("pushing", "pushall") # refresh
        await asyncio.sleep(0.5)
        await message.channel.send(f"🌡️ Nozzle: `{printer_state['nozzle']}°C` | Bed: `{printer_state['bed']}°C`")

    # 📊 PROGRESS
    elif c == "!progress":
        send_cmd("pushing", "pushall")
        await asyncio.sleep(0.5)
        await message.channel.send(f"📊 Progress: `{printer_state['progress']}%` | Time Left: `{printer_state['remain']} min`")

    # 🧠 STATUS
    elif c == "!status":
        send_cmd("pushing", "pushall")
        await asyncio.sleep(0.5)
        await message.channel.send(
            f"📊 **STATUS**\n"
            f"State: `{printer_state['print_state']}`\n"
            f"Temps: `{printer_state['nozzle']}°C` / `{printer_state['bed']}°C`\n"
            f"Progress: `{printer_state['progress']}%`\n"
            f"Time Left: `{printer_state['remain']} min`"
        )
        
    # 🚨 KILL
    elif c == "!kill":
        send_cmd("print", "stop")
        send_cmd("system", "ledctrl", {"led_node": "chamber_light", "led_mode": "off"})
        await message.channel.send("🚨 **EMERGENCY KILL TRIGGERED** 🚨")

bot.run(DISCORD_TOKEN)
