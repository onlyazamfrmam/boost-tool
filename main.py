import tls_client, threading, os, requests
from base64 import b64encode
import json, time
from colorama import Fore, Style, init

# تهيئة مكتبة colorama للألوان
init(autoreset=True)

__useragent__ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
build_number = 165486
cv = "108.0.0.0"
__properties__ = b64encode(
    json.dumps(
        {
            "os": "Windows",
            "browser": "Chrome",
            "device": "PC",
            "system_locale": "en-GB",
            "browser_user_agent": __useragent__,
            "browser_version": cv,
            "os_version": "10",
            "referrer": "https://discord.com/channels/@me",
            "referring_domain": "discord.com",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": build_number,
            "client_event_source": None
        },
        separators=(',', ':')
    ).encode()
).decode()

# دالة طباعة البانر عند التشغيل
def print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = f"""
{Fore.GREEN}    ██████╗ ██████╗ ██████╗ 
{Fore.GREEN}    ██╔════╝ ██╔══██╗██╔══██╗
{Fore.GREEN}    ███████╗ ██████╔╝██████╔╝
{Fore.GREEN}    ██╔═══██╗██╔══██╗██╔══██╗
{Fore.GREEN}    ╚██████╔╝██║  ██║██████╔╝
{Fore.GREEN}     ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
    """
    print(banner)

# تشغيل البانر عند تشغيل البرنامج
print_banner()

# إدخال معلومات السيرفر والاسم
guild = input(f"{Fore.GREEN}[!] Server ID: {Fore.WHITE}")
nickname = input(f"{Fore.GREEN}[!] Nickname: {Fore.WHITE}")

# وظيفة للانضمام إلى سيرفر باستخدام الدعوة
def join_server(token):
    invite = extract_invite_from_token(token)  # استخراج كود الدعوة من التوكن
    url = f"https://discord.com/api/v9/invites/{invite}"
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    
    if response.status_code in (200, 201, 204):
        print(f"{Fore.GREEN}[+] Successfully joined server: {guild}")
    else:
        print(f"{Fore.RED}[-] Failed to join server: {guild} | {response.status_code}")

# دالة لتغيير الاسم داخل السيرفر
def rename(token):
    headers = get_headers(token)
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    response = client.patch(f"https://discord.com/api/v9/guilds/{guild}/members/@me", json={"nick": nickname})
    
    if response.status_code in (200, 201, 204):
        print(f"{Fore.GREEN}[+] Nickname changed to {nickname}")
    else:
        print(f"{Fore.RED}[-] Failed to change nickname")

# دالة لتفعيل الـ Nitro Boost
def boost_server(token):
    headers = get_headers(token)
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    response = client.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots")
    
    for slot in response.json():
        slot_id = slot['id']
        payload = {"user_premium_guild_subscription_slot_ids": [slot_id]}
        boost_response = client.put(f"https://discord.com/api/v9/guilds/{guild}/premium/subscriptions", json=payload)
        
        if boost_response.status_code in (200, 201, 204):
            print(f"{Fore.GREEN}[+] Boosted {guild}")

# الوظيفة الأساسية لكل توكن
def main(token):
    join_server(token)  # الانضمام للسيرفر تلقائيًا
    rename(token)  # تغيير الاسم
    boost_server(token)  # تفعيل الـ Boost

# تشغيل البوت باستخدام التوكنات المخزنة
with open("boost-tokens.txt", "r") as f:
    tokens = [tk.strip() for tk in f.readlines()]

for tk in tokens:
    threading.Thread(target=main, args=(tk,)).start()