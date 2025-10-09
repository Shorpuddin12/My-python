import datetime

# User Info
name = "Ibrahim Hosen"
dob = "17-12-2007"
email = "ihibrahimhosen22@gmail.com"
phone = "01780883128"
address = "Mirpur 1, Dhaka"
skills = ["Python", "Web Development", "Graphics", "ChatGPT Prompt"]
issue_date = datetime.date.today()

# Print Card Border
print("="*40)
print("💳 PYTHON MASTER CARD".center(40))
print("="*40)

# Info Display
print(f"👤 Name       : {name}")
print(f"🎂 DOB        : {dob}")
print(f"📧 Email      : {email}")
print(f"📱 Phone      : {phone}")
print(f"🏠 Address    : {address}")
print(f"🛠️  Skills     : {', '.join(skills)}")
print(f"🗓️  Issued on  : {issue_date}")
print("="*40)
print("✅ Verified by Python Authority 🐍")
print("="*40)
