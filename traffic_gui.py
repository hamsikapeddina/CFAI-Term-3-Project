from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

# =====================================================
# WINDOW
# =====================================================

root = Tk()
root.title("Smart Traffic Signal Optimization System")
root.state("zoomed")
root.configure(bg="white")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =====================================================
# DATA
# =====================================================

TRAFFIC_DATA = {

    "High Traffic": {
        "vehicles": 57,
        "sensor": 52,
        "waiting": 31,
        "signal": 60,
        "efficiency": 92,
        "status": "🔴 HIGH TRAFFIC",

        "reason":
        """
• Heavy congestion detected
• Vehicle density above threshold
• Priority score highest
• Signal duration increased
""",

        "measures":
        """
✓ Green Signal Extended

✓ Congestion Reduction Activated

✓ Lane Priority Increased

✓ Traffic Monitoring Enabled
"""
    },

    "Medium Traffic": {
        "vehicles": 34,
        "sensor": 30,
        "waiting": 18,
        "signal": 40,
        "efficiency": 88,
        "status": "🟡 MEDIUM TRAFFIC",

        "reason":
        """
• Moderate traffic detected
• Normal optimization applied
• Traffic flow balanced
""",

        "measures":
        """
✓ Balanced Traffic Flow

✓ Standard Optimization

✓ Dynamic Monitoring
"""
    },

    "Low Traffic": {
        "vehicles": 12,
        "sensor": 10,
        "waiting": 8,
        "signal": 20,
        "efficiency": 96,
        "status": "🟢 LOW TRAFFIC",

        "reason":
        """
• Low vehicle density
• No congestion detected
• Standard timing sufficient
""",

        "measures":
        """
✓ Standard Signal Timing

✓ Smooth Traffic Flow
"""
    },

    "Emergency Vehicle": {
        "vehicles": 25,
        "sensor": 22,
        "waiting": 5,
        "signal": 60,
        "efficiency": 100,
        "status": "🚑 EMERGENCY PRIORITY",

        "reason":
        """
• Ambulance detected

• Priority override activated

• Fastest route selected
""",

        "measures":
        """
✓ Immediate Green Signal

✓ Route Clearance

✓ Other Lanes Temporarily Stopped

✓ Emergency Priority Mode
"""
    }
}

# =====================================================
# VARIABLES
# =====================================================

status_var = StringVar()
status_var.set("⚪ Waiting For Analysis")

selected_img_label = None

# =====================================================
# FUNCTIONS
# =====================================================

def generate_report():

    report = dashboard_text.get("1.0", END)

    with open("traffic_report.txt", "w") as file:
        file.write(report)

    status_var.set("✅ Report Generated")

