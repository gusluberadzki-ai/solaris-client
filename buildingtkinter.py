import tkinter as tk 
from tkinter import messagebox
from tkinter import font
from tkinter import simpledialog
import math
import os
import random
import time  
from datetime import datetime





TAB = tk.Tk()
TAB.title("Tactical Nuclear Launch Control")
TAB.configure(bg="#1a1a1a")
TAB.attributes("-fullscreen", True)

custom_font = font.Font(family="Airborne 86", size=24, weight="bold")

# Readiness strip
status_strip = tk.Frame(TAB, bg="#070707")
status_strip.pack(fill="x", side="top")
strip_labels = {}
for text in ("Officer 1", "Officer 2", "Launch code"):
    lbl = tk.Label(status_strip, text=f"{text}: waiting", font=("Airborne 86", 10, "bold"), fg="#ff5555", bg="#070707")
    lbl.pack(side="left", padx=12, pady=4)
    strip_labels[text] = lbl

# Layout frame for main content and console
main_frame = tk.Frame(TAB, bg="#1a1a1a")
main_frame.pack(fill="both", expand=True)

# Left side: credentials
cred_frame = tk.Frame(main_frame, bg="#1a1a1a")
cred_frame.pack(side="left", fill="both", expand=True)

label = tk.Label(cred_frame, text="TACTICAL NUCLEAR LAUNCH CONTROL", font=custom_font, fg="#00FF00", bg="#1a1a1a")
label.pack(pady=30)

# Officer 1
officer1_label = tk.Label(cred_frame, text="Officer 1 Name and Surname:", font=("Airborne 86", 18), fg="white", bg="#1a1a1a")
officer1_label.pack()
officer1_entry = tk.Entry(cred_frame, font=("Airborne 86", 18), width=30, bg="#222222", fg="white", insertbackground="white")
officer1_entry.pack(pady=5)
officer1_led = tk.Label(cred_frame, text="●", font=("Airborne 86", 14), fg="#440000", bg="#1a1a1a")
officer1_led.pack(pady=(0, 8))

# Officer 2
officer2_label = tk.Label(cred_frame, text="Officer 2 Name and Surname:", font=("Airborne 86", 18), fg="white", bg="#1a1a1a")
officer2_label.pack()
officer2_entry = tk.Entry(cred_frame, font=("Airborne 86", 18), width=30, bg="#222222", fg="white", insertbackground="white")
officer2_entry.pack(pady=5)
officer2_led = tk.Label(cred_frame, text="●", font=("Airborne 86", 14), fg="#440000", bg="#1a1a1a")
officer2_led.pack(pady=(0, 8))

# Destination
destination_label = tk.Label(cred_frame, text="Target Destination:", font=("Airborne 86", 18), fg="white", bg="#1a1a1a")
destination_label.pack()
destination_entry = tk.Entry(cred_frame, font=("Airborne 86", 18), width=30, bg="#222222", fg="white", insertbackground="white")
destination_entry.pack(pady=5)

# Coordinates
coord_label = tk.Label(cred_frame, text="Target Coordinates (Lat, Long):", font=("Airborne 86", 18), fg="white", bg="#1a1a1a")
coord_label.pack()
coord_entry = tk.Entry(cred_frame, font=("Airborne 86", 18), width=30, bg="#222222", fg="white", insertbackground="white")
coord_entry.pack(pady=5)

# Launch overview (higher, compact)
launch_frame = tk.Frame(cred_frame, bg="#050505", bd=1, relief="solid")
launch_frame.pack(padx=14, pady=(10, 6))
launch_title = tk.Label(launch_frame, text="TARGET OVERVIEW", font=("Airborne 86", 12, "bold"), fg="#00FF00", bg="#050505")
launch_title.pack(pady=(6, 4))

