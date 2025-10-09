import qrcode
import json

# 10 জনের নাম ও ID ডাটা
data = [
    {"name": "Rahul", "ID": 101},
    {"name": "Suman", "ID": 102},
    {"name": "Maruf", "ID": 103},
    {"name": "Farhan", "ID": 104},
    {"name": "Nabila", "ID": 105},
    {"name": "Zahid", "ID": 106},
    {"name": "Saif", "ID": 107},
    {"name": "Tanvir", "ID": 108},
    {"name": "Lima", "ID": 109},
    {"name": "Atik", "ID": 110},
]

for person in data:
    # প্রতিটি ব্যক্তির ডাটাকে JSON স্ট্রিং এ কনভার্ট করা
    person_data_str = json.dumps(person, ensure_ascii=False)

    # QR কোড তৈরি
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(person_data_str)
    qr.make(fit=True)

    # ইমেজ জেনারেট করা
    img = qr.make_image(fill_color="black", back_color="white")

    # ফাইল নাম, যেমন Rahul_101.png
    filename = f"{person['name']}_{person['ID']}.png"
    img.save(filename)
    print(f"QR code created for {person['name']} and saved as {filename}")
