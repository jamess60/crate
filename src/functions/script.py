import socket
from colorama import Fore, Back, Style  


def ok_msg(text):
    rettext = Fore.BLACK + Back.GREEN + Style.BRIGHT + " [OK] " + Style.RESET_ALL + " - " + text
    print(rettext)


def info_msg(text):
    rettext = Fore.BLACK + Back.CYAN + Style.BRIGHT + "[INFO]" + Style.RESET_ALL + " - " + text
    print(rettext)


def warn_msg(text):
    rettext = Fore.BLACK + Back.YELLOW + Style.BRIGHT + "[WARN]" + Style.RESET_ALL + " - " + text
    print(rettext)


def err_msg(text):
    rettext = Fore.WHITE + Back.RED + Style.BRIGHT + "[FATAL ERROR]" + Style.RESET_ALL + " - " + text
    print(rettext)


def recovery_confirmation(RECOVERY_ZIP, RECOVERY_HOST, SOURCE_DIR, RUN_MODE):
    hostname = socket.gethostname()

    # Check if the zip file to recover from and host were specified
    if RECOVERY_ZIP is None:
        err_msg("Recovery ZIP file not specified. Use -z to specify the backup source archive.\n\n")
        print("Example: -z /tmp/2023-08-16---10-45-03.zip\n\n")
        exit()
    else:
        info_msg("Using " + str(RECOVERY_ZIP) + " as the backup source.")
    

    if RUN_MODE == "recover-remote" or RUN_MODE == "rr":
        if RECOVERY_HOST is None:
            err_msg("Host to be recovered not specified. Use -s to specify the broken host.")
            print("Example: -s pc-tbed-net-01\n\n")
            exit()
        else:
            info_msg(str(RECOVERY_HOST) + " selected as the host to recover.")
    else:
        info_msg("Localhost selected as the host to recover.")


    print("\n\n")
    warn_msg("Proceeding will KILL AND REMOVE all containers and PERMANENTLY DELETE the source directory. (" + SOURCE_DIR + ")")
    while True:
        recovery_confirm = input("Proceed? - Enter 'DatA-LosS' to proceed:   ")
        if recovery_confirm == "DatA-LosS":
            break
    # print("DEBUG - SKIP CONF INPUT")
    return True



def rainbow(text):
    length = len(text)
    i = 0
    char = text[i]
    try:
        while i != length:
            print(Fore.LIGHTRED_EX + char, end='')
            i = i + 1
            char = text[i]
            print(Fore.LIGHTYELLOW_EX + char, end='')
            i = i + 1
            char = text[i]
            print(Fore.LIGHTGREEN_EX + char, end='')
            i = i + 1
            char = text[i]
            print(Fore.LIGHTCYAN_EX + char, end='')
            i = i + 1
            char = text[i]
            print(Fore.LIGHTBLUE_EX + char, end='')
            i = i + 1
            char = text[i]
            print(Fore.LIGHTMAGENTA_EX + char, end='')
            i = i + 1
            char = text[i]
    except IndexError:
        pass
    return text