# move the single launch code entry into the launch frame so that it appears
# above the button per the original layout
officer1_code_label = tk.Label(launch_frame, text="Launch Code:", font=("Airborne 86", 16), fg="white", bg="#050505")
officer1_code_label.pack(pady=(4,2))
officer1_code_frame = tk.Frame(launch_frame, bg="#050505")
officer1_code_entry = tk.Entry(officer1_code_frame, font=("Airborne 86", 16), width=20, bg="#222222", fg="white", insertbackground="white", show="*")
officer1_code_entry.pack(side="left", pady=3)
officer1_code_led = tk.Label(officer1_code_frame, text="●", font=("Airborne 86", 12), fg="#440000", bg="#050505")
officer1_code_led.pack(side="left", padx=(8, 0))
officer1_code_frame.pack(pady=3)
def perform_launch():
    # first confirmation dialog
    if not messagebox.askyesno("Confirm Launch", "Are you sure you want to send the missile?"):
        log_console("Launch aborted by operator.")
        return

    # second dialog: siren option
    play_siren = False
    if messagebox.askyesno("Sirens", "Enable siren during countdown?"):
        play_siren = True

    # pre‑countdown events
    log_console("Bay doors opening...")
    log_console("Thrusters primed.")

    # Countdown sequence before launch; add ellipses to each line
    for t in range(10, 0, -1):
        log_console(f"T-MINUS {t} ...")
        TAB.update()
        time.sleep(1)

    log_console("*** LAUNCH INITIATED ***")
    append_mission_log("Launch button pressed.", severity="action")

    # final missile departure message
    log_console("Missile away!")

    # optionally play a siren sound from the user's Documents folder
    if play_siren:
        path = os.path.expanduser("~/Documents/siren.mp3")
        if os.path.exists(path):
            os.system(f"afplay '{path}' >/dev/null 2>&1 &")
        else:
            log_console("Siren file not found: " + path)

    # after launch we disable the button so it can't be pressed twice
    launch_button.config(state="disabled")

launch_button = tk.Button(launch_frame, text="LAUNCH", font=("Airborne 86", 24, "bold"), fg="white", bg="#0b0b0b", activebackground="#222222", relief="raised", bd=3, state="disabled", width=20, command=perform_launch)
launch_button.pack(pady=(0, 10), padx=48)
target_map_label = tk.Label(launch_frame, text="Target: N/A", font=("Airborne 86", 10), fg="#00FF00", bg="#050505")
target_map_label.pack(pady=(0, 6))

radar_widget_size = 120
radar_frame = tk.Frame(cred_frame, bg="#0b0b0b", bd=1, relief="solid")
radar_frame.pack(padx=14, pady=(4, 12))
radar_title = tk.Label(radar_frame, text="SENSOR ROTOR", font=("Airborne 86", 10, "bold"), fg="#00FF00", bg="#0b0b0b")
radar_title.pack(pady=(6, 2))
radar_canvas = tk.Canvas(radar_frame, width=radar_widget_size, height=radar_widget_size, bg="#050505", highlightthickness=0)
radar_canvas.pack(padx=6, pady=(0, 4))
radar_status_label = tk.Label(radar_frame, text="Sweep idle", font=("Airborne 86", 9), fg="#00FF00", bg="#0b0b0b")
radar_status_label.pack(pady=(0, 2))
radar_ping_label = tk.Label(radar_frame, text="Ping streak: 0", font=("Airborne 86", 9), fg="#00FF00", bg="#0b0b0b")
radar_ping_label.pack(pady=(0, 4))
radar_alert_flash = tk.Label(radar_frame, text="", font=("Airborne 86", 10, "bold"), fg="#ff5555", bg="#0b0b0b")
radar_alert_flash.pack(pady=(0, 2))

"""(launch code widgets were moved into the launch_frame above)
    The old copy remained here; it is no longer needed.
"""

# Console terminal on the right
console_frame = tk.Frame(main_frame, bg="black")
console_frame.pack(side="right", fill="y")
console_label = tk.Label(console_frame, text="TACTICAL LAUNCH CONSOLE", font=("Airborne 86", 16, "bold"), fg="#00FF00", bg="black")
console_label.pack(pady=5)

