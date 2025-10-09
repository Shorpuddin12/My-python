import tkinter as tk
from datetime import datetime

def save_message():
    message = entry.get("1.0", tk.END).strip()
    if message:
        with open("saved_messages.txt", "a", encoding="utf-8") as file:
            file.write(f"[{datetime.now()}] {message}\n")
        entry.delete("1.0", tk.END)
        status_label.config(text="✅ Message saved!")

app = tk.Tk()
app.title("Facebook Message Logger")
app.geometry("400x300")

label = tk.Label(app, text="Type your message:")
label.pack(pady=10)

entry = tk.Text(app, height=8)
entry.pack(pady=5)

save_btn = tk.Button(app, text="Save Message", command=save_message)
save_btn.pack(pady=5)

status_label = tk.Label(app, text="")
status_label.pack()

app.mainloop()
