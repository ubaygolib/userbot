import os
import asyncio
from pyrogram import Client, filters, enums

# --- SOZLAMALAR ---
API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION = os.environ.get("TG_SESSION", "")
OWNER_ID = 5471176468

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION) if SESSION else Client("userbot", api_id=API_ID, api_hash=API_HASH)

# Holat o'zgaruvchilari
away_mode = False
away_text = ""
known_users = set()

# --- TAYYOR JAVOBLAR (Produktiv hayot tarzi uchun) ---
MESSAGES = {
    "uyqu": "Assalomu alaykum! Hozir uxlab dam olyapman (Bomdodgacha). Uyg'onganimdan keyin o'zim xabaringizga javob yozaman 🌙",
    "yugurish": "Salom! Hozir yugurish mashg'ulotida edim. Masofani yugurib bo'lgach, albatta aloqaga chiqaman 🏃‍♂️",
    "gym": "Assalomu alaykum! Hozir sport zalida (gym) mashg'ulot qilyapman. Mashqlarim tugagach o'zim yozaman 💪",
    "ish": "Assalomu alaykum! Hozir ishda, ma'lumotlar bazasi va jadvallar bilan ishlab, jarayonga butunlay sho'ng'ib ketgan edim. Diqqatimni bo'la olmayman, bo'shashim bilan o'zim javob qaytaraman 💻",
    "majlis": "Assalomu alaykum! Hozir muhim majlisdaman. Qatnashayotganim uchun telefonim ovozsiz rejimda. Tugashi bilan o'zim aloqaga chiqaman 📊",
    "dam": "Assalomu alaykum! Bugun dam olish kuni, shaxsiy ishlar va hordiq chiqarish bilan bandman. Tez orada aloqaga chiqaman ☕️",
    "tog": "Assalomu alaykum! Hozir tog'daman, bu yerda umuman antena yo'q (aloqa yo'q). Pastga tushganimdan keyin o'zim yozaman ⛰️",
    "hordiq": "Assalomu alaykum! Hozir boshqa joyda, dam olish ta'tilida edim. Telefonimga kam qarayapman, bo'sh vaqtim bo'lishi bilan javob yozaman 🌴",
    "on": "Assalomu alaykum! Xabaringizni oldim, lekin hozir biroz band edim. Vaqt topishim bilan o'zim sizga aloqaga chiqaman."
}

# --- BUYRUQLAR ---

@app.on_message(filters.command("away", prefixes=[".", "/"]) & filters.me)
async def toggle_away(c, msg):
    global away_mode, away_text, known_users
    
    args = msg.text.split()
    
    # Agar faqat .away yozilsa, yo'riqnoma chiqaradi
    if len(args) == 1:
        menu_text = "**🤖 Buyruqni tanlang:**\n\n"
        menu_text += "`.away uyqu` - Bomdodgacha uyqu\n"
        menu_text += "`.away yugurish` - Yugurish mashg'uloti\n"
        menu_text += "`.away gym` - Sport zal\n"
        menu_text += "`.away ish` - Chuqur ish (Deep work)\n"
        menu_text += "`.away majlis` - Majlisdaman\n"
        menu_text += "`.away dam` - Dam olish kuni\n"
        menu_text += "`.away tog` - Tog'daman (Antena yo'q)\n"
        menu_text += "`.away hordiq` - Ta'til/Sayohat\n"
        menu_text += "`.away on` - Umumiy bandlik\n"
        menu_text += "`.away off` - O'chirish"
        await msg.edit(menu_text)
        return
        
    mode = args[1].lower()
    
    # O'chirish buyrug'i
    if mode == "off":
        away_mode = False
        away_text = ""
        known_users.clear() # O'chirilganda xotirani ham tozalaymiz
        await msg.edit("🤖 Away **O'CHIRILDI**. Bot hech kimga avtomat javob bermaydi.")
        
    # Tayyor shablonlardan birini tanlash
    elif mode in MESSAGES:
        away_mode = True
        away_text = MESSAGES[mode]
        await msg.edit(f"🤖 Away **YOQILDI** ({mode.upper()}).\n\n📝 Javobingiz: {away_text}")
        
    # Agar qo'lda boshqa gap yozilsa (masalan: .away mehmondaman)
    else:
        away_mode = True
        away_text = msg.text.split(maxsplit=1)[1]
        await msg.edit(f"🤖 Away **YOQILDI** (Maxsus).\n\n📝 Javobingiz: {away_text}")

@app.on_message(filters.command("status", prefixes=[".", "/"]) & filters.me)
async def status(c, msg):
    status_text = "YOQILGAN ✅" if away_mode else "O'CHIRILGAN ❌"
    display_text = away_text if away_text else "Yo'q"
    
    await msg.edit(
        f"**Userbot Holati:**\n"
        f"🤖 Away: {status_text}\n"
        f"📝 Matn: {display_text}\n"
        f"👥 Spam-himoya (javob berilganlar): {len(known_users)}"
    )

# --- AVTOMATIK JAVOB ---

@app.on_message(filters.private & ~filters.me)
async def auto_reply(c, msg):
    if not away_mode:
        return
        
    user = msg.from_user
    if not user or user.id == OWNER_ID:
        return
        
    uid = user.id
    text = msg.text or msg.caption or ""
    if not text.strip():
        return

    # SPAM HIMOYA: Har bir kishiga faqat bir marta javob qaytarish
    if uid in known_users:
        return
        
    known_users.add(uid)

    name = user.first_name or "Do'stim"
    
    try:
        await c.send_chat_action(msg.chat.id, enums.ChatAction.TYPING)
        await asyncio.sleep(2)
    except:
        pass
    
    reply_text = f"{away_text}\n\n*(Avtomatik xabar)*"

    try:
        await msg.reply(reply_text)
        print(f"JAVOB ✅ {name} ga yuborildi.")
    except Exception as e:
        print(f"Xatolik: {e}")

# --- ISHGA TUSHIRISH ---
async def main():
    print("Userbot tayyor! Produktiv rejimlar ishga tushdi.")
    await app.start()
    await enums.pyrogram.utils.idle()

if __name__ == "__main__":
    asyncio.run(main())