hud_frame = tk.Frame(console_frame, bg="#050505", highlightbackground="#00FF00", highlightthickness=1)
hud_frame.pack(padx=10, pady=(0, 8), fill="x")
hud_title = tk.Label(hud_frame, text="IMPACT HUD", font=("Airborne 86", 12, "bold"), fg="#00FF00", bg="#050505")
hud_title.pack(pady=(6, 0))
HUD_WIDTH = 160
HUD_HEIGHT = 160
hud_canvas = tk.Canvas(hud_frame, width=HUD_WIDTH, height=HUD_HEIGHT, bg="#050505", highlightthickness=0)
hud_canvas.pack(padx=5, pady=(4, 2))
hud_info = tk.Label(hud_frame, text="Heading: N/A", font=("Airborne 86", 10), fg="#00FF00", bg="#050505")
hud_info.pack(pady=(0, 4))
hud_impact = tk.Label(hud_frame, text="Impact: N/A", font=("Airborne 86", 10), fg="#00FF00", bg="#050505")
hud_impact.pack(pady=(0, 6))

status_frame = tk.Frame(console_frame, bg="#050505")
status_frame.pack(padx=10, pady=(0, 6), fill="x")

bio_frame = tk.Frame(status_frame, bg="#0b0b0b", bd=1, relief="solid")
bio_frame.pack(side="left", expand=True, fill="both", padx=4)
bio_title = tk.Label(bio_frame, text="BIOMETRIC SECURE", font=("Airborne 86", 10, "bold"), fg="#00FF00", bg="#0b0b0b")
bio_title.pack(pady=(4, 2))
biometric_status = tk.Label(bio_frame, text="Biometric: STANDBY", font=("Airborne 86", 10), fg="#00FF00", bg="#0b0b0b")
biometric_status.pack(pady=(2, 4))
badge_frame = tk.Frame(bio_frame, bg="#0b0b0b")
badge_frame.pack(fill="x", pady=(0, 4))
badge_officer1 = tk.Label(badge_frame, text="Officer 1: OFF", font=("Airborne 86", 9), fg="#00FF00", bg="#141414")
badge_officer1.pack(side="left", expand=True, fill="x", padx=(2, 1))
badge_officer2 = tk.Label(badge_frame, text="Officer 2: OFF", font=("Airborne 86", 9), fg="#00FF00", bg="#141414")
badge_officer2.pack(side="left", expand=True, fill="x", padx=(1, 2))
seal_frame = tk.Frame(bio_frame, bg="#0b0b0b")
seal_frame.pack(fill="x", pady=(0, 4))
seal_label = tk.Label(seal_frame, text="Seal: STANDING BY", font=("Airborne 86", 8, "bold"), fg="#00FF00", bg="#0b0b0b")
seal_label.pack(pady=(2, 4))

mission_frame = tk.Frame(status_frame, bg="#050505")
mission_frame.pack(side="left", expand=True, fill="both", padx=4)
mission_title = tk.Label(mission_frame, text="MISSION LOG", font=("Airborne 86", 10, "bold"), fg="#00FF00", bg="#050505")
mission_title.pack(pady=(4, 2))
mission_log_text = tk.Text(mission_frame, font=("Courier", 9), fg="#00FF00", bg="#050505", height=6, bd=0, highlightthickness=0, wrap="none")
mission_log_text.pack(fill="both", expand=True, padx=2, pady=(0, 4))
mission_log_text.config(state="disabled")

comm_ticker = tk.Label(console_frame, text="Chatter standby...", font=("Airborne 86", 10), fg="#00FF00", bg="#050505")
comm_ticker.pack(padx=10, pady=(0, 6), fill="x")

console_text = tk.Text(console_frame, font=("Courier", 14), fg="#00FF00", bg="black", width=32, height=22, state="disabled")
console_text.pack(padx=10, pady=(0, 0))

console_entry = tk.Entry(console_frame, font=("Courier", 14), fg="#00FF00", bg="black", insertbackground="#00FF00")
console_entry.pack(padx=10, pady=(0, 10), fill="x")

"""The old version of this script used two separate officer launch codes.
For simplicity we now require only a single shared launch code.  The
operators enter the value into the first code field and the validation
logic ignores the second entry entirely.  This also makes the various
status labels behave as if there is a single "codes" check.
"""
LAUNCH_CODE = "NUKE2026"  # the single code that unlocks the launch
CODE_CONFIRM_TONE = "/System/Library/Sounds/Tink.aiff"

