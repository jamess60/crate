import datetime
import time
import shutil
import os
import zipfile
import socket
import subprocess
import paramiko
import pwd
import re
from functions import script





def create_hostname_subdirs(HOSTS, DEST_DIR, RUN_MODE):
    # Check if $DESTDIR/hostname exists for localhost, create it if not
    if RUN_MODE == "backup-local" or RUN_MODE == "bl": 
        hostname = socket.gethostname()
        script.info_msg("Checking/creating sub directories for localhost...")
        sub_dir_path = os.path.join(DEST_DIR, str(hostname))
        
        if not os.path.exists(sub_dir_path):
            os.mkdir(sub_dir_path)
            script.ok_msg("Sub directory " + hostname + " created in " + DEST_DIR + ".")
        else:
            script.ok_msg("Sub directory " + hostname + " already exists in " + DEST_DIR + ".")


    # Check if $DESTDIR/hostname exists for each remote host, create them if not
    if RUN_MODE == "backup-remote" or RUN_MODE == "br":
        script.info_msg("Checking/creating sub directories for each host...")
        for host in HOSTS:
            sub_dir_path = os.path.join(DEST_DIR, host)
            
            if not os.path.exists(sub_dir_path):
                os.mkdir(sub_dir_path)
                script.ok_msg("Sub directory " + host + " created in " + DEST_DIR + ".")
            else:
                script.ok_msg("Sub directory " + host + " already exists in " + DEST_DIR + ".")





def perform_backup_local(SOURCE_DIR, DEST_DIR):
    datetime_str = datetime.datetime.now().strftime('%Y-%m-%d---%H-%M-%S')
    hostname = socket.gethostname()
    print("\n\n")
    script.info_msg("Starting local backup task. Timestamp: " + str(datetime_str))
    
    # Create backup
    backup_file_path = DEST_DIR + "/" + str(hostname) + "/" + datetime_str
    script.info_msg("Creating backup file: " + str(backup_file_path) + ".zip")
    shutil.make_archive(backup_file_path, 'zip', SOURCE_DIR)
        
    # Test file by extracting first file to null
    print("\n\n")
    script.info_msg("Running archive validity check...")
    os.system("mkdir -p /tmp/crate-scratch")
    validate_me = backup_file_path + ".zip"        
    script.info_msg("Testing file validity for: " + str(validate_me))
    try:
        archive = 'good'
        with zipfile.ZipFile(validate_me, 'r') as zip_ref:
            first_file = zip_ref.namelist()[0]
            zip_ref.extract(first_file, '/tmp/crate-scratch')
    except zipfile.BadZipFile:
        archive = "bad"
        script.warn_msg("The backup archive is potentially corrupt: " + validate_me)
    if archive == 'good':
        script.ok_msg("Backup archive passed validation check.")
        os.system("rm -rf /tmp/crate-scratch")
        script.ok_msg("Backup task complete!\n\n")
    else:
        script.err_msg("Backup archive FAILED validation check.")

    # This is the path of the created backup archive, returned so offsite def can use it
    return validate_me 






def perform_recovery_local(RECOVERY_ZIP, SOURCE_DIR, SKIP_RM):
    script.info_msg("Starting local recovery task...")


    if SKIP_RM is not True:
        try:
            shutil.rmtree(SOURCE_DIR)
            print(script.ok_msg("Source dir removed successfully."))

        except Exception as e:
            script.err_msg("Unable to remove Source Dir - An error occurred: " + str(e))
            print("Remove and recreate the source directory as root and retry. Use -srm to skip this step in the next run.\n\n")
            exit()


    try:
        with zipfile.ZipFile(RECOVERY_ZIP, 'r') as zip_ref:
            zip_ref.extractall(SOURCE_DIR)
            status = "ok"
        
    except zipfile.BadZipFile:
        script.err_msg("Invalid zip file.")
        status = "badzip"

    except Exception as e:
        script.err_msg("An error occurred: " + e)
        status = "error"

    return status





def copy_to_offsite_dir(zip_to_offsite, OFFSITE_PATH, HOSTS): 

# Check if the ZIP file exists
    if not os.path.isfile(zip_to_offsite):
        script.err_msg(f"The file {zip_to_offsite} does not exist.")
        return
    
    # Check if the destination path is a directory
    if not os.path.isdir(OFFSITE_PATH):
        script.warn_msg(f"The destination path {OFFSITE_PATH} is not a directory. Attempting to create it...")
        return

    # Construct the subdirectory path using the hostname
    hostname_path = os.path.join(OFFSITE_PATH, HOSTS)
    
    # Create the directory if it does not exist
    if not os.path.exists(hostname_path):
        try:
            os.makedirs(hostname_path)
        except PermissionError as e:
            script.err_msg(f"Permission error while creating directory {hostname_path}: {e}")
            return
        except Exception as e:
            script.err_msg(f"An error occurred while creating directory {hostname_path}: {e}")
            return
    
    # Construct the destination path for the copied file
    filename = os.path.basename(zip_to_offsite)
    destination = os.path.join(hostname_path, filename)
    
    try:
        # Copy the file to the destination directory
        shutil.copy(zip_to_offsite, destination)
        script.ok_msg(f"Successfully copied {zip_to_offsite} to {destination}.")
    except PermissionError as e:
        script.err_msg(f"Permission error: {e}")
    except Exception as e:
        script.err_msg(f"An error occurred: {e}")








def sanity_check_permission_config(CONTAINER_USER, PERMISSION):
    script.info_msg("Sanity checking user and permission configuration")

    # Check if the user exists
    try:
        pwd.getpwnam(CONTAINER_USER)
        script.ok_msg("CONTAINER_USER (" + CONTAINER_USER + ") exists.")
    except KeyError:
        script.err_msg("CONTAINER_USER does not exist on system. Please check configuration for typos or run again without fix permissions.")
        return False
    
    # Check if the chmod permission is valid
    if re.match(r'^[0-7]{3}$', str(PERMISSION)):
        script.ok_msg("chmod value (" + str(PERMISSION) + ") is valid.")
    else:
        script.err_msg("PERMISSION is invalid. Must be a 3-digit number with each digit between 0 and 7")
        return False

    return True




def fix_recovery_permissions(SOURCE_DIR, CONTAINER_USER, PERMISSION):
    script.info_msg("Attempting to fix permissions on recovered files...")
    
    # Check if script is running as root
    if os.geteuid() != 0:
        script.err_msg("Arg -fp selected but script is not running as root. Exiting...")
        exit()
    else:
        print(script.ok_msg("Script has root perms."))
        # Get UID and PID of container user
        uid = int(os.popen("id -u netadmin").read().strip())
        gid = int(os.popen("id -g netadmin").read().strip())

        # Change ownership of the directory
        try:
            os.chown(SOURCE_DIR, uid, gid)
            script.ok_msg("Source dir ownership changed successfully.")
        except OSError as e:
            # print(f"Error: {e}")
            print(script.err_msg(e))


        # Change perms of the directory
        try:
            # os.chmod(SOURCE_DIR, PERMISSION)# <--- Doesn't work with var, requires 0o prefix and gets caught up on str/int inputs
            permcmd = "chmod -R 777 " + SOURCE_DIR
            os.system(permcmd)
            script.ok_msg("Source dir permissions changed successfully.")
        except OSError as e:
            # print(f"Error: {e}")
            print(script.err_msg(e))