def analyze_image_density(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    edge_pixels = np.count_nonzero(edges)

    height, width = edges.shape

    density = edge_pixels / (height * width)

    if density > 0.12:
        traffic_level = "HIGH"

    elif density > 0.06:
        traffic_level = "MEDIUM"

    else:
        traffic_level = "LOW"

    return traffic_level, round(density, 4)

def analyze(scenario, image_path):

    data = TRAFFIC_DATA[scenario]

    vehicles = data["vehicles"]
    sensor = data["sensor"]
    waiting = data["waiting"]

    # -----------------------------------------
    # OpenCV Image Analysis
    # -----------------------------------------

    traffic_level, density_score = analyze_image_density(image_path)

    # -----------------------------------------
    # AI Priority Score
    # -----------------------------------------

    priority_score = (vehicles * 2) + waiting

    # -----------------------------------------
    # Rule-Based Decision Engine
    # -----------------------------------------

    if scenario == "Emergency Vehicle":

        signal_time = 60

        applied_rule = """
Emergency Vehicle Detected

Priority Override Activated

Immediate Green Signal Assigned
"""

    elif priority_score > 120:

        signal_time = 60

        applied_rule = """
Priority Score > 120

Heavy Congestion Detected

Green Signal Extended To 60 Seconds
"""

    elif priority_score > 60:

        signal_time = 40

        applied_rule = """
Priority Score > 60

Moderate Traffic Detected

Green Signal Set To 40 Seconds
"""

    else:

        signal_time = 20

        applied_rule = """
Priority Score <= 60

Low Traffic Detected

Standard Signal Time Applied
"""

    status_var.set(data["status"])

    dashboard_text.delete("1.0", END)

    dashboard_text.insert(
        END,
        f"""
TRAFFIC ANALYSIS REPORT
==================================================

Traffic Type            : {scenario}

Image Analysis Result   : {traffic_level}

Density Score           : {density_score}

Vehicle Count           : {vehicles}

Sensor Reading          : {sensor}

Waiting Time            : {waiting} sec

Priority Score          : {priority_score}

Green Signal Duration   : {signal_time} sec

Optimization Efficiency : {data['efficiency']} %

==================================================

MEASURES TAKEN

{data['measures']}

==================================================

AI REASONING

{data['reason']}

Image Analysis:
Traffic density estimated using OpenCV edge detection.

==================================================

DECISION LOGIC

Priority Score Formula

Priority Score
= (Vehicle Count × 2) + Waiting Time

= ({vehicles} × 2) + {waiting}

= {priority_score}

==================================================

RULE APPLIED

{applied_rule}

==================================================
"""
    )

    image = Image.open(image_path)

    image = image.resize((350, 250))

    photo = ImageTk.PhotoImage(image)

    selected_img_label.config(image=photo)

    selected_img_label.image = photo

# =====================================================
# TITLE
# =====================================================

Label(
    root,
    text="SMART TRAFFIC SIGNAL OPTIMIZATION SYSTEM",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="darkblue"
).pack(pady=15)

# =====================================================
# MAIN CONTAINER
# =====================================================

main_frame = Frame(root, bg="white")
main_frame.pack(fill=BOTH, expand=True)

# =====================================================
# LEFT PANEL
# =====================================================

left_panel = Frame(
    main_frame,
    bg="white",
    width=500
)

left_panel.pack(
    side=LEFT,
    fill=Y,
    padx=20
)

# =====================================================
# RIGHT PANEL
# =====================================================

right_panel = Frame(
    main_frame,
    bg="white"
)

right_panel.pack(
    side=RIGHT,
    fill=BOTH,
    expand=True,
    padx=20
)

# =====================================================
# LOAD IMAGES
# =====================================================

high_path = os.path.join(BASE_DIR, "high_traffic.jpg")
medium_path = os.path.join(BASE_DIR, "medium_traffic.jpg")
low_path = os.path.join(BASE_DIR, "low_traffic.jpg")
emergency_path = os.path.join(BASE_DIR, "emergency.jpg")

def create_thumb(path):
    img = Image.open(path)
    img = img.resize((160, 90))
    return ImageTk.PhotoImage(img)

high_img = create_thumb(high_path)
medium_img = create_thumb(medium_path)
low_img = create_thumb(low_path)
emergency_img = create_thumb(emergency_path)

# =====================================================
# LEFT SIDE IMAGES
# =====================================================

Label(
    left_panel,
    text="Traffic Scenarios",
    font=("Arial", 16, "bold"),
    bg="white"
).pack(pady=10)

for title, image, path in [

    ("High Traffic", high_img, high_path),

    ("Medium Traffic", medium_img, medium_path),

    ("Low Traffic", low_img, low_path),

    ("Emergency Vehicle", emergency_img, emergency_path)

]:

    frame = Frame(left_panel, bg="white")
    frame.pack(pady=5)

    Label(
        frame,
        image=image,
        bg="white"
    ).pack()

    Button(
        frame,
        text=title,
        width=25,
        command=lambda t=title,p=path:
        analyze(t,p)
    ).pack(pady=5)

# =====================================================
# STATUS
# =====================================================

Label(
    right_panel,
    textvariable=status_var,
    font=("Arial",16,"bold"),
    bg="white"
).pack(pady=10)

# =====================================================
# SELECTED IMAGE
# =====================================================

selected_frame = LabelFrame(
    right_panel,
    text="Selected Scenario",
    bg="white",
    font=("Arial",12,"bold")
)

selected_frame.pack(fill=X)

selected_img_label = Label(
    selected_frame,
    bg="white"
)

selected_img_label.pack(pady=10)

# =====================================================
# DASHBOARD
# =====================================================

dashboard_frame = LabelFrame(
    right_panel,
    text="Traffic Analysis Dashboard",
    bg="white",
    font=("Arial",12,"bold")
)

dashboard_frame.pack(
    fill=BOTH,
    expand=True,
    pady=15
)

dashboard_text = Text(
    dashboard_frame,
    font=("Consolas",11),
    wrap=WORD
)

dashboard_text.pack(
    fill=BOTH,
    expand=True
)

dashboard_text.insert(
    END,
    "Select a traffic scenario to begin analysis."
)

# =====================================================
# REPORT BUTTON
# =====================================================

Button(
    right_panel,
    text="Generate Traffic Report",
    bg="darkgreen",
    fg="white",
    font=("Arial",12,"bold"),
    command=generate_report
).pack(pady=10)

root.mainloop()