command_history = []
history_index = [0]
script_running = [False]
mission_log_entries = []
auth_states = ["STANDING BY", "SECOND AUTHORIZATION", "LAUNCH CODE VERIFIED", "LOCKED IN"]
auth_index = [0]
chatter_index = [0]
alert_ping_active = [False]
radar_angle = [0]
radar_dot_data = [None]
radar_radius = radar_widget_size / 2 - 8
radar_beam_width = 12
radar_spin_speed = 6
ping_streak = [0]
radar_alert_after = [None]
codes_confirmed = [False]
overwatch_window = [None]
ambient_tone_files = [
    "/System/Library/Sounds/Submarine.aiff",
    "/System/Library/Sounds/Glass.aiff",
    "/System/Library/Sounds/Tink.aiff"
]
ambient_index = [0]
radio_chatter_sounds = [
    "/System/Library/Sounds/Sosumi.aiff",
    "/System/Library/Sounds/Pop.aiff"
]
radio_chatter_index = [0]

SCRIPT_SEQUENCES = {
    "DIAGNOSTICS": [
        "Initializing diagnostics...",
        "Guidance system checksum verified.",
        "Thermal layers nominal.",
        "Flight computers synced.",
        "Redundant nav check passed.",
        "Targeting array locked.",
        "Diagnostics complete, all systems green."
    ],
    "DIAGNOSTICS FULL": [
        "Spooling sensor arrays (1/3)...",
        "Spooling sensor arrays (2/3)...",
        "Spooling sensor arrays (3/3)...",
        "Radar sweep alpha complete.",
        "Radar sweep beta complete.",
        "Telemetry cross-check stable.",
        "Diagnostics FULL complete."
    ],
    "THRUSTER CYCLE": [
        "Cycling thrusters (stage 1)...",
        "Cycling thrusters (stage 2)...",
        "Primary boosters online.",
        "Secondary boosters online.",
        "Thruster cycle complete."
    ],
    # simple launch sequence describing the main events seen in the old
    # version of the application.  the button handler will invoke this
    # script when the user confirms the launch.
    "LAUNCH": [
        # retained for console script compatibility, but actual
        # messages are emitted directly by perform_launch.
        "Launch sequence underway."
    ],
    "COMM CHECK": [
        "Broadcasting range beacon...",
        "Signal locked to command net.",
        "Telemetry streaming stable.",
        "Comm check success."
    ],
    "COMMUNICATIONS": [
        "Opening encrypted comm channel...",
        "Pacific relay online.",
        "Relay: 'Bravo Team holding, awaiting green-light.'",
        "Ack: 'Flight path stable, ready to proceed.'",
        "Channel secured."
    ],
    "COMM CHATTER": [
        "HQ: 'Weather is clear, proceed with caution.'",
        "Forward team: 'Radiation levels nominal.'",
        "Telecom: 'Repeating, telemetry link looks solid.'",
        "HQ: 'Maintain current heading until impact.'",
        "Chatter log complete."
    ],
    "RADAR": [
        "Overwatch map engaged.",
        "Plotting blast radius.",
        "Radar overlay complete."
    ]
}

chatter_messages = SCRIPT_SEQUENCES.get("COMM CHATTER", ["Comm net quiet."])

def log_console(msg):
    console_text.config(state="normal")
    console_text.insert("end", msg+"\n")
    console_text.see("end")
    console_text.config(state="disabled")


def play_code_confirmation_tone():
    os.system(f"afplay {CODE_CONFIRM_TONE} >/dev/null 2>&1 &")


def get_officer_code_state():
    # only the first code entry is used now; the second field is left on
    # the UI for historical/visual reasons but it no longer affects
    # authorization.  A match on the single LAUNCH_CODE is treated as
    # both codes having been entered correctly so existing callers don't
    # have to change.
    code = officer1_code_entry.get().strip().upper()
    match = code == LAUNCH_CODE
    # return values mirror the old signature (first, second, both)
    return match, match, match


def refresh_officer_code_feedback():
    match_first, match_second, both_matched = get_officer_code_state()
    officer1_code_led.config(fg="#00ff00" if match_first else "#440000")
    # second LED removed; match_second is ignored
    if both_matched and not codes_confirmed[0]:
        codes_confirmed[0] = True
        play_code_confirmation_tone()
    if not both_matched:
        codes_confirmed[0] = False
    return both_matched

