import json
import subprocess
import os
import re
import time
import datetime
import notify as nt
import utils as ut

# --- SCRIPT SETUP ---
pyclone_dir = os.path.dirname(os.path.realpath(__file__)) # This is C:\rclone\pyclone
rclone_dir = os.path.dirname(pyclone_dir) # This is C:\rclone

config_path = os.path.join(pyclone_dir, 'config.json') # Path of config.json file located inside the pyclone directory
rclone_exe = os.path.join(rclone_dir, 'rclone.exe') # Correctly finds C:\rclone\rclone.exe
log_file = os.path.join(pyclone_dir, 'rclone_log.txt') # Path of rclone_log.txt file located inside the pyclone directory
message_id_file = os.path.join(pyclone_dir, 'last_message_id.txt') # Path of last_message_id.txt file located inside the pyclone directory

# --- MAIN SCRIPT LOGIC ---
def main():
    # 1. Clean up the message from the previous run
    last_message_id = ut.load(message_id_file)
    if last_message_id:
        nt.delete(last_message_id)
        
    # 2. Clean up the log file from the previous run
    if os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as log:
            log.write("")

    # 3. Load rclone configuration
    with open(config_path, 'r') as f:
        config = json.load(f)

    # 4. Prepare initial status and send the first message
    job_statuses = {job_name: "Pending..." for job_name in config.keys()}

    initial_message = ut.formats(job_statuses) # Prepare the initial message with job statuses
    message_id = nt.send(initial_message) # Send the initial message to Telegram and get the message ID
    if not message_id:
        print("Could not get message_id from Telegram. Aborting.")
        return
    ut.save(message_id, message_id_file) # Save new ID immediately

    # 5. Define common rclone flags, including performance optimizations
    common_flags = [
        '-v', '-L', '--fast-list', '--progress',
        '--checkers=20', '--transfers=20',  # Performance flags
        '--delete-excluded', '--exclude=desktop.ini', '--exclude=Thumbs.db'
    ]
    
    # Initialize overall success status
    overall_success = True

    # 6. Open log file and loop through each backup job
    with open(log_file, 'a', encoding='utf-8') as log:
        for job_name, details in config.items():
            print(f"Syncing {job_name}...")
            
            # Get source and destination paths from the config, defaulting to user profile if not specified
            source_path = details.get('source', os.path.join(os.environ['USERPROFILE'], job_name))
            destination_path = details['destination']
            
            # Prepare the rclone command with the specified source and destination along with common flags
            command = [rclone_exe, 'sync', source_path, destination_path] + common_flags
            
            # Add any additional flags specified in the config
            for exclude_pattern in details.get('excludes', []):
                command.append(f'--exclude={exclude_pattern}')
            
            last_update_time = 0 # Track the last time we updated the job status
            last_percentage = 0 # Reset for each job
            
            # Using Popen to run rclone and capture output in real-time
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')

            # Read output in real-time and line-by-line
            for line in iter(process.stdout.readline, ''):
                log.write(line) # Write to log file
                log.flush() # Ensure log is written in real-time
                
                # Check if the line contains progress information
                match = re.search(r'Transferred:\s+.*,\s+(\d+)%', line)
                if match:
                    percentage = int(match.group(1))
                    last_percentage = percentage # Store the most recent percentage
                    
                    # Throttle updates to avoid hitting Telegram's rate limits
                    if time.time() - last_update_time > 2:
                        job_statuses[job_name] = ut.progress(percentage)
                        nt.edit(message_id, ut.formats(job_statuses))
                        last_update_time = time.time()
            
            # Wait for the process to finish and get the exit code
            process.wait()
            
            # Update the final status based on the exit code
            if process.returncode in [0, 9]: # Treat code 9 (success with non-critical errors) as a success
                # If no progress was reported (e.g., no files transferred), show 100%
                display_percentage = 100 if last_percentage == 0 else last_percentage
                job_statuses[job_name] = ut.progress(display_percentage) + " ✅"
            else:
                # On failure, show the last percentage before it failed
                job_statuses[job_name] = ut.progress(last_percentage) + f" ❌ (Code: {process.returncode})"
                overall_success = False
            
            # Update the message with the latest job status
            nt.edit(message_id, ut.formats(job_statuses))
    
    # Final "finished" message
    final_status = "Finished" if overall_success else "Finished with Errors"
    final_text = ut.formats(job_statuses, status_text=final_status)
    nt.edit(message_id, final_text)
    
    # 7. If there were errors, send the log file as a reply
    if not overall_success:
        print("An error occurred. Sending log file to Telegram...")
        now = datetime.datetime.now().strftime('%c')
        caption_text = f"This is the error log file for the backup run at {now}."
        nt.file(log_file, caption=caption_text)
        
    # 8. Last print statement to indicate the script has finished
    print(f"Backup script {final_status}.")

if __name__ == "__main__":
    main()
