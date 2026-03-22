from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Smart Repair API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DiagnoseRequest(BaseModel):
    device: str
    problem: str


class DiagnoseResponse(BaseModel):
    device: str
    problem: str
    causes: list[str]
    steps: list[str]


RULES = [
    # ── Arduino ───────────────────────────────────────────
    {
        "device": "arduino",
        "keywords": ["not detected", "not recognized", "port not found", "com port"],
        "causes": [
            "Faulty or low-quality USB cable",
            "Missing or corrupted CH340/FTDI driver",
            "Defective USB port on the computer",
            "Damaged USB connector on the Arduino board",
        ],
        "steps": [
            "Try a different USB cable (data cable, not charge-only)",
            "Install or reinstall the CH340/FTDI driver for your OS",
            "Test a different USB port on your computer",
            "Check Device Manager for errors",
            "Test the Arduino board on another computer to isolate the fault",
        ],
    },
    {
        "device": "arduino",
        "keywords": ["upload error", "avrdude", "cannot upload", "timeout"],
        "causes": [
            "Wrong board or COM port selected in Arduino IDE",
            "Another process is occupying the serial port",
            "Bootloader is corrupted or missing",
            "Sketch is too large for the selected board",
        ],
        "steps": [
            "Go to Tools → Board and select the correct Arduino model",
            "Go to Tools → Port and select the correct COM/tty port",
            "Close any serial monitors or other apps using the port",
            "Try pressing the Reset button just before uploading",
            "Re-burn the bootloader using another Arduino as ISP if needed",
        ],
    },
    {
        "device": "arduino",
        "keywords": ["power", "no light", "led off", "not turning on", "dead"],
        "causes": [
            "Insufficient power supply (USB hub without power)",
            "Blown onboard fuse or voltage regulator",
            "Short circuit on the breadboard or connected components",
            "Damaged microcontroller from over-voltage",
        ],
        "steps": [
            "Connect directly to a computer USB port, not a hub",
            "Check if the power LED (PWR) lights up — if not, inspect the fuse",
            "Disconnect all external components and try again",
            "Measure the 5V and 3.3V pins with a multimeter",
            "Replace the board if the voltage regulator is burned out",
        ],
    },

    # ── Laptop ────────────────────────────────────────────
    {
        "device": "laptop",
        "keywords": ["not turning on", "won't start", "no power", "black screen", "dead"],
        "causes": [
            "Drained or faulty battery",
            "Defective power adapter or charging port",
            "RAM module is loose or failed",
            "Corrupted BIOS/UEFI firmware",
        ],
        "steps": [
            "Hold the power button for 10 seconds to force shutdown, then restart",
            "Connect the charger and wait 10 minutes before trying to power on",
            "Remove the battery (if removable), hold power 30s, reinsert and try",
            "Try a known-working charger to rule out adapter failure",
            "Reseat or replace RAM modules if comfortable opening the laptop",
        ],
    },
    {
        "device": "laptop",
        "keywords": ["slow", "lagging", "freezing", "hangs", "performance"],
        "causes": [
            "High CPU/RAM usage from background processes",
            "Failing or nearly full hard drive",
            "Malware or adware consuming resources",
            "Thermal throttling due to dust-clogged vents",
        ],
        "steps": [
            "Open Task Manager and kill high-usage processes",
            "Run a disk health check with CrystalDiskInfo",
            "Scan for malware with Malwarebytes",
            "Clean the cooling vents with compressed air",
            "Consider upgrading to an SSD or adding more RAM",
        ],
    },
    {
        "device": "laptop",
        "keywords": ["wifi", "no internet", "network", "wireless", "not connecting"],
        "causes": [
            "Wi-Fi adapter is disabled in settings",
            "Outdated or corrupted network driver",
            "Router or ISP issue",
            "IP address conflict on the network",
        ],
        "steps": [
            "Toggle Airplane Mode off, then toggle Wi-Fi off and on again",
            "Restart the router and modem",
            "Update or reinstall the Wi-Fi driver from Device Manager",
            "Run the network troubleshooter in Windows Settings",
            "Try connecting via ethernet to confirm if the issue is Wi-Fi-specific",
        ],
    },

    # ── TV ────────────────────────────────────────────────
    {
        "device": "tv",
        "keywords": ["no picture", "black screen", "no display", "screen off"],
        "causes": [
            "Incorrect input source selected",
            "HDMI or signal cable is loose or damaged",
            "Backlight failure",
            "Firmware/software crash on Smart TV",
        ],
        "steps": [
            "Press the Input/Source button and cycle through all inputs",
            "Power cycle the TV: unplug for 60 seconds, then plug back in",
            "Check all cables and try a different HDMI port or cable",
            "Shine a flashlight at the screen — dim image means backlight is faulty",
            "Perform a factory reset from the settings menu",
        ],
    },
    {
        "device": "tv",
        "keywords": ["no sound", "audio", "mute", "volume"],
        "causes": [
            "TV is muted or volume is at zero",
            "Audio output set to external speakers that are off",
            "Defective internal speakers",
            "Software/firmware glitch affecting audio",
        ],
        "steps": [
            "Check mute status and volume level on both TV and remote",
            "Go to Settings → Sound and set output back to TV Speakers",
            "Test with headphones plugged in to isolate speaker failure",
            "Power cycle and perform a sound test from the diagnostics menu",
            "Update TV firmware via Settings → Support → Software Update",
        ],
    },
    {
        "device": "tv",
        "keywords": ["remote", "not responding", "remote not working"],
        "causes": [
            "Dead or depleted batteries in the remote",
            "IR sensor on the TV is blocked or dirty",
            "Remote control is faulty",
        ],
        "steps": [
            "Replace the batteries with fresh ones",
            "Point a phone camera at the remote IR LED — press a button to see if it flashes",
            "Clean the front IR sensor window on the TV with a soft cloth",
            "Try controlling the TV using physical buttons on the set",
        ],
    },

    # ── Smartphone ────────────────────────────────────────
    {
        "device": "smartphone",
        "keywords": ["not turning on", "black screen", "dead", "won't start", "no power"],
        "causes": [
            "Battery is completely drained",
            "Faulty charging cable or adapter",
            "Software crash or bootloop",
            "Physical damage to the power button or motherboard",
        ],
        "steps": [
            "Plug in the charger and wait at least 15 minutes before pressing power",
            "Try a different charging cable and adapter",
            "Hold Power + Volume Down for 10-15 seconds to force restart",
            "Try booting into Recovery Mode (Power + Volume Up)",
            "If still dead, visit a repair shop to check the battery and board",
        ],
    },
    {
        "device": "smartphone",
        "keywords": ["not charging", "charging slow", "charger not working"],
        "causes": [
            "Dirty or lint-filled charging port",
            "Damaged charging cable or adapter",
            "Battery health has degraded significantly",
            "Software bug preventing charging detection",
        ],
        "steps": [
            "Clean the charging port gently with a toothpick or soft brush",
            "Try a different cable and charger (preferably original)",
            "Check battery health in Settings → Battery",
            "Restart the phone and try charging again",
            "If wireless charging works but wired doesn't, the port may need replacement",
        ],
    },
    {
        "device": "smartphone",
        "keywords": ["screen cracked", "display broken", "touch not working", "screen unresponsive"],
        "causes": [
            "Physical impact cracked the display glass",
            "Digitizer layer damaged (touch input layer)",
            "Display connector is loose internally",
            "Water damage affecting the screen",
        ],
        "steps": [
            "If only glass is cracked but touch works, use a screen protector temporarily",
            "If touch is unresponsive, the digitizer needs replacement",
            "Avoid pressing hard on the screen to prevent further damage",
            "Back up your data immediately via cloud or PC",
            "Visit a certified repair shop for screen replacement",
        ],
    },
    {
        "device": "smartphone",
        "keywords": ["overheating", "too hot", "heating up", "hot"],
        "causes": [
            "CPU-intensive apps running in the background",
            "Charging while using the phone heavily",
            "Blocked ventilation or direct sunlight exposure",
            "Battery is swollen or degraded",
        ],
        "steps": [
            "Close all background apps and let the phone rest for 10 minutes",
            "Remove the phone case while charging",
            "Avoid using the phone in direct sunlight or hot environments",
            "Check for apps consuming excessive CPU in Settings → Battery",
            "If the back feels unusually hot or bulging, replace the battery immediately",
        ],
    },

    # ── Printer ───────────────────────────────────────────
    {
        "device": "printer",
        "keywords": ["not printing", "won't print", "no output", "print job stuck"],
        "causes": [
            "Print queue is stuck or jammed with old jobs",
            "Printer is offline or not set as default",
            "Driver is corrupted or outdated",
            "USB or network connection lost",
        ],
        "steps": [
            "Open the print queue and cancel all pending jobs",
            "Right-click the printer in Settings and set it as default",
            "Restart the Print Spooler service (services.msc → Print Spooler → Restart)",
            "Reinstall the printer driver from the manufacturer's website",
            "Reconnect the USB cable or reconnect to the Wi-Fi network",
        ],
    },
    {
        "device": "printer",
        "keywords": ["paper jam", "paper stuck", "jammed"],
        "causes": [
            "Paper loaded incorrectly or too much paper in tray",
            "Small torn piece of paper stuck inside",
            "Worn out paper feed rollers",
            "Wrong paper size loaded vs print settings",
        ],
        "steps": [
            "Turn off the printer and unplug it before removing paper",
            "Gently pull the jammed paper in the direction of paper flow",
            "Check for any small torn pieces remaining inside",
            "Clean the paper feed rollers with a damp lint-free cloth",
            "Reload paper properly and ensure it matches the selected paper size",
        ],
    },
    {
        "device": "printer",
        "keywords": ["ink", "low ink", "no ink", "faded", "streaks", "poor quality"],
        "causes": [
            "Ink or toner cartridge is empty or nearly empty",
            "Printhead is clogged from infrequent use",
            "Incompatible or refilled cartridge causing issues",
            "Incorrect print quality settings",
        ],
        "steps": [
            "Check ink levels from the printer software on your computer",
            "Run the printhead cleaning utility from printer settings",
            "Replace empty or low cartridges with genuine ones",
            "Print a test page to check quality after cleaning",
            "Set print quality to High in the print dialog for better results",
        ],
    },
    {
        "device": "printer",
        "keywords": ["offline", "not detected", "not found", "cannot connect"],
        "causes": [
            "Printer is in sleep mode or powered off",
            "Wi-Fi connection dropped for wireless printers",
            "IP address of printer changed on the network",
            "Driver not installed or corrupted",
        ],
        "steps": [
            "Turn the printer off and back on, then wait 30 seconds",
            "On Windows: Settings → Printers → right-click → uncheck 'Use Printer Offline'",
            "Reconnect the printer to Wi-Fi using the printer's display panel",
            "Remove the printer from your PC and re-add it",
            "Reinstall the latest driver from the manufacturer's website",
        ],
    },

    # ── Router ────────────────────────────────────────────
    {
        "device": "router",
        "keywords": ["no internet", "not working", "no connection", "internet down"],
        "causes": [
            "ISP outage in your area",
            "Router firmware crashed or needs reboot",
            "Ethernet cable from modem to router is loose",
            "DNS server issue causing connectivity problems",
        ],
        "steps": [
            "Reboot the router: unplug power for 30 seconds, plug back in",
            "Check if other devices also have no internet (if yes, it is an ISP issue)",
            "Log into the router admin panel (192.168.1.1) and check WAN status",
            "Try changing DNS to 8.8.8.8 (Google) or 1.1.1.1 (Cloudflare)",
            "Contact your ISP if the WAN IP is missing or shows an error",
        ],
    },
    {
        "device": "router",
        "keywords": ["slow wifi", "weak signal", "poor speed", "dropping", "unstable"],
        "causes": [
            "Router is too far from the device or obstructed by walls",
            "Wi-Fi channel congestion from neighboring networks",
            "Too many devices connected simultaneously",
            "Router overheating or outdated firmware",
        ],
        "steps": [
            "Move the router to a central, elevated, open location",
            "Log into admin panel and change the Wi-Fi channel (try 1, 6, or 11 for 2.4GHz)",
            "Switch devices to the 5GHz band if available",
            "Update router firmware from the admin panel",
            "Restart the router and limit background bandwidth-heavy devices",
        ],
    },
    {
        "device": "router",
        "keywords": ["can't connect", "wrong password", "authentication failed", "not connecting"],
        "causes": [
            "Incorrect Wi-Fi password entered",
            "Device MAC address is blocked in router settings",
            "Router is set to only allow specific devices (MAC filtering)",
            "Corrupted Wi-Fi profile saved on the device",
        ],
        "steps": [
            "Double-check the Wi-Fi password — check the label on the router",
            "Forget the network on your device and reconnect from scratch",
            "Log into router admin and check if MAC filtering is enabled",
            "Disable MAC filtering temporarily to test if that is the issue",
            "Reset the router to factory defaults if you lost admin access",
        ],
    },
    {
        "device": "router",
        "keywords": ["lights", "blinking", "red light", "no light", "led"],
        "causes": [
            "Red/orange WAN light means no internet from ISP",
            "All lights off means no power",
            "Blinking power light may indicate firmware update in progress",
            "Solid red on LAN port means cable issue",
        ],
        "steps": [
            "Check the router manual or manufacturer website for LED meanings",
            "If WAN light is red: check the cable from modem to router, then call ISP",
            "If no lights: check power adapter and outlet",
            "Do not unplug the router if lights are cycling (firmware update)",
            "Perform a factory reset (hold reset button 10s) as a last resort",
        ],
    },

    # ── Desktop PC ────────────────────────────────────────
    {
        "device": "desktop",
        "keywords": ["not turning on", "no power", "dead", "won't start"],
        "causes": [
            "Power supply unit (PSU) is faulty or underpowered",
            "Power cable is loose or wall outlet has no power",
            "RAM or GPU is not seated properly",
            "Motherboard failure or short circuit",
        ],
        "steps": [
            "Check the power cable at both ends (wall and PSU)",
            "Make sure the PSU switch on the back is set to ON ( | )",
            "Try a different wall outlet or power strip",
            "Open the case and reseat the RAM and GPU firmly",
            "Test with a known-working PSU to rule out PSU failure",
        ],
    },
    {
        "device": "desktop",
        "keywords": ["no display", "black screen", "monitor not working", "no signal"],
        "causes": [
            "Monitor cable plugged into motherboard instead of GPU",
            "GPU is not seated properly in PCIe slot",
            "Monitor is on wrong input source",
            "RAM issue causing no POST",
        ],
        "steps": [
            "Make sure the display cable is connected to the GPU, not the motherboard",
            "Check the monitor input source button — switch to the correct HDMI/DisplayPort",
            "Reseat the GPU firmly in the PCIe slot and reconnect power connectors",
            "Try with one stick of RAM in the first slot (A2 slot)",
            "Listen for beep codes on startup — they indicate specific hardware failures",
        ],
    },
    {
        "device": "desktop",
        "keywords": ["overheating", "hot", "shutdown", "thermal", "fan noise"],
        "causes": [
            "CPU cooler has dried thermal paste",
            "Case fans are not working or blocked",
            "Dust buildup on heatsinks and filters",
            "Poor airflow inside the case",
        ],
        "steps": [
            "Open the case and clean all dust with compressed air",
            "Check that all fans (CPU, case, GPU) are spinning",
            "Replace the thermal paste on the CPU (recommended every 3-5 years)",
            "Ensure proper cable management for good airflow",
            "Monitor temperatures with HWMonitor or MSI Afterburner",
        ],
    },
    {
        "device": "desktop",
        "keywords": ["slow", "lagging", "freezing", "performance", "hangs"],
        "causes": [
            "HDD is failing or nearly full",
            "Too many startup programs consuming resources",
            "Malware running in the background",
            "Insufficient RAM for current workload",
        ],
        "steps": [
            "Run CrystalDiskInfo to check HDD/SSD health",
            "Disable unnecessary startup programs (Task Manager → Startup tab)",
            "Run a full malware scan with Malwarebytes",
            "Check RAM usage in Task Manager — upgrade if consistently above 80%",
            "Consider upgrading to an SSD if running on an old HDD",
        ],
    },
]

DEFAULT_RESPONSE = {
    "causes": [
        "The problem description did not match a known failure pattern",
        "The issue may require physical inspection",
    ],
    "steps": [
        "Search for your exact device model + problem description online",
        "Check the manufacturer's official support page",
        "Consult a certified repair technician if the issue persists",
    ],
}


def diagnose(device: str, problem: str) -> tuple[list[str], list[str]]:
    device_lower = device.lower().strip()
    problem_lower = problem.lower().strip()

    for rule in RULES:
        if rule["device"] == device_lower:
            if any(kw in problem_lower for kw in rule["keywords"]):
                return rule["causes"], rule["steps"]

    return DEFAULT_RESPONSE["causes"], DEFAULT_RESPONSE["steps"]


@app.post("/diagnose", response_model=DiagnoseResponse)
def diagnose_endpoint(request: DiagnoseRequest):
    causes, steps = diagnose(request.device, request.problem)
    return DiagnoseResponse(
        device=request.device,
        problem=request.problem,
        causes=causes,
        steps=steps,
    )


@app.get("/")
def root():
    return {"message": "Smart Repair API is running. POST to /diagnose"}