def update_readiness_strip():
    ready1 = bool(officer1_entry.get().strip())
    ready2 = bool(officer2_entry.get().strip())
    officer_codes_ready = refresh_officer_code_feedback()
    def set_label(key, active):
        label = strip_labels[key]
        label.config(text=f"{key}: {'ready' if active else 'waiting'}", fg="#00ff00" if active else "#ff5555")
    set_label("Officer 1", ready1)
    set_label("Officer 2", ready2)
    # update the readiness strip; the third label now reflects the
    # single launch code requirement
    set_label("Launch code", officer_codes_ready)
    # enable the launch button only when both officers are named and the
    # correct code has been entered
    if ready1 and ready2 and officer_codes_ready:
        launch_button.config(state="normal")
    else:
        launch_button.config(state="disabled")

def replay_log_entry(command):
    if not command:
        return
    log_console(f"Replaying: {command}")
    execute_console_command(command)

def append_mission_log(entry, severity="info", command=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    display_text = f"[{timestamp}] {entry}"
    mission_log_entries.append({"text": display_text, "severity": severity, "command": command})
    if len(mission_log_entries) > 6:
        mission_log_entries.pop(0)
    mission_log_text.config(state="normal")
    mission_log_text.delete("1.0", "end")
    for idx, data in enumerate(mission_log_entries):
        tag_name = f"mission_entry_{idx}"
        color = {"info": "#00FF00", "warn": "#ff5555", "action": "#00bfff", "alert": "#ffcc00"}.get(data["severity"], "#00FF00")
        mission_log_text.tag_configure(tag_name, foreground=color)
        mission_log_text.insert("end", data["text"] + "\n", tag_name)
        if data["command"]:
            mission_log_text.tag_bind(tag_name, "<Button-1>", lambda e, cmd=data["command"]: replay_log_entry(cmd))
    mission_log_text.config(state="disabled")
    mission_log_text.see("end")

def play_alert_ping_sound():
    os.system("afplay /System/Library/Sounds/Glass.aiff >/dev/null 2>&1 &")

def play_background_hum():
    tone = ambient_tone_files[ambient_index[0] % len(ambient_tone_files)]
    ambient_index[0] += 1
    os.system(f"afplay {tone} >/dev/null 2>&1 &")

def schedule_ambient_hum():
    play_background_hum()
    delay = random.randint(15000, 25000)
    TAB.after(delay, schedule_ambient_hum)

def play_radio_chatter():
    sound = radio_chatter_sounds[radio_chatter_index[0] % len(radio_chatter_sounds)]
    radio_chatter_index[0] += 1
    os.system(f"afplay {sound} >/dev/null 2>&1 &")

def clear_radar_dot():
    radar_canvas.delete("alert_dot")
    radar_status_label.config(text="Sweep idle", fg="#00FF00")
    alert_ping_active[0] = False
    radar_dot_data[0] = None

def show_radar_alert(msg):
    radar_alert_flash.config(text=msg)
    if radar_alert_after[0]:
        TAB.after_cancel(radar_alert_after[0])
    radar_alert_after[0] = TAB.after(1800, lambda: radar_alert_flash.config(text=""))

def update_ping_streak(reset=False):
    if reset:
        ping_streak[0] = 0
    else:
        ping_streak[0] += 1
    radar_ping_label.config(text=f"Ping streak: {ping_streak[0]}")

def update_target_brief(coord_text=None):
    if coord_text is None:
        coord_text = coord_entry.get().strip()
    parsed = parse_coordinates(coord_text)
    if parsed:
        lat, lon = parsed
        target_map_label.config(text=f"Target: {lat:.2f}, {lon:.2f}")
    else:
        target_map_label.config(text="Target: N/A")

def calculate_radar_dot():
    parsed = parse_coordinates(coord_entry.get().strip())
    if not parsed:
        angle = random.uniform(0, 360)
        radius = radar_radius * random.random()
        return angle, radius
    lat, lon = parsed
    angle = (lon + 180) % 360
    lat = max(-90, min(90, lat))
    radius = radar_radius * (1 - (abs(lat) / 90))
    return angle, radius

def trigger_radar_ping():
    if alert_ping_active[0]:
        return
    alert_ping_active[0] = True
    radar_dot_data[0] = calculate_radar_dot()
    center = radar_widget_size / 2
    radius = 8
    radar_canvas.create_oval(center - radius, center - radius, center + radius, center + radius, fill="#FF0000", outline="", tags="alert_dot")
    radar_status_label.config(text="Ping detected!", fg="#FF5555")
    update_ping_streak()
    show_radar_alert("Ping registered")
    play_alert_ping_sound()
    play_background_hum()
    TAB.after(700, clear_radar_dot)

def update_badges():
    name1 = officer1_entry.get().strip()
    name2 = officer2_entry.get().strip()
    if name1:
        badge_officer1.config(text=f"Officer 1: {name1}", bg="#003300")
    else:
        badge_officer1.config(text="Officer 1: OFF", bg="#141414")
    if name2:
        badge_officer2.config(text=f"Officer 2: {name2}", bg="#003300")
    else:
        badge_officer2.config(text="Officer 2: OFF", bg="#141414")
def draw_radar_grid():
    radar_canvas.delete("grid")
    center = radar_widget_size / 2
    for ring in range(1, 4):
        radius = (radar_widget_size/2 - 6) * ring / 4
        radar_canvas.create_oval(center - radius, center - radius, center + radius, center + radius, outline="#00FF00", tags="grid")
    for i in range(16):
        angle_rad = math.radians(i * 360 / 16)
        x = center + (radar_widget_size/2 - 6) * math.cos(angle_rad)
        y = center + (radar_widget_size/2 - 6) * math.sin(angle_rad)
        radar_canvas.create_line(center, center, x, y, fill="#00FF00", tags="grid")

def draw_radar_dot():
    radar_canvas.delete("target")
    data = radar_dot_data[0]
    if not data:
        return
    center = radar_widget_size / 2
    angle, radius = data
    angle_rad = math.radians(angle)
    x = center + radius * math.cos(angle_rad)
    y = center + radius * math.sin(angle_rad)
    radar_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#ff4444", outline="", tags="target")

def update_rotating_widget():
    radar_canvas.delete("sweep")
    center = radar_widget_size / 2
    start_angle = radar_angle[0]
    end_angle = start_angle + radar_beam_width
    angle_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    points = [
        center, center,
        center + radar_radius * math.cos(angle_rad), center + radar_radius * math.sin(angle_rad),
        center + radar_radius * math.cos(end_rad), center + radar_radius * math.sin(end_rad)
    ]
    radar_canvas.create_polygon(points, fill="#00FF00", outline="", tags="sweep")
    radar_angle[0] = (radar_angle[0] + radar_spin_speed) % 360
    draw_radar_dot()
    if random.random() < 0.08:
        trigger_radar_ping()
    TAB.after(120, update_rotating_widget)

def rotate_authorization_seal():
    seal_label.config(text=f"Seal: {auth_states[auth_index[0] % len(auth_states)]}")
    auth_index[0] = (auth_index[0] + 1) % len(auth_states)
    TAB.after(2800, rotate_authorization_seal)

def update_comm_ticker():
    if chatter_messages:
        comm_ticker.config(text=chatter_messages[chatter_index[0] % len(chatter_messages)])
        chatter_index[0] = (chatter_index[0] + 1) % len(chatter_messages)
    TAB.after(2200, update_comm_ticker)

def close_overwatch_window():
    if overwatch_window[0] and overwatch_window[0].winfo_exists():
        overwatch_window[0].destroy()
    overwatch_window[0] = None

def show_overwatch_map():
    if overwatch_window[0] and overwatch_window[0].winfo_exists():
        overwatch_window[0].lift()
        return
    win = tk.Toplevel(TAB)
    win.title("Overwatch Map")
    win.configure(bg="black")
    win.resizable(False, False)
    center = 160
    radius = 140
    map_canvas = tk.Canvas(win, width=center*2, height=center*2, bg="#010101", highlightthickness=0)
    map_canvas.pack(padx=10, pady=10)
    # grid
    for r in range(1, 4):
        r_radius = radius * r / 4
        map_canvas.create_oval(center - r_radius, center - r_radius, center + r_radius, center + r_radius, outline="#00ff00")
    for i in range(0, 360, 45):
        ang_rad = math.radians(i)
        x = center + radius * math.cos(ang_rad)
        y = center + radius * math.sin(ang_rad)
        map_canvas.create_line(center, center, x, y, fill="#00ff00")
    parsed = parse_coordinates(coord_entry.get().strip())
    if parsed:
        lat, lon = parsed
        angle = math.radians((lon + 180) % 360)
        radial = radius * (1 - (abs(lat) / 90))
        tx = center + radial * math.cos(angle)
        ty = center + radial * math.sin(angle)
        map_canvas.create_oval(tx - 6, ty - 6, tx + 6, ty + 6, fill="#ff4444", outline="#ff4444")
        map_canvas.create_line(center, center, tx, ty, fill="#00ff00")
        map_canvas.create_text(center, center - radius - 10, text=f"Impact: {lat:.2f}, {lon:.2f}", fill="#00ff00", font=("Airborne 86", 10))
    else:
        map_canvas.create_text(center, center, text="No coordinates", fill="#ff5555", font=("Airborne 86", 12, "bold"))
    overwatch_window[0] = win
    win.protocol("WM_DELETE_WINDOW", close_overwatch_window)
    win.after(6000, close_overwatch_window)

def parse_coordinates(coord_text):
    try:
        lat_str, lon_str = coord_text.split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
        return lat, lon
    except Exception:
        return None

def update_hud_display(coord_text):
    hud_info.config(text=f"Heading: {coord_text or 'N/A'}")
    hud_impact.config(text=f"Impact: {coord_text or 'N/A'}")
    hud_canvas.delete("target")
    hud_canvas.delete("direction")
    parsed = parse_coordinates(coord_text)
    if not parsed:
        return
    lat, lon = parsed
    x = max(0, min(HUD_WIDTH, (lon + 180) / 360 * HUD_WIDTH))
    y = max(0, min(HUD_HEIGHT, (90 - lat) / 180 * HUD_HEIGHT))
    center_x = HUD_WIDTH / 2
    center_y = HUD_HEIGHT / 2
    hud_canvas.create_line(center_x, center_y, x, y, fill="#00FF00", width=2, arrow="last", tags="direction")
    hud_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#FF0000", outline="#FF0000", tags="target")

def validate_fields(*args):
    officer1 = officer1_entry.get().strip()
    # officer2 field is no longer relevant for validation
    officer1_code = officer1_code_entry.get().strip()
    coords = coord_entry.get().strip()
    update_badges()
    update_hud_display(coords)
    update_readiness_strip()
    update_target_brief(coords)

def format_coordinates(coord_text):
    parsed = parse_coordinates(coord_text)
    if not parsed:
        return None
    lat, lon = parsed
    return f"{lat:.6f}, {lon:.6f}"

def execute_console_command(raw_command):
    command = raw_command.strip()
    if not command:
        return
    upper = command.upper()
    if upper == "KILL":
        log_console("Launch sequence terminated.")
        append_mission_log("Launch sequence killed.", severity="alert", command=command)
        # also disable launch button as a safety
        launch_button.config(state="disabled")
        # re-enable after 10 seconds and notify operator
        TAB.after(10000, lambda: (launch_button.config(state="normal"), log_console("Launch button re-enabled.")))
        return
    if upper == "ABORT":
        log_console("ABORT signal received. All systems standing down.")
        append_mission_log("Abort command executed.", severity="alert", command=command)
        launch_button.config(state="disabled")
        TAB.after(10000, lambda: (launch_button.config(state="normal"), log_console("Launch button re-enabled.")))
        return
    if upper == "DETONATE":
        log_console("mid-air detonation complete")
        append_mission_log("Detonate command executed.", severity="action", command=command)
        return
    if upper == "SCRIPT LIST":
        log_console("Available scripts: " + ", ".join(SCRIPT_SEQUENCES.keys()))
        return
    if upper.startswith("CHANGE HEADING"):
        tail = command[len("CHANGE HEADING"):].strip()
        new_coords = format_coordinates(tail)
        if new_coords:
            coord_entry.delete(0, "end")
            coord_entry.insert(0, new_coords)
            log_console(f"Heading updated to {new_coords}.")
            update_hud_display(new_coords)
            append_mission_log(f"Heading updated to {new_coords}.", severity="action", command=command)
            update_target_brief(new_coords)
        else:
            log_console("Invalid coordinates. Use: CHANGE HEADING lat,long")
    elif upper in ("PLAY CHATTER", "RADIO", "CHATTER"):
        log_console("Radio chatter playing...")
        play_radio_chatter()
        append_mission_log("Radio chatter stream triggered.", severity="action", command=command)
    elif upper.startswith("SCRIPT"):
        requested = command[len("SCRIPT"):].strip().upper()
        run_console_script(requested)
    elif upper.startswith("REPEAT"):
        requested = command[len("REPEAT"):].strip().upper()
        run_console_script(requested)
    elif upper == "STATUS":
        status = [
            f"Officer 1: {officer1_entry.get().strip() or 'N/A'}",
            f"Officer 2: {officer2_entry.get().strip() or 'N/A'}",
            f"Target: {destination_entry.get().strip() or 'N/A'}",
            f"Coordinates: {coord_entry.get().strip() or 'N/A'}",
        ]
        log_console("Console Status:")
        for line in status:
            log_console(f"  {line}")
    else:
        log_console(f"Unknown command: {command}")

def run_console_script(name):
    if script_running[0]:
        log_console("A script is already running.")
        return
    if not name:
        log_console("Available scripts: " + ", ".join(SCRIPT_SEQUENCES.keys()))
        return
    sequence = SCRIPT_SEQUENCES.get(name)
    if not sequence:
        log_console(f"No sequence named {name}.")
        return
    script_running[0] = True
    command_token = f"SCRIPT {name}"
    append_mission_log(f"{name} sequence started.", severity="action", command=command_token)
    log_console(f"Executing {name} sequence...")
    if name in ("COMM CHATTER", "COMMUNICATIONS"):
        play_radio_chatter()
    if name == "RADAR":
        show_overwatch_map()
    def step(idx):
        if idx >= len(sequence):
            script_running[0] = False
            log_console(f"{name} sequence complete.")
            append_mission_log(f"{name} sequence complete.", severity="info", command=command_token)
            return
        log_console(sequence[idx])
        TAB.after(500, lambda: step(idx + 1))
    step(0)

def handle_console_input(event=None):
    command = console_entry.get().strip()
    if not command:
        return "break"
    command_history.append(command)
    history_index[0] = len(command_history)
    console_entry.delete(0, "end")
    log_console(f"> {command}")
    execute_console_command(command)
    return "break"

def cycle_history(direction):
    if not command_history:
        return
    history_index[0] = max(0, min(history_index[0] + direction, len(command_history)))
    if history_index[0] < len(command_history):
        console_entry.delete(0, "end")
        console_entry.insert(0, command_history[history_index[0]])

console_entry.bind("<Return>", handle_console_input)
console_entry.bind("<Up>", lambda e: cycle_history(-1) or "break")
console_entry.bind("<Down>", lambda e: cycle_history(1) or "break")

officer1_entry.bind("<KeyRelease>", validate_fields)
officer2_entry.bind("<KeyRelease>", validate_fields)
officer1_code_entry.bind("<KeyRelease>", validate_fields)
    # second code field removed, nothing to bind
destination_entry.bind("<KeyRelease>", validate_fields)
coord_entry.bind("<KeyRelease>", validate_fields)

validate_fields()
rotate_authorization_seal()
update_comm_ticker()
draw_radar_grid()
update_target_brief()
update_rotating_widget()
schedule_ambient_hum()

footer_frame = tk.Frame(TAB, bg="#222222")
footer_frame.pack(side="bottom", fill="x")
conf_label = tk.Label(footer_frame, text="US ARMY CONFIDENTIAL PROGRAM", font=("Airborne 86", 16, "bold"), fg="white", bg="#222222")
conf_label.pack(side="left", padx=20, pady=5)
author_label = tk.Label(footer_frame, text="Property of Gustaw Luberadzki | Authorized Personnel Only", font=("Airborne 86", 14), fg="white", bg="#222222")
author_label.pack(side="right", padx=20, pady=5)

TAB.mainloop()
