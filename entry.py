import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import numpy as np
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time

# pip install numpyColor palette
COLOR_PRIMARY = "#44d87c"      # Green Light
COLOR_SECONDARY = "#a474fc"    # Purple
COLOR_DARK = "#166d37"         # Dark Green
COLOR_LIGHT = "#64a6a9"        # Light Blue-Green
COLOR_PINK = "#d0a0c5"         # Light Pink
COLOR_BG = "#242c2c"           # Dark Background
COLOR_TEXT = "#ffffff"         # White text

# Load CSV
csv_path = 'students.csv'
if not os.path.exists(csv_path):
    messagebox.showerror("Error", f"'{csv_path}' file not found!")
    exit()

students_df = pd.read_csv(csv_path)
entry_list = []
scanned_qrs = set()
scanned_faces = set()

# Get student info by QR
def get_student_by_qr(qr_data):
    match = students_df[students_df['QR'] == qr_data]
    if not match.empty:
        student = match.iloc[0]
        return student['ID'], student['Name']
    return None, None

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# GUI setup
root = tk.Tk()
root.title("🎓 QR or Face Detection Attendance")
root.geometry("920x560")
root.configure(bg=COLOR_BG)

video_label = tk.Label(root, bg=COLOR_BG, width=640, height=480)
video_label.pack(side='left', padx=10, pady=10)

info_frame = tk.Frame(root, bg=COLOR_BG)
info_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

title_label = tk.Label(info_frame, text="Attendance Scanner", font=("Segoe UI", 22, "bold"),
                       fg=COLOR_PRIMARY, bg=COLOR_BG)
title_label.pack(pady=(0,20))

status_label = tk.Label(info_frame, text="Scan Status", font=("Segoe UI", 18),
                        fg=COLOR_LIGHT, bg=COLOR_BG)
status_label.pack(pady=10)

color_canvas = tk.Canvas(info_frame, width=140, height=140, bg=COLOR_BG, highlightthickness=2, highlightbackground=COLOR_SECONDARY)
color_canvas.pack(pady=20)

list_label = tk.Label(info_frame, text="Entries", font=("Segoe UI", 16, "bold"),
                      fg=COLOR_PINK, bg=COLOR_BG)
list_label.pack(pady=(10, 5))

columns = ("ID", "Name", "Time")
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
                background=COLOR_BG,
                fieldbackground=COLOR_BG,
                foreground=COLOR_TEXT,
                rowheight=25,
                font=("Segoe UI", 11))
style.configure("Treeview.Heading",
                font=("Segoe UI", 12, "bold"),
                foreground=COLOR_PRIMARY)
style.map('Treeview', background=[('selected', COLOR_SECONDARY)])

tree = ttk.Treeview(info_frame, columns=columns, show='headings', height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor='center')
tree.pack(fill='both', expand=True, pady=5)

def flash_color(color, times=2, delay=0.3):
    def runner():
        for _ in range(times):
            color_canvas.config(bg=color)
            time.sleep(delay)
            color_canvas.config(bg=COLOR_BG)
            time.sleep(delay)
    threading.Thread(target=runner, daemon=True).start()

