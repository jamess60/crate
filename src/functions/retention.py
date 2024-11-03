import datetime
import os
import pysftp
from functions import script



def localhost_basic_retention(DEST_DIR, LOCAL_RETENTION_PERIOD_DAYS):
    today = datetime.datetime.now()
    retention_delta = datetime.timedelta(days=LOCAL_RETENTION_PERIOD_DAYS)

    delete_errors = []    
    hostname = os.uname().nodename
    
    server_path = os.path.join(DEST_DIR, hostname)

    if os.path.isdir(server_path):
        for backup_file in os.listdir(server_path):
            backup_file_path = os.path.join(server_path, backup_file)
            
            if os.path.isfile(backup_file_path) and backup_file.endswith('.zip'):
                timestamp_str = backup_file.split('.')[0]
                backup_timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d---%H-%M-%S')

                entered_deletion_loop = False

                if today - backup_timestamp > retention_delta:
                    entered_deletion_loop = True
                    try:
                        os.remove(backup_file_path)
                        script.ok_msg("Deleted " + backup_file_path + " as per retention policy.")
                    except:
                        script.err_msg("Error deleting " + backup_file_path + " as per retention policy.")
                        delete_errors.append(backup_file_path)
            
                    # If the hostname subdir is empty after deleting the backup(s), bin it too
                    if not os.listdir(server_path):
                        os.rmdir(server_path)

        if entered_deletion_loop == False:
            script.ok_msg("Destination does not contain any backup files older than the retention period.")

    if delete_errors:
        print("RETENTION DEBUG - " + str(delete_errors))

    script.ok_msg("Retention cleanup complete\n\n")




def sftp_basic_retention(HOSTS, SFTP_USER, SFTP_PASS, SFTP_HOST, SFTP_PATH, OFFSITE_RETENTION_PERIOD_DAYS):
    # Combine the SFTP path with the HOSTS variable to form the full path
    directory_path = os.path.join(SFTP_PATH, HOSTS)

    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=OFFSITE_RETENTION_PERIOD_DAYS)
    
    # SFTP connection options to disable host key checking
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key checking for automation

    # Establish connection to the SFTP server
    with pysftp.Connection(SFTP_HOST, username=SFTP_USER, password=SFTP_PASS, cnopts=cnopts) as sftp:
        
        # Change to the desired directory
        try:
            sftp.cwd(directory_path)
            
            # List files in the directory
            for file in sftp.listdir():
                # Check if file is a .zip file and has a timestamp in the name
                if file.endswith('.zip'):
                    try:
                        # Extract timestamp from filename
                        timestamp_str = file.split('.')[0]
                        file_timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d---%H-%M-%S')
                        
                        # If the file timestamp is older than the cutoff date, delete it
                        if file_timestamp < cutoff_date:
                            sftp.remove(file)
                            print(f"Deleted file: {file} (Timestamp: {file_timestamp})")
                    except ValueError:
                        # Skip files that don't match the timestamp format
                        print(f"Skipping file (timestamp format not matched): {file}")
                        
        except FileNotFoundError:
            print(f"Directory {directory_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        script.ok_msg("Retention cleanup complete\n\n")



