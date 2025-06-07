import os
import sys
import ctypes
import subprocess
import shutil
import time

def is_admin():
    """
    Check if the script is running with administrator privileges.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    """
    Relaunch the current script with administrator privileges using UAC prompt.
    """
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )

def clear_screen():
    """
    Clear the console screen (Windows).
    """
    os.system('cls')

def show_banner():
    """
    Display a simple ASCII banner with the text 'arshiakia'.
    """
    text = "arshiakia"
    border = "+" + "-" * (len(text) + 4) + "+"
    print(border)
    print(f"|  {text}  |")
    print(border)

def clear_dns():
    """
    Reset DNS settings on all active network adapters to DHCP (automatic),
    without loading any PowerShell profiles and bypassing execution policy.
    """
    print("[*] Resetting DNS servers to automatic (DHCP) on all active adapters...")
    ps_command = (
        "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | "
        "ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ResetServerAddresses }"
    )
    subprocess.run([
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-Command", ps_command
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] DNS reset complete.")
    input("\nPress Enter to continue...")

def clear_proxy():
    """
    Remove any system proxy settings (WinHTTP and Internet Settings in registry).
    """
    print("[*] Clearing system proxy settings...")
    # Reset WinHTTP proxy
    subprocess.run(["netsh", "winhttp", "reset", "proxy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Remove IE/WinInet proxy settings from registry for current user
    reg_paths = [
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    ]
    for path in reg_paths:
        subprocess.run([
            "reg", "delete", path, "/v", "ProxyEnable", "/f"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([
            "reg", "delete", path, "/v", "ProxyServer", "/f"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] Proxy settings cleared.")
    input("\nPress Enter to continue...")

def flash_ip():
    """
    Release and renew the IP address, and flush DNS cache.
    """
    print("[*] Releasing IP address...")
    subprocess.run(["ipconfig", "/release"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    print("[*] Renewing IP address...")
    subprocess.run(["ipconfig", "/renew"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    print("[*] Flushing DNS resolver cache...")
    subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] IP flush and DNS flush complete.")
    input("\nPress Enter to continue...")

def disable_firewall():
    """
    Turn off Windows Firewall for all profiles.
    """
    print("[*] Disabling Windows Firewall for all profiles...")
    subprocess.run([
        "netsh", "advfirewall", "set", "allprofiles", "state", "off"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] Windows Firewall disabled.")
    input("\nPress Enter to continue...")

def clear_hosts_file():
    """
    Overwrite the hosts file with default content (loopback entries only).
    """
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    default_content = "127.0.0.1\tlocalhost\n::1\tlocalhost\n"
    try:
        print("[*] Clearing hosts file...")
        with open(hosts_path, "w") as f:
            f.write(default_content)
        print("[+] Hosts file reset to default.")
    except PermissionError:
        print("[!] Permission denied while clearing hosts file.")
    input("\nPress Enter to continue...")

def clear_all_internet_settings():
    """
    Execute all internet-related operations in sequence.
    """
    clear_dns()
    clear_proxy()
    flash_ip()
    disable_firewall()
    clear_hosts_file()

def clear_browser_cache():
    """
    Ask the user which browser’s cache to clear, then remove the cache folder.
    """
    user_profile = os.environ.get("USERPROFILE", "")
    browsers = {
        "1": ("Google Chrome", os.path.join(
            user_profile, r"AppData\Local\Google\Chrome\User Data\Default\Cache"
        )),
        "2": ("Mozilla Firefox", None),  # Firefox cache path varies by profile
        "3": ("Microsoft Edge", os.path.join(
            user_profile, r"AppData\Local\Microsoft\Edge\User Data\Default\Cache"
        )),
        "4": ("Brave", os.path.join(
            user_profile, r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Cache"
        )),
        "5": ("Opera", os.path.join(
            user_profile, r"AppData\Local\Opera Software\Opera Stable\Cache"
        )),
    }

    clear_screen()
    print("=== Clear Browser Cache ===")
    for key, (name, _) in browsers.items():
        print(f"{key}. {name}")
    print("6. Back to Internet Menu")

    choice = input("Enter choice: ").strip()
    if choice == "6":
        return
    if choice in browsers:
        name, cache_path = browsers[choice]
        if name == "Mozilla Firefox":
            ff_base = os.path.join(user_profile, r"AppData\Local\Mozilla\Firefox\Profiles")
            if os.path.isdir(ff_base):
                for profile in os.listdir(ff_base):
                    cache_dir = os.path.join(ff_base, profile, "cache2")
                    if os.path.isdir(cache_dir):
                        try:
                            print(f"[*] Clearing {name} cache at {cache_dir} ...")
                            shutil.rmtree(cache_dir, ignore_errors=True)
                            print(f"[+] {name} cache cleared.")
                        except Exception as e:
                            print(f"[!] Failed to clear {name} cache: {e}")
                    else:
                        print(f"[!] Cache directory not found for profile: {profile}")
            else:
                print(f"[!] Firefox profiles directory not found: {ff_base}")
        else:
            if os.path.isdir(cache_path):
                try:
                    print(f"[*] Clearing {name} cache at {cache_path} ...")
                    shutil.rmtree(cache_path, ignore_errors=True)
                    print(f"[+] {name} cache cleared.")
                except Exception as e:
                    print(f"[!] Failed to clear {name} cache: {e}")
            else:
                print(f"[!] Cache path not found: {cache_path}")
    else:
        print("[!] Invalid choice.")

    input("\nPress Enter to continue...")

def internet_menu():
    """
    Display the Internet menu and execute corresponding actions.
    """
    while True:
        clear_screen()
        print("=== Internet Menu ===")
        print("1. Delete all DNS settings")
        print("2. Delete proxy settings")
        print("3. Flush IP (release, renew, flushdns)")
        print("4. Disable Windows Firewall")
        print("5. Clear hosts file")
        print("6. Perform all of the above")
        print("7. Clear browser cache")
        print("8. Return to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            clear_screen()
            clear_dns()
        elif choice == "2":
            clear_screen()
            clear_proxy()
        elif choice == "3":
            clear_screen()
            flash_ip()
        elif choice == "4":
            clear_screen()
            disable_firewall()
        elif choice == "5":
            clear_screen()
            clear_hosts_file()
        elif choice == "6":
            clear_screen()
            clear_all_internet_settings()
            reboot_choice = input("Do you want to reboot now? (y/n): ").strip().lower()
            if reboot_choice == "y":
                print("[*] Rebooting the system...")
                subprocess.run(["shutdown", "/r", "/t", "0"])
                sys.exit(0)
            else:
                print("[*] Returning to Internet Menu without reboot.")
                input("\nPress Enter to continue...")
        elif choice == "7":
            clear_screen()
            clear_browser_cache()
        elif choice == "8":
            break
        else:
            print("[!] Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def check_winget_available():
    """
    Check if winget is available on the system.
    """
    try:
        subprocess.run(["winget", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def install_program():
    """
    Display categories and let the user choose a program to install via winget.
    """
    if not check_winget_available():
        print("[!] winget is not available on this system. Cannot install programs.")
        input("\nPress Enter to continue...")
        return

    while True:
        clear_screen()
        print("=== Install Program ===")
        print("1. Browsers")
        print("2. Programming Software")
        print("3. Essential Tools")
        print("4. Back to Program Menu")
        cat_choice = input("Choose a category: ").strip()

        if cat_choice == "1":
            browsers = {
                "1": ("Google.Chrome", "Google Chrome"),
                "2": ("Mozilla.Firefox", "Mozilla Firefox"),
                "3": ("Microsoft.Edge", "Microsoft Edge"),
                "4": ("BraveSoftware.BraveBrowser", "Brave"),
                "5": ("Opera.Opera", "Opera"),
                "6": ("TorBrowser.TorBrowser", "Tor Browser"),
            }
            clear_screen()
            print("Select a browser to install:")
            for key, (_, name) in browsers.items():
                print(f"{key}. {name}")
            print("7. Back")
            b_choice = input("Enter choice: ").strip()
            if b_choice in browsers:
                pkg_id, name = browsers[b_choice]
                print(f"[*] Installing {name} ...")
                subprocess.run(["winget", "install", "--id", pkg_id, "--silent"])
                print(f"[+] {name} installation command executed.")
            else:
                print("[*] Returning to Install Program menu.")
            input("\nPress Enter to continue...")
        elif cat_choice == "2":
            prog_tools = {
                "1": ("Python.Python.3", "Python 3"),
                "2": ("Git.Git", "Git"),
                "3": ("Microsoft.VisualStudioCode", "Visual Studio Code"),
                "4": ("OpenJS.NodeJS", "Node.js"),
                "5": ("Oracle.JavaRuntimeEnvironment", "Java JDK"),
                "6": ("JetBrains.IntelliJIDEA.Community", "IntelliJ IDEA Community"),
                "7": ("Microsoft.PowerShell", "PowerShell"),
                "8": ("GoLang.Go", "Go"),  # Winget ID for Go
                "9": ("RustLang.Rust", "Rust"),  # Winget ID for Rust
            }
            clear_screen()
            print("Select a programming software to install:")
            for key, (_, name) in prog_tools.items():
                print(f"{key}. {name}")
            print("10. Back")
            p_choice = input("Enter choice: ").strip()
            if p_choice in prog_tools:
                pkg_id, name = prog_tools[p_choice]
                print(f"[*] Installing {name} ...")
                subprocess.run(["winget", "install", "--id", pkg_id, "--silent"])
                print(f"[+] {name} installation command executed.")
            else:
                print("[*] Returning to Install Program menu.")
            input("\nPress Enter to continue...")
        elif cat_choice == "3":
            tools = {
                "1": ("7zip.7zip", "7-Zip"),
                "2": ("VideoLAN.VLC", "VLC Media Player"),
                "3": ("Notepad++.Notepad++", "Notepad++"),
                "4": ("RARLab.WinRAR", "WinRAR"),
                "5": ("Spotify.Spotify", "Spotify"),
                "6": ("Zoom.Zoom", "Zoom"),
                "7": ("Docker.DockerDesktop", "Docker Desktop"),
                "8": ("Postman.Postman", "Postman"),
                "9": ("Discord.Discord", "Discord"),
            }
            clear_screen()
            print("Select an essential tool to install:")
            for key, (_, name) in tools.items():
                print(f"{key}. {name}")
            print("10. Back")
            t_choice = input("Enter choice: ").strip()
            if t_choice in tools:
                pkg_id, name = tools[t_choice]
                print(f"[*] Installing {name} ...")
                subprocess.run(["winget", "install", "--id", pkg_id, "--silent"])
                print(f"[+] {name} installation command executed.")
            else:
                print("[*] Returning to Install Program menu.")
            input("\nPress Enter to continue...")
        elif cat_choice == "4":
            break
        else:
            print("[!] Invalid category. Please try again.")
            input("\nPress Enter to continue...")

def update_program():
    """
    Display program list and let the user choose one to update via winget.
    """
    if not check_winget_available():
        print("[!] winget is not available on this system. Cannot update programs.")
        input("\nPress Enter to continue...")
        return

    programs = {
        "1": ("Google.Chrome", "Google Chrome"),
        "2": ("Mozilla.Firefox", "Mozilla Firefox"),
        "3": ("Microsoft.Edge", "Microsoft Edge"),
        "4": ("BraveSoftware.BraveBrowser", "Brave"),
        "5": ("Opera.Opera", "Opera"),
        "6": ("TorBrowser.TorBrowser", "Tor Browser"),
        "7": ("Python.Python.3", "Python 3"),
        "8": ("Git.Git", "Git"),
        "9": ("Microsoft.VisualStudioCode", "Visual Studio Code"),
        "10": ("OpenJS.NodeJS", "Node.js"),
        "11": ("Oracle.JavaRuntimeEnvironment", "Java JDK"),
        "12": ("JetBrains.IntelliJIDEA.Community", "IntelliJ IDEA Community"),
        "13": ("Microsoft.PowerShell", "PowerShell"),
        "14": ("GoLang.Go", "Go"),
        "15": ("RustLang.Rust", "Rust"),
        "16": ("7zip.7zip", "7-Zip"),
        "17": ("VideoLAN.VLC", "VLC Media Player"),
        "18": ("Notepad++.Notepad++", "Notepad++"),
        "19": ("RARLab.WinRAR", "WinRAR"),
        "20": ("Spotify.Spotify", "Spotify"),
        "21": ("Zoom.Zoom", "Zoom"),
        "22": ("Docker.DockerDesktop", "Docker Desktop"),
        "23": ("Postman.Postman", "Postman"),
        "24": ("Discord.Discord", "Discord"),
    }

    clear_screen()
    print("=== Update Program ===")
    for key, (_, name) in programs.items():
        print(f"{key}. {name}")
    print("25. Back to Program Menu")

    choice = input("Enter the number of the program to update: ").strip()
    if choice in programs:
        pkg_id, name = programs[choice]
        print(f"[*] Updating {name} ...")
        subprocess.run(["winget", "upgrade", "--id", pkg_id, "--silent"])
        print(f"[+] {name} update command executed.")
    else:
        print("[*] Returning to Program menu.")
    input("\nPress Enter to continue...")

def clear_program_cache():
    """
    Display program list and let the user choose one to clear its cache.
    Only a few common cache paths are defined here.
    """
    user_profile = os.environ.get("USERPROFILE", "")
    appdata = os.environ.get("APPDATA", "")
    local_appdata = os.environ.get("LOCALAPPDATA", "")

    programs = {
        "1": ("Python", os.path.join(local_appdata, r"pip\Cache")),
        "2": ("Git", None),  # No standard cache path
        "3": ("Visual Studio Code", os.path.join(appdata, r"Code\Cache")),
        "4": ("Node.js", None),  # Could run 'npm cache clean' instead
        "5": ("Java JDK", None),
        "6": ("7-Zip", None),
        "7": ("VLC Media Player", None),
        "8": ("Notepad++", os.path.join(appdata, r"Notepad++\cache")),
        "9": ("WinRAR", None),
        "10": ("Spotify", None),
        "11": ("Zoom", None),
        "12": ("Docker Desktop", None),
        "13": ("Postman", None),
        "14": ("Discord", None),
    }

    clear_screen()
    print("=== Clear Program Cache ===")
    for key, (name, _) in programs.items():
        print(f"{key}. {name}")
    print("15. Back to Program Menu")

    choice = input("Enter the number of the program to clear cache: ").strip()
    if choice in programs:
        name, cache_path = programs[choice]
        if cache_path and os.path.isdir(cache_path):
            try:
                print(f"[*] Clearing cache for {name} at {cache_path} ...")
                shutil.rmtree(cache_path, ignore_errors=True)
                print(f"[+] {name} cache cleared.")
            except Exception as e:
                print(f"[!] Failed to clear cache for {name}: {e}")
        else:
            print(f"[!] Cache path not defined or does not exist for {name}.")
    else:
        print("[*] Returning to Program menu.")
    input("\nPress Enter to continue...")

def uninstall_program():
    """
    Display program list and let the user choose one to uninstall via winget.
    """
    if not check_winget_available():
        print("[!] winget is not available on this system. Cannot uninstall programs.")
        input("\nPress Enter to continue...")
        return

    programs = {
        "1": ("Google.Chrome", "Google Chrome"),
        "2": ("Mozilla.Firefox", "Mozilla Firefox"),
        "3": ("Microsoft.Edge", "Microsoft Edge"),
        "4": ("BraveSoftware.BraveBrowser", "Brave"),
        "5": ("Opera.Opera", "Opera"),
        "6": ("TorBrowser.TorBrowser", "Tor Browser"),
        "7": ("Python.Python.3", "Python 3"),
        "8": ("Git.Git", "Git"),
        "9": ("Microsoft.VisualStudioCode", "Visual Studio Code"),
        "10": ("OpenJS.NodeJS", "Node.js"),
        "11": ("Oracle.JavaRuntimeEnvironment", "Java JDK"),
        "12": ("JetBrains.IntelliJIDEA.Community", "IntelliJ IDEA Community"),
        "13": ("Microsoft.PowerShell", "PowerShell"),
        "14": ("GoLang.Go", "Go"),
        "15": ("RustLang.Rust", "Rust"),
        "16": ("7zip.7zip", "7-Zip"),
        "17": ("VideoLAN.VLC", "VLC Media Player"),
        "18": ("Notepad++.Notepad++", "Notepad++"),
        "19": ("RARLab.WinRAR", "WinRAR"),
        "20": ("Spotify.Spotify", "Spotify"),
        "21": ("Zoom.Zoom", "Zoom"),
        "22": ("Docker.DockerDesktop", "Docker Desktop"),
        "23": ("Postman.Postman", "Postman"),
        "24": ("Discord.Discord", "Discord"),
    }

    clear_screen()
    print("=== Uninstall Program ===")
    for key, (_, name) in programs.items():
        print(f"{key}. {name}")
    print("25. Back to Program Menu")

    choice = input("Enter the number of the program to uninstall: ").strip()
    if choice in programs:
        pkg_id, name = programs[choice]
        confirm = input(f"Are you sure you want to uninstall {name}? (y/n): ").strip().lower()
        if confirm == "y":
            print(f"[*] Uninstalling {name} ...")
            subprocess.run(["winget", "uninstall", "--id", pkg_id, "--silent"])
            print(f"[+] {name} uninstall command executed.")
        else:
            print(f"[*] Skipped uninstalling {name}.")
    else:
        print("[*] Returning to Program menu.")
    input("\nPress Enter to continue...")

def program_menu():
    """
    Display the Program menu and execute corresponding actions.
    """
    while True:
        clear_screen()
        print("=== Program Menu ===")
        print("1. Install Program")
        print("2. Update Program")
        print("3. Clear Program Cache")
        print("4. Uninstall Program")
        print("5. Return to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            install_program()
        elif choice == "2":
            update_program()
        elif choice == "3":
            clear_program_cache()
        elif choice == "4":
            uninstall_program()
        elif choice == "5":
            break
        else:
            print("[!] Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

def main():
    """
    Main entry point: check for admin, show banner, and display the main menu.
    """
    if not is_admin():
        print("[*] Administrator privileges required. Requesting elevation...")
        relaunch_as_admin()
        sys.exit(0)

    while True:
        clear_screen()
        show_banner()
        print("\n=== Main Menu ===")
        print("1. Internet")
        print("2. Program")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            internet_menu()
        elif choice == "2":
            program_menu()
        elif choice == "3":
            print("[*] Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