def scan_qr_or_face():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles on faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (68, 216, 124), 2)

        qr_found = False
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32).reshape((-1,1,2))
            cv2.polylines(frame, [pts], True, (164, 116, 252), 3)

            if qr_data in scanned_qrs:
                root.after(0, status_label.config, {"text": "Duplicate QR detected!", "fg": "#FF5555"})
                root.after(0, flash_color, "#FF5555", 1, 0.5)
            else:
                student_id, student_name = get_student_by_qr(qr_data)
                if student_id:
                    # QR valid, entry নাও, face থাকুক বা না থাকুক
                    entry = {
                        'ID': student_id,
                        'Name': student_name,
                        'Time': datetime.now().strftime('%H:%M:%S')
                    }
                    entry_list.append(entry)
                    scanned_qrs.add(qr_data)
                    root.after(0, status_label.config, {"text": f"Welcome {student_name} via QR!", "fg": COLOR_PRIMARY})
                    root.after(0, flash_color, COLOR_PRIMARY, 2, 0.3)
                    root.after(0, lambda: tree.insert('', 'end', values=(student_id, student_name, entry['Time'])))
                else:
                    root.after(0, status_label.config, {"text": "Invalid QR Code!", "fg": "#FF5555"})
                    root.after(0, flash_color, "#FF5555", 1, 0.5)

            qr_found = True
            break

        # যদি QR পাওয়া না যায়, তাহলে মুখ দেখে এন্ট্রি নাও
        if not qr_found:
            if len(faces) > 0:
                # মুখ যদি নতুন হয় (duplicate না হয়)
                # আমরা শুধু face detect করছি, তাই name বা id নেই, তাই generic entry
                # এখানে তুমি চাইলে "FaceDetected" নামে বা অন্যভাবে handle করতে পারো
                face_id = "FaceDetected"
                if face_id not in scanned_faces:
                    entry = {
                        'ID': "FaceDetected",
                        'Name': "Face Detected (No QR)",
                        'Time': datetime.now().strftime('%H:%M:%S')
                    }
                    entry_list.append(entry)
                    scanned_faces.add(face_id)
                    root.after(0, status_label.config, {"text": "Entry by Face Detection!", "fg": COLOR_PRIMARY})
                    root.after(0, flash_color, COLOR_PRIMARY, 2, 0.3)
                    root.after(0, lambda: tree.insert('', 'end', values=(entry['ID'], entry['Name'], entry['Time'])))
            else:
                root.after(0, status_label.config, {"text": "Scan Status", "fg": COLOR_LIGHT})

        # Tkinter এর জন্য OpenCV ইমেজ কনভার্ট
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)

        if not root.winfo_exists():
            break

    cap.release()
    cv2.destroyAllWindows()

def start_scan():
    t = threading.Thread(target=scan_qr_or_face, daemon=True)
    t.start()

start_scan()

def on_close():
    if entry_list:
        df = pd.DataFrame(entry_list)
        df.to_csv("entries.csv", index=False)
        messagebox.showinfo("Saved", "✅ Entries saved to 'entries.csv'")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import numpy as np
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time

# Color palette
COLOR_PRIMARY = "#44d87c"      # Green Light
COLOR_SECONDARY = "#a474fc"    # Purple
COLOR_DARK = "#166d37"         # Dark Green
COLOR_LIGHT = "#64a6a9"        # Light Blue-Green
COLOR_PINK = "#d0a0c5"         # Light Pink
COLOR_BG = "#242c2c"           # Dark Background
COLOR_TEXT = "#ffffff"         # White text

# Load CSV
csv_path = 'students.csv'
if not os.path.exists(csv_path):
    messagebox.showerror("Error", f"'{csv_path}' file not found!")
    exit()

students_df = pd.read_csv(csv_path)
entry_list = []
scanned_qrs = set()
scanned_faces = set()

# Get student info by QR
def get_student_by_qr(qr_data):
    match = students_df[students_df['QR'] == qr_data]
    if not match.empty:
        student = match.iloc[0]
        return student['ID'], student['Name']
    return None, None

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# GUI setup
root = tk.Tk()
root.title("🎓 QR or Face Detection Attendance")
root.geometry("920x560")
root.configure(bg=COLOR_BG)

video_label = tk.Label(root, bg=COLOR_BG, width=640, height=480)
video_label.pack(side='left', padx=10, pady=10)

info_frame = tk.Frame(root, bg=COLOR_BG)
info_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

title_label = tk.Label(info_frame, text="Attendance Scanner", font=("Segoe UI", 22, "bold"),
                       fg=COLOR_PRIMARY, bg=COLOR_BG)
title_label.pack(pady=(0,20))

status_label = tk.Label(info_frame, text="Scan Status", font=("Segoe UI", 18),
                        fg=COLOR_LIGHT, bg=COLOR_BG)
status_label.pack(pady=10)

color_canvas = tk.Canvas(info_frame, width=140, height=140, bg=COLOR_BG, highlightthickness=2, highlightbackground=COLOR_SECONDARY)
color_canvas.pack(pady=20)

