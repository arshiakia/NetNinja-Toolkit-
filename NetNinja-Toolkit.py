# NetNinja Toolkit
# Author: https://github.com/arshiakia/NetNinja-Toolkit

import os
import sys
import subprocess
import ctypes
import shutil

# ----- Admin check & relaunch -----
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

# ----- Operations -----
def clear_dns():
    print("\nClearing DNS settings (reset to DHCP)...")
    subprocess.run(["netsh", "interface", "ip", "set", "dns", "name=Wi-Fi", "dhcp"])
    input("\nOperation complete. Press Enter to return to main menu...")

def clear_proxy():
    print("\nDisabling proxy...")
    subprocess.run(["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                    "/v", "ProxyEnable", "/t", "REG_DWORD", "/d", "0", "/f"])
    input("\nOperation complete. Press Enter to return to main menu...")

def flash_ip():
    print("\nReleasing and renewing IP... (ipconfig /release & /renew)")
    subprocess.run(["ipconfig", "/release"])
    subprocess.run(["ipconfig", "/renew"])
    input("\nOperation complete. Press Enter to return to main menu...")

def firewall_menu():
    while True:
        print("\nFirewall Operations:")
        print("1) Turn Firewall On")
        print("2) Turn Firewall Off")
        print("3) Back to Main Menu")
        choice = input("Select an option: ")
        if choice == '1':
            subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "on"])
            print("Firewall turned ON.")
            input("\nPress Enter to return to firewall menu...")
        elif choice == '2':
            subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "off"])
            print("Firewall turned OFF.")
            input("\nPress Enter to return to firewall menu...")
        elif choice == '3':
            break
        else:
            print("Invalid choice, try again.")

# ----- Hosts & Network -----
def delete_hosts():
    print("\nDeleting hosts file content...")
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    open(hosts_path, 'w').close()
    print("Hosts file cleared.")
    input("\nOperation complete. Press Enter to return to main menu...")

def reset_network():
    print("\nResetting network stack...")
    cmds = [
        ["netsh", "winsock", "reset"],
        ["ipconfig", "/flushdns"],
        ["netsh", "int", "ip", "reset"]
    ]
    for cmd in cmds:
        subprocess.run(cmd)
    print("Network reset complete.")
    input("\nOperation complete. Press Enter to return to main menu...")

# ----- Browser Operations -----
def flush_browser_cache(browser):
    paths = {
        'Chrome': os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Cache"),
        'Edge': os.path.expandvars(r"%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Cache"),
        'Firefox': os.path.expandvars(r"%APPDATA%\\Mozilla\\Firefox\\Profiles")
    }
    path = paths.get(browser)
    if not path or not os.path.exists(path):
        print("Cache path not found.")
    else:
        print(f"\nClearing cache for {browser}...")
        try:
            shutil.rmtree(path)
            print("Cache cleared.")
        except Exception as e:
            print(f"Failed to clear cache: {e}")
    input("\nPress Enter to return to browser menu...")

def update_browser(browser):
    print(f"\nUpdating {browser} via Winget...")
    pkg_ids = {'Chrome': 'Google.Chrome', 'Edge': 'Microsoft.Edge', 'Firefox': 'Mozilla.Firefox'}
    pkg = pkg_ids.get(browser)
    if pkg:
        subprocess.run(["winget", "upgrade", "--id", pkg, "--exact", "--source", "winget"])
    else:
        print("Unknown browser for update.")
    input("\nPress Enter to return to browser menu...")

def browser_submenu():
    while True:
        print("\nBrowser Operations:")
        print("1) Update Browser")
        print("2) Clear Browser Cache")
        print("3) Back to Main Menu")
        choice = input("Select an option: ")
        if choice == '3':
            break
        if choice not in ('1', '2'):
            print("Invalid choice, try again.")
            continue
        op = update_browser if choice == '1' else flush_browser_cache
        browsers = ['Chrome', 'Edge', 'Firefox']
        print("\nSelect browser:")
        for i, b in enumerate(browsers, 1): print(f"{i}) {b}")
        bchoice = input("Browser: ")
        try:
            browser = browsers[int(bchoice) - 1]
            op(browser)
        except:
            print("Invalid browser selection.")
            input("\nPress Enter to return to browser menu...")

# ----- Maintenance (all-in-one) -----
def maintenance():
    clear_dns()
    clear_proxy()
    flash_ip()
    # Toggle off then on
    subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "off"])
    subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "on"])
    print("\nFirewall toggled off and on.")
    delete_hosts()
    reset_network()
    print("\nMaintenance complete.")

    print("\nWould you like to restart the computer now?")
    print("1) Restart now")
    print("2) Restart later")
    restart_choice = input("Select an option: ")
    if restart_choice == '1':
        subprocess.run(["shutdown", "/r", "/t", "0"])

    input("\nPress Enter to return to main menu...")

# ----- Main -----
def main():
    if not is_admin():
        print("Need admin privileges, relaunching as admin...")
        run_as_admin()

    # Options: label, function, persistent?
    options = [
        ("Clear DNS settings", clear_dns, False),
        ("Disable Proxy", clear_proxy, False),
        ("Flash IP (Release/Renew)", flash_ip, False),
        ("Firewall Operations", firewall_menu, False),
        ("Delete Hosts File", delete_hosts, False),
        ("Reset Network", reset_network, False),
        ("Browser Operations", browser_submenu, False),
        ("System Maintenance (all-in-one)", maintenance, True)
    ]

    while True:
        print("\nMain Menu:")
        for i, (label, _, _) in enumerate(options, 1):
            print(f"{i}) {label}")
        print(f"{len(options) + 1}) Exit")

        choice = input("Select an option: ")
        try:
            idx = int(choice)
        except ValueError:
            print("Invalid input, enter a number.")
            continue

        if idx == len(options) + 1:
            print("Exiting...")
            break
        if 1 <= idx <= len(options):
            label, func, persistent = options[idx - 1]
            func()
            if not persistent:
                del options[idx - 1]
                print(f"Option '{label}' removed from menu.")
                if not options:
                    print("No more operations. Exiting...")
                    break
        else:
            print("Selection out of range, try again.")

if __name__ == '__main__':
    main()

# NetNinja Toolkit
# Author: https://github.com/arshiakia/NetNinja-Toolkit