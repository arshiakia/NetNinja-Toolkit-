# Windows Admin Utility Script


## Features

1. **Internet Menu**  
   - Reset all DNS adapters to DHCP.  
   - Clear system proxy settings.  
   - Release/renew IP address and flush DNS cache.  
   - Disable Windows Firewall for all profiles.  
   - Reset the `hosts` file to default.  
   - Clear browser cache (Chrome, Firefox, Edge, Brave, Opera) .  
   - “Perform All” option to run all internet-related tasks sequentially .
  
2. **Program Menu**  
   - Install popular applications via `winget` (browsers, programming tools, essential utilities).  
   - Update installed applications using `winget upgrade`.  
   - Clear cache directories for selected programs.  
   - Uninstall applications via `winget uninstall`.
   - Supports a broad list of software—see [Supported Applications (Program Menu)](https://learn.microsoft.com/en-us/windows/package-manager/winget/list)

---

## Prerequisites

   - Windows 10 or later
   - Python 3.6+ installed and added to your system’s PATH
   - Winget (Windows Package Manager) installed for installing/updating/uninstalling programs
   - No extra Python packages needed — everything uses the standard library
   - Run the script as Administrator for full functionality

---

## Installation & Setup

1. **Clone or Download Repository**  
```
git clone https://github.com/arshiakia/NetNinja-Toolkit-.git
```
```
cd C:\Users\----\NetNinja-Toolkit-
```

2. **Verify Python Installation**

```
python --version
```

3. **Ensure Winget is Installed** (optional, for Program menu)

```
winget --version
```

## Usage

### Launching with Administrator Privileges
Choose the description style you prefer:

Simple:
You can run the Python script or use the standalone EXE file. Just double-click the EXE—no need for Python installation. Both versions have the same features.

Detailed & Engaging:
For your convenience, this tool is also available as a standalone EXE application. No need to install Python or any dependencies—just download, double-click, and you’re ready to go! The EXE version offers the full functionality of the Python script wrapped in an easy-to-use executable, perfect for users who want a hassle-free setup.
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

* 1. Internet** → Opens the Internet Menu.
* 2. Program** → Opens the Program Menu.
* 3. Exit** → Terminates the script.

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
2. **Delete proxy settings**
3. **Flush IP (release, renew, flushdns)**
4. **Disable Windows Firewall**
5. **Clear hosts file**
6. **Perform all of the above**
7. **Clear browser cache**
8. **Return to Main Menu**

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


2. **Update Program**

   * Checks if `winget` exists.
   * Displays a combined list of all supported applications (same IDs as above).

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