list_label = tk.Label(info_frame, text="Entries", font=("Segoe UI", 16, "bold"),
                      fg=COLOR_PINK, bg=COLOR_BG)
list_label.pack(pady=(10, 5))

columns = ("ID", "Name", "Time")
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
                background=COLOR_BG,
                fieldbackground=COLOR_BG,
                foreground=COLOR_TEXT,
                rowheight=25,
                font=("Segoe UI", 11))
style.configure("Treeview.Heading",
                font=("Segoe UI", 12, "bold"),
                foreground=COLOR_PRIMARY)
style.map('Treeview', background=[('selected', COLOR_SECONDARY)])

tree = ttk.Treeview(info_frame, columns=columns, show='headings', height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor='center')
tree.pack(fill='both', expand=True, pady=5)

def flash_color(color, times=2, delay=0.3):
    def runner():
        for _ in range(times):
            color_canvas.config(bg=color)
            time.sleep(delay)
            color_canvas.config(bg=COLOR_BG)
            time.sleep(delay)
    threading.Thread(target=runner, daemon=True).start()

def scan_qr_or_face():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles on faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (68, 216, 124), 2)

        qr_found = False
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32).reshape((-1,1,2))
            cv2.polylines(frame, [pts], True, (164, 116, 252), 3)

            if qr_data in scanned_qrs:
                root.after(0, status_label.config, {"text": "Duplicate QR detected!", "fg": "#FF5555"})
                root.after(0, flash_color, "#FF5555", 1, 0.5)
            else:
                student_id, student_name = get_student_by_qr(qr_data)
                if student_id:
                    # QR valid, entry নাও, face থাকুক বা না থাকুক
                    entry = {
                        'ID': student_id,
                        'Name': student_name,
                        'Time': datetime.now().strftime('%H:%M:%S')
                    }
                    entry_list.append(entry)
                    scanned_qrs.add(qr_data)
                    root.after(0, status_label.config, {"text": f"Welcome {student_name} via QR!", "fg": COLOR_PRIMARY})
                    root.after(0, flash_color, COLOR_PRIMARY, 2, 0.3)
                    root.after(0, lambda: tree.insert('', 'end', values=(student_id, student_name, entry['Time'])))
                else:
                    root.after(0, status_label.config, {"text": "Invalid QR Code!", "fg": "#FF5555"})
                    root.after(0, flash_color, "#FF5555", 1, 0.5)

            qr_found = True
            break

        # যদি QR পাওয়া না যায়, তাহলে মুখ দেখে এন্ট্রি নাও
        if not qr_found:
            if len(faces) > 0:
                # মুখ যদি নতুন হয় (duplicate না হয়)
                # আমরা শুধু face detect করছি, তাই name বা id নেই, তাই generic entry
                # এখানে তুমি চাইলে "FaceDetected" নামে বা অন্যভাবে handle করতে পারো
                face_id = "FaceDetected"
                if face_id not in scanned_faces:
                    entry = {
                        'ID': "FaceDetected",
                        'Name': "Face Detected (No QR)",
                        'Time': datetime.now().strftime('%H:%M:%S')
                    }
                    entry_list.append(entry)
                    scanned_faces.add(face_id)
                    root.after(0, status_label.config, {"text": "Entry by Face Detection!", "fg": COLOR_PRIMARY})
                    root.after(0, flash_color, COLOR_PRIMARY, 2, 0.3)
                    root.after(0, lambda: tree.insert('', 'end', values=(entry['ID'], entry['Name'], entry['Time'])))
            else:
                root.after(0, status_label.config, {"text": "Scan Status", "fg": COLOR_LIGHT})

        # Tkinter এর জন্য OpenCV ইমেজ কনভার্ট
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.config(image=imgtk)

        if not root.winfo_exists():
            break

    cap.release()
    cv2.destroyAllWindows()

def start_scan():
    t = threading.Thread(target=scan_qr_or_face, daemon=True)
    t.start()

start_scan()

def on_close():
    if entry_list:
        df = pd.DataFrame(entry_list)
        df.to_csv("entries.csv", index=False)
        messagebox.showinfo("Saved", "✅ Entries saved to 'entries.csv'")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
