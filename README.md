# Flüsterfuchs Keylogger


![Flüsterfuchs (1)](https://github.com/Wadee-Haddad/Fl-sterfuchs/assets/117990238/51936cd1-c0b6-4a9b-904e-802862ef498a)



Flüsterfuchs is a cyberweapon (malware) keylogger implemented in Python for educational purposes. It captures keyboard input and associates it with the foreground process (active window). The graphical user interface (GUI) is built using the Tkinter library for ease of use.

## Features

1. **Process Identification:** Identifies the foreground process and logs keyboard input associated with it.
2. **Color-coded Output:** The output in the GUI is color-coded based on the foreground process.
3. **Start/Stop Control:** The keylogger can be started and stopped through the GUI.

## Implementation Details

### Libraries Used

- **ctypes:** Used for calling functions in DLLs/shared libraries.
- **wintypes:** Provides data types for Windows API functions.
- **tkinter:** Used for creating the graphical user interface (GUI).

### Windows API Functions

1. **GetForegroundWindow:** Retrieves the handle to the foreground window.
2. **GetWindowTextLengthA and GetWindowTextA:** Retrieve the length and text of the window title.
3. **GetKeyState:** Determines the state of a key.
4. **GetKeyboardState:** Retrieves the status of all virtual keys.
5. **ToAscii:** Translates a virtual-key code and keyboard state to characters.
6. **SetWindowsHookExA:** Installs a hook procedure into a hook chain.
7. **CallNextHookEx:** Passes the hook information to the next hook procedure.
8. **UnhookWindowsHookEx:** Removes a hook procedure.

### Keylogger Logic

1. **Hook Procedure (`hook_function`):** Intercepts and logs keyboard events.
2. **KBDLLHOOKSTRUCT:** A structure representing information about a low-level keyboard input event.
3. **Process Identification (`get_foreground_process`):** Retrieves the title of the foreground window.
4. **Logging:** Keyboard input is logged and displayed in the GUI with color-coded text.
5. **ASCII Logo:** An ASCII art logo is displayed at startup.

## GUI

- **Start Keylogger Button:** Initiates the keylogging process.
- **Stop Keylogger Button:** Stops the keylogging process.
- **Output Text Area:** Displays the captured keyboard input.

## How to Use

1. **Start Keylogger:** Click the "Start Keylogger" button.
2. **Capture Input:** The keylogger will capture keyboard input and display it in the GUI.
3. **Stop Keylogger:** Click the "Stop Keylogger" button.

## Disclaimer

Flüsterfuchs is an educational project. Unauthorized use of keyloggers is illegal and unethical.

## Credits

Developed by [Your Name] for educational purposes.

## License

Flüsterfuchs is released under the [License Name] license. See the LICENSE file for more details.
