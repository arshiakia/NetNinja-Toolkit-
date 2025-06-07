````markdown
# Windows Admin Utility Script

A Python-based command-line utility for performing common network and system maintenance tasks on Windows. This script offers two main menus—**Internet** and **Program**—and executes various actions under elevated (Administrator) privileges. It’s designed to simplify tasks such as resetting DNS, clearing cache, installing/updating/removing applications via `winget`, and more.

---

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation & Setup](#installation--setup)  
- [Usage](#usage)  
  - [Launching with Administrator Privileges](#launching-with-administrator-privileges)  
  - [Main Menu Overview](#main-menu-overview)  
  - [Internet Menu](#internet-menu)  
  - [Program Menu](#program-menu)  
- [Supported Applications (Program Menu)](#supported-applications-program-menu)  
- [Error Handling & Execution Policy](#error-handling--execution-policy)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

1. **Administrator Elevation**  
   - Automatically requests UAC elevation if run without Administrator privileges.  
2. **Internet Menu**  
   - Reset all DNS adapters to DHCP.  
   - Clear system proxy settings.  
   - Release/renew IP address and flush DNS cache.  
   - Disable Windows Firewall for all profiles.  
   - Reset the `hosts` file to default.  
   - Clear browser cache (Chrome, Firefox, Edge, Brave, Opera) after selecting the desired browser.  
   - “Perform All” option to run all internet-related tasks sequentially, then prompt for a reboot.  
3. **Program Menu**  
   - Install popular applications via `winget` (browsers, programming tools, essential utilities).  
   - Update installed applications using `winget upgrade`.  
   - Clear cache directories for selected programs.  
   - Uninstall applications via `winget uninstall`.  
   - Supports a broad list of software—see [Supported Applications](#supported-applications-program-menu).  
4. **User-Friendly Console Interface**  
   - Clear screen between menus and operations for readability.  
   - Simple numbered prompts with “Back” options to navigate.  
   - ASCII banner (`arshiakia`) displayed at startup.  
5. **Automated User Paths**  
   - Detects the current Windows user automatically (via `os.environ["USERPROFILE"]`).  
   - Builds cache paths, profile paths, and hosts file location dynamically—no manual editing required.

---

## Prerequisites

- **Operating System**: Windows 10 or later (Windows 11 tested).  
- **Python Version**:  
  - Python 3.6+ installed and available in `PATH`.  
  - Ensure the `python` command is recognized in PowerShell/Command Prompt.

- **Dependencies**: No external Python packages are required.  
  All functionality is implemented using standard library modules (`os`, `sys`, `subprocess`, `ctypes`, `shutil`, `time`).

- **Winget**:  
  - Windows Package Manager (`winget`) must be installed and accessible in `PATH` for Program Menu actions.  
  - If `winget` is unavailable, the script will skip “Install,” “Update,” and “Uninstall” actions with a warning message.

---

## Installation & Setup

1. **Clone or Download Repository**  
   ```bash
   git clone https://github.com/<YourUsername>/windows-admin-utility.git
   cd windows-admin-utility
````

2. **Verify Python Installation**

   ```powershell
   python --version
   ```

3. **Ensure Winget is Installed** (optional, for Program menu)

   ```powershell
   winget --version
   ```

   * If not installed, download the App Installer from the Microsoft Store or install via [winget GitHub releases](https://github.com/microsoft/winget-cli).

4. **(Optional) Unblock Script Execution**
   If your system’s PowerShell execution policy blocks running scripts, you can unblock this file:

   ```powershell
   Unblock-File .\admin_utility.py
   ```

   > **Note:** The script bypasses execution policy when using PowerShell commands internally, so you should not encounter execution policy errors during DNS operations.

---

## Usage

### Launching with Administrator Privileges

1. Open **Command Prompt** or **PowerShell** *as Administrator*.
2. Navigate to the directory containing `admin_utility.py`.
3. Run:

   ```powershell
   python admin_utility.py
   ```

   * If you run it without administrative rights, the script will prompt for elevation and relaunch itself with UAC.

---

### Main Menu Overview

Upon successful elevation, you will see a banner and the main menu:

```
+------------------+
|    arshiakia     |
+------------------+

=== Main Menu ===
1. Internet
2. Program
3. Exit
Enter your choice:
```

* **1. Internet** → Opens the Internet Menu.
* **2. Program** → Opens the Program Menu.
* **3. Exit** → Terminates the script.

Navigate by entering the corresponding number and pressing **Enter**.

---

### Internet Menu

```
=== Internet Menu ===
1. Delete all DNS settings
2. Delete proxy settings
3. Flush IP (release, renew, flushdns)
4. Disable Windows Firewall
5. Clear hosts file
6. Perform all of the above
7. Clear browser cache
8. Return to Main Menu
Enter your choice:
```

1. **Delete all DNS settings**

   * Resets DNS server to DHCP for every active network adapter. Internally runs PowerShell with `-NoProfile -ExecutionPolicy Bypass`.
   * Example PowerShell command:

     ```powershell
     Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} |
       ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ResetServerAddresses }
     ```

2. **Delete proxy settings**

   * Runs `netsh winhttp reset proxy` and removes `ProxyEnable`/`ProxyServer` registry values under `HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings`.

3. **Flush IP (release, renew, flushdns)**

   * `ipconfig /release` → `ipconfig /renew` → `ipconfig /flushdns`.
   * Pauses 2 seconds between each command for stability.

4. **Disable Windows Firewall**

   * Runs `netsh advfirewall set allprofiles state off`.

5. **Clear hosts file**

   * Overwrites `%WINDIR%\System32\drivers\etc\hosts` with default loopback entries:

     ```
     127.0.0.1    localhost
     ::1          localhost
     ```

6. **Perform all of the above**

   * Executes (1) through (5) in sequence.
   * After completion, prompts:

     ```
     Do you want to reboot now? (y/n):
     ```

     * `y` → `shutdown /r /t 0` (immediate reboot).
     * `n` → Return to Internet Menu.

7. **Clear browser cache**

   * Displays:

     ```
     1. Google Chrome
     2. Mozilla Firefox
     3. Microsoft Edge
     4. Brave
     5. Opera
     6. Back to Internet Menu
     ```
   * Automatically detects `%USERPROFILE%` and deletes the chosen browser’s cache folder:

     * Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache`
     * Firefox: `%LOCALAPPDATA%\Mozilla\Firefox\Profiles\<Profile>\cache2` (clears all profile cache2 folders)
     * Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache`
     * Brave: `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cache`
     * Opera: `%LOCALAPPDATA%\Opera Software\Opera Stable\Cache`

8. **Return to Main Menu**

   * Goes back to the Main Menu screen.

---

### Program Menu

```
=== Program Menu ===
1. Install Program
2. Update Program
3. Clear Program Cache
4. Uninstall Program
5. Return to Main Menu
Enter your choice:
```

1. **Install Program**

   * Checks if `winget` exists.
   * Displays categories:

     ```
     1. Browsers
     2. Programming Software
     3. Essential Tools
     4. Back to Program Menu
     ```
   * **Browsers** (example list):

     ```
     1. Google Chrome            (winget ID: Google.Chrome)
     2. Mozilla Firefox          (winget ID: Mozilla.Firefox)
     3. Microsoft Edge           (winget ID: Microsoft.Edge)
     4. Brave                    (winget ID: BraveSoftware.BraveBrowser)
     5. Opera                    (winget ID: Opera.Opera)
     6. Tor Browser              (winget ID: TorBrowser.TorBrowser)
     7. Back
     ```
   * **Programming Software** (example list):

     ```
     1. Python 3                 (winget ID: Python.Python.3)
     2. Git                      (winget ID: Git.Git)
     3. Visual Studio Code       (winget ID: Microsoft.VisualStudioCode)
     4. Node.js                  (winget ID: OpenJS.NodeJS)
     5. Java JDK                 (winget ID: Oracle.JavaRuntimeEnvironment)
     6. IntelliJ IDEA Community  (winget ID: JetBrains.IntelliJIDEA.Community)
     7. PowerShell               (winget ID: Microsoft.PowerShell)
     8. Go                       (winget ID: GoLang.Go)
     9. Rust                     (winget ID: RustLang.Rust)
     10. Back
     ```
   * **Essential Tools** (example list):

     ```
     1. 7-Zip                    (winget ID: 7zip.7zip)
     2. VLC Media Player         (winget ID: VideoLAN.VLC)
     3. Notepad++                (winget ID: Notepad++.Notepad++)
     4. WinRAR                   (winget ID: RARLab.WinRAR)
     5. Spotify                  (winget ID: Spotify.Spotify)
     6. Zoom                     (winget ID: Zoom.Zoom)
     7. Docker Desktop           (winget ID: Docker.DockerDesktop)
     8. Postman                  (winget ID: Postman.Postman)
     9. Discord                  (winget ID: Discord.Discord)
     10. Back
     ```
   * After selection, runs:

     ```bash
     winget install --id <PACKAGE_ID> --silent
     ```

2. **Update Program**

   * Checks if `winget` exists.
   * Displays a combined list of all supported applications (same IDs as above).
   * After selection, runs:

     ```bash
     winget upgrade --id <PACKAGE_ID> --silent
     ```

3. **Clear Program Cache**

   * Displays a list of applications with known cache paths:

     ```
     1. Python        → %LOCALAPPDATA%\pip\Cache
     2. Git           → (No standard path; skipped)
     3. Visual Studio Code → %APPDATA%\Code\Cache
     4. Node.js       → (npm cache can be cleared manually)
     5. Java JDK      → (No standard path; skipped)
     6. 7-Zip         → (No standard path; skipped)
     7. VLC Media Player → (No standard path; skipped)
     8. Notepad++     → %APPDATA%\Notepad++\cache
     9. WinRAR        → (No standard path; skipped)
     10. Spotify      → (No standard path; skipped)
     11. Zoom         → (No standard path; skipped)
     12. Docker Desktop → (No standard path; skipped)
     13. Postman      → (No standard path; skipped)
     14. Discord      → (No standard path; skipped)
     15. Back
     ```
   * If a valid cache folder exists, it will be deleted. Otherwise, a warning is shown.

4. **Uninstall Program**

   * Checks if `winget` exists.
   * Displays the same list as in “Update Program.”
   * After confirming, runs:

     ```bash
     winget uninstall --id <PACKAGE_ID> --silent
     ```

5. **Return to Main Menu**

   * Goes back to the Main Menu screen.

---

## Supported Applications (Program Menu)

Below is a consolidated list of application IDs used by `winget` in this script. If you want to add or modify entries, search the official [Windows Package Manager repository](https://github.com/microsoft/winget-pkgs) for the exact `Id`.

* **Browsers**

  * `Google.Chrome` (Google Chrome)
  * `Mozilla.Firefox` (Mozilla Firefox)
  * `Microsoft.Edge` (Microsoft Edge)
  * `BraveSoftware.BraveBrowser` (Brave)
  * `Opera.Opera` (Opera)
  * `TorBrowser.TorBrowser` (Tor Browser)

* **Programming Software**

  * `Python.Python.3` (Python 3)
  * `Git.Git` (Git for Windows)
  * `Microsoft.VisualStudioCode` (Visual Studio Code)
  * `OpenJS.NodeJS` (Node.js)
  * `Oracle.JavaRuntimeEnvironment` (Java JDK)
  * `JetBrains.IntelliJIDEA.Community` (IntelliJ IDEA Community)
  * `Microsoft.PowerShell` (PowerShell)
  * `GoLang.Go` (Go)
  * `RustLang.Rust` (Rust)

* **Essential Tools**

  * `7zip.7zip` (7-Zip)
  * `VideoLAN.VLC` (VLC Media Player)
  * `Notepad++.Notepad++` (Notepad++)
  * `RARLab.WinRAR` (WinRAR)
  * `Spotify.Spotify` (Spotify)
  * `Zoom.Zoom` (Zoom)
  * `Docker.DockerDesktop` (Docker Desktop)
  * `Postman.Postman` (Postman)
  * `Discord.Discord` (Discord)

---

## Error Handling & Execution Policy

* **PowerShell “Scripts Disabled” Error**
  When resetting DNS, if you see:

  ```
  File C:\Users\<User>\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 cannot be loaded 
  because running scripts is disabled on this system.
  ```

  The script is already configured to call PowerShell with `-NoProfile -ExecutionPolicy Bypass`, which prevents loading your personal profile and ignores the system’s execution policy. No additional change is usually required.

* **Winget Not Found**
  If `winget` is not installed or not in `PATH`, install it via the Microsoft Store (App Installer) or download from [GitHub Releases](https://github.com/microsoft/winget-cli/releases). The script will detect its absence and skip “Install,” “Update,” and “Uninstall” operations.

---

## Contributing

1. Fork this repository on GitHub.
2. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature/my-feature
   ```
3. Make your changes and commit them with clear messages.
4. Push your branch and open a Pull Request.
5. Ensure your code follows the existing style and thoroughly test new additions—especially PowerShell commands or `winget` IDs.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute as you see fit.

---

```
```
