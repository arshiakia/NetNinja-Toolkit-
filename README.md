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

This tool offers two ways to use it:

1_ EXE Installer: A convenient and hassle-free executable file. Just run it—no setup or Python needed.

2_ Python Script: For advanced users who prefer flexibility and customization, the full Python script is available.

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

1. Internet 
2. Program 
3. Exit 

Navigate by entering the corresponding number and pressing **Enter**.

---

### Internet Menu

```
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
1. Install Program
2. Update Program
3. Clear Program Cache
4. Uninstall Program
5. Return to Main Menu
Enter your choice:
```

1. **Install Program: Install new software from the available list**
2. **Update Program: Update existing installed programs to the latest version**
3. **Clear Program Cache: Remove temporary files and cache of a selected program**
4. **Uninstall Program: Completely remove a program from your system**



---

### 🧭 Browsers

1. Google Chrome
2. Mozilla Firefox
3. Microsoft Edge
4. Brave
5. Opera

---

### 💻 Programming & Development Tools

1. Visual Studio Code
2. Python
3. Git
4. Node.js
5. Java JDK
6. Android Studio
7. IntelliJ IDEA
8. PyCharm
9. Eclipse IDE
10. Docker Desktop
11. Postman

---

### 🧰 Utilities

1. Notepad++
2. 7-Zip
3. WinRAR
4. FileZilla
5. Adobe Acrobat Reader
6. Paint.NET

---

### 📞 Communication & Productivity

1. Microsoft Teams
2. Skype
3. Zoom
4. Telegram Desktop
5. WhatsApp
6. Discord
7. Steam

---

### 📊 Databases

1. MySQL
2. MongoDB Compass
