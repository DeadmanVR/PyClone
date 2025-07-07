# PyClone

PyClone is a powerful Python wrapper for the popular command-line tool `rclone`. It transforms `rclone` into a fully automated, observable backup system for Windows, providing rich, real-time progress notifications directly to your `Telegram`.

This project was created to solve the challenge of running rclone as a silent background task while still having full visibility into its progress and status. It's designed to be set up once and run reliably in the background via Windows Task Scheduler.

## Table of Contents

* [Key Features](#key-features)

* [Prerequisites](#prerequisites)

* [Installation & Setup](#installation--setup)

* [Configuration](#configuration)

* [Scheduling the Backup](#scheduling-the-backup)

* [Demo](#demo)

* [Usage](#usage)

## Key Features

* **🤖 Fully Automated Syncing:** Schedule your backups to run daily or at any interval using Windows Task Scheduler.

* **📢 Real-time Telegram Notifications:** Receive detailed status messages from a personal Telegram bot, including dynamic progress bars, percentage completion, and final success (✅) or failure (❌) icons for each job.

* **📄 Centralized JSON Configuration:** Easily define all your backup jobs (sources, destinations, and specific exclusions) in a single, human-readable config.json file.

* **🎯 Per-Job Filtering:** Apply unique exclusion rules for each backup job, giving you granular control over what gets synced.

* **🚀 One-Click Setup:** A simple setup.bat script creates the necessary folder structure and Python virtual environment, and installs all dependencies automatically.

* **⚙️ Built for Windows:** Designed from the ground up to integrate seamlessly with Windows environments and the Task Scheduler for robust, set-and-forget operation.

*  **🔰 Beginner Friendly:** Designed for ease of use. The setup script handles all complex installation, so you only need to edit a simple config file to get started.

## Prerequisites

Before you begin, ensure you have the following installed on your Windows machine:

* **Python:** Download and install the latest version from [python.org](http://python.org/downloads/). Important: During installation, make sure to check the box that says **"Add Python to PATH"**.

* **Rclone:** Download the `rclone.exe` file from the [official rclone website](https://rclone.org/downloads/). You will place this file in the C:\rclone directory during the setup.

## Installation & Setup

Installation is handled by a single script.

1. **Download the Project:** Download the [project files](https://github.com/theamanstark/PyClone/releases/latest/) from this GitHub repository and extract its content.

2. **Run the Setup Script:** Right-click the `setup.bat` file and then select `Run as administrator`.

3. **The setup script will automatically:**
   - Create the necessary folder structure (`C:\rclone\` & `C:\rclone\pyclone`).
   - Move the project files to the correct location.
   - Create a Python virtual environment.
   - Install the required `requests` library.
   - Create the `run_pyclone.bat` launcher script.

4. **Place `rclone.exe`:** Place the `rclone.exe` file you downloaded earlier into the main `C:\rclone` folder.

## Configuration

After running the setup script, you need to configure three things: `rclone` itself, your notification settings, and your backup jobs.

1. **Configure Rclone Remotes**
    First, you need to authorize `rclone` to access your cloud accounts.
    1. Open a Command Prompt and run `C:\rclone\rclone.exe config`.
    2. Follow the interactive setup to add your cloud storage providers (e.g., create a remote named `onedrive` for your OneDrive account and `gdrive` for your Google Drive account).

2. **Configure Telegram Notifications**
    1. Create a Telegram Bot by talking to [@BotFather](https://t.me/BotFather) on Telegram and get your **Bot Token**.
    2. Find your **Chat ID** by talking to [@userinfobot](https://t.me/userinfobot).
    3. Open the `C:\rclone\pyclone\notify.py` file in a text editor.
    4. Paste your **Bot Token** and **Chat ID** into the configuration section at the top.

3. **Configure Your Backup Jobs (`config.json`)**

   This is the most important step, where you define exactly what to back up and where it should go. Open the `C:\rclone\pyclone\config.json` file in a text editor like **VS Code** or **Notepad**.

   The file is structured as a dictionary of "backup jobs." Each job has a name (like `"Documents"` or `"V-Drive"`) and contains details about its destination, source (if needed), and any files or folders to exclude.

   **Anatomy of a Backup Job**

   Here is a breakdown of a single job:

   ```json
    "JobName": {
        "destination": "remote:path/to/folder",
        "source": "C:\\path\\to\\local\\folder",
        "excludes": [
            "FolderName/**",
            "*.file_extension"
        ]
    }
   ```

   1. `destination` **(Required)**

      This tells `rclone` where to put the files in your cloud storage.
   
      - ***Format:*** It must be in the format `remote:path`.
      - `remote`: This is the name you gave your cloud storage during the `rclone config` setup (e.g., `onedrive` or `gdrive`).
      - `path`: This is the folder path inside your cloud storage. If the folder doesn't exist, `rclone` will create it automatically.
      - Example: `"destination": "onedrive:My Backups/Documents"` will sync files to the `My Backups/Documents` folder in your OneDrive.

   2. `source`

      This tells `rclone` where to find the files on your local computer.
   
      - **When it's OPTIONAL:** If the job name (e.g., `"Documents"`, `"Pictures"`, `"Downloads"`) exactly matches the name of a standard folder in your user profile like `C:\Users\YourName\Pictures`, you can leave this out. The script will find it automatically.
   
         ```json
         "Pictures": {
             "destination": "onedrive:Pictures",
             "excludes": []
         }
         ```
      
      - **When it's REQUIRED:** You must add a `"source"` key for any non-standard folder or for an entire drive.
   
        ```json
         "V-Drive": {
             "source": "V:",
             "destination": "gdrive:Dev",
             "excludes": []
         },
         "My Games": {
             "source": "D:\\Games\\Saved Games",
             "destination": "onedrive:Game-Saves",
             "excludes": []
         }
        ```
   
        **Note: In JSON files, you must use double backslashes (`\\`) for Windows paths.**

   3. `excludes` **(Optional)**
    
      This is a list of rules to tell `rclone` which files or folders to skip.

      - **To Exclude a Folder and Everything Inside It:** Add the folder name followed by `/**`. This is the most common exclusion rule.

         ```json
           "excludes": [
            "Torrent Downloads/**"
            ]
          ```

      - **To Exclude a Specific File Type:** Use a wildcard `(*)` followed by the file extension. This rule will exclude all files of that type from the backup.

         ```json
           "excludes": [
            "*.tmp",
            "*.log"
            ]
          ```

      - **To Exclude Multiple Items:** Simply add more rules to the list, separated by commas.

         ```json
           "excludes": [
            "Cache/**",
            "Temporary Files/**",
            "*.bak"
            ]
          ```

   4. Complete Example `config.json`:

      Here is a complete example demonstrating all these concepts.

         ```json
       {
           "Documents": {
              "destination": "onedrive:Documents",
              "excludes": []
           },
           "Pictures": {
              "destination": "onedrive:Pictures",
              "excludes": []
           },
           "Downloads": {
              "destination": "onedrive:Downloads",
              "excludes": [
                "Torrent Downloads/**"
              ]
           },
           "V-Drive": {
              "source": "V:",
              "destination": "gdrive:Dev",
              "excludes": [
                "System Volume Information/**",
                "$RECYCLE.BIN/**"
              ]
           }
       }
       ```

      **Each backup job supports multiple exclusion to control what files/folders are synced.**

## Scheduling the Backup

To make the backup run automatically, use **Windows Task Scheduler**.

1. Open **Task Scheduler**.

2. Click **Create Basic Task**... in the **Actions pane**.

3. **Name:** Give it a name like **"PyClone Backup"**.

4. **Trigger:** Choose how often you want the backup to run (e.g., Daily).

5. **Action:** Select **Start a program**.

6. **Configure the Action:**

   * **Program/script**: `"C:\rclone\pyclone\run_pyclone.bat"`
   * **Add arguments (optional)**: (Leave this blank)
   * **Start in (optional)**: (Leave this blank)

7. **Final Settings:** On the last screen, check the box for "Open the Properties dialog for this task when I click Finish."

8. In the **Properties** window:

   * On the **General** tab, select **"Run whether user is logged on or not"**. You will be prompted for your Microsoft Account password using which your current Windows profile was created. (This step is important to always run the backup script in the background without being shown a terminal window.)
   * On the **Conditions** tab, uncheck **"Start the task only if the computer is on AC power"** if you want it to run on a laptop's battery.

## Demo 

![PyClone Demo](https://theamanstark.com/cdn/assets/PyClone/demo.gif)

## Usage

Once scheduled, the script will run automatically. You don't need to do anything. You will receive a message on Telegram when a backup starts, see real-time progress for each job, and get a final status message upon completion. If any errors occur, the script will send you the log file for easy diagnosis.
