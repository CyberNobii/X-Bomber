
import sys
import time
import getpass
import hashlib
import uuid
from datetime import datetime, timezone
from colorama import init, Fore, Style
import webbrowser 


init(autoreset=True)
ln_k="https://t.me/hackHuub"

MAX_ATTEMPTS = 3
LOG_FILE = "attempts.log"
SESSION_ID = uuid.uuid4().hex[:12]

__internal_flag = None


def type_write(text, speed=0.015, color=Fore.WHITE):

    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(Style.RESET_ALL + "\n")


def spinner(seconds=1.2, label="Checking token", color=Fore.CYAN):
    chars = "|/-\\"
    end = time.time() + seconds
    sys.stdout.write(color + label + " " + Style.RESET_ALL)
    i = 0
    while time.time() < end:
        sys.stdout.write(chars[i % 4])
        sys.stdout.flush()
        time.sleep(0.12)
        sys.stdout.write("\b")
        i += 1
    sys.stdout.write(Fore.GREEN + "done\n" + Style.RESET_ALL)


def mask_phone(p):
    digits = "".join(c for c in p if c.isdigit())
    if len(digits) <= 4:
        return "*" * len(digits)
    return "*" * (len(digits) - 4) + digits[-4:]


def log_attempt(phone, candidate):
    masked = mask_phone(phone)
    tag = "<EMPTY>" if candidate == "" else hashlib.sha256(candidate.encode()).hexdigest()
    now = datetime.now(timezone.utc).isoformat()

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now} | session={SESSION_ID} | phone={masked} | token={tag}\n")
    except:
        pass


def valid_phone(p):
    return sum(c.isdigit() for c in p) >= 7


BANNER = f"""
{Fore.CYAN}{Style.BRIGHT} 
    )                                          
 ( /(         (                   )            
 )\())      ( )\          )    ( /(    (   (   
((_)\  ___  )((_)  (     (     )\())  ))\  )(  
__((_)|___|((_)_   )\    )\  '((_)\  /((_)(()\ 
\ \/ /      | _ ) ((_) _((_)) | |(_)(_))   ((_)
 >  <       | _ \/ _ \| '  \()| '_ \/ -_) | '_|
/_/\_\      |___/\___/|_|_|_| |_.__/\___| |_|  v1.0.0

{Style.RESET_ALL}
"""

def main():
    print(BANNER)
    type_write(f"X-Bomber", 0.01,Fore.CYAN)
    type_write(f" Session: {SESSION_ID}\n", 0.01, Fore.YELLOW)

    
    phone = input(Fore.CYAN + "\t Enter phone number: " + Style.RESET_ALL).strip()

    if not valid_phone(phone):
        print(Fore.RED + " Invalid phone number. Exiting." + Style.RESET_ALL)
        sys.exit(1)

    print()
    type_write(" Enter access token to continue.\n", 0.01, Fore.BLUE)

    attempts = 0
    showed_support = False

    while attempts < MAX_ATTEMPTS:
        token = getpass.getpass(Fore.BLUE + "\t Access token: " + Style.RESET_ALL).strip()

        if token == "":
            print(Fore.YELLOW + "\t No token entered. Try again.\n" + Style.RESET_ALL)
            log_attempt(phone, "")
            continue

        spinner(1.2, "\t Checking token", color=Fore.CYAN)

        ok = False
        if __internal_flag and token == __internal_flag:
            ok = True

        if ok:
            print(Fore.GREEN + f"\t Access granted for {mask_phone(phone)}" + Style.RESET_ALL)
            return

        attempts += 1
        log_attempt(phone, token)
        remaining = MAX_ATTEMPTS - attempts

        print(Fore.RED + f"\t Access denied. Attempts left: {remaining}\n" + Style.RESET_ALL)

        if not showed_support:
            type_write("\t To Obtain Valid Access Key, contact support.", 0.01, Fore.MAGENTA)
            type_write("\t Support: https://t.me/hackHuub\n", 0.01, Fore.CYAN)
            time.sleep(4)
            webbrowser.open(ln_k)
            time.sleep(7)
            showed_support = True

    type_write("\t Authentication failed.", 0.01, Fore.RED)
    type_write(f"\t Session ID: {SESSION_ID}", 0.01, Fore.YELLOW)
    sys.exit(1)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Fore.YELLOW + " Interrupted. Exiting." + Style.RESET_ALL)
        sys.exit(0)