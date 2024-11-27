#!/usr/bin/python3

__author__ = "james_s60"
__date__ = "27 Nov 2024"
__credits__ = ["james_s60"]
__version__ = "1.2"



############################
# Imports
############################
import argparse
import ast
import os
import socket
from configparser import ConfigParser 
from colorama import Fore, Back, Style  
##
from functions import container
from functions import file
from functions import retention
from functions import rwcheck
from functions import script
from functions import sftp
from functions import ntfy


config = ConfigParser()
config.read('/usr/share/crate/conf/config.ini')
############################


script.rainbow("\n \
   _____ _____         _______ ______\n \
  / ____|  __ \     /\|__   __|  ____|\n \
 | |    | |__) |   /  \  | |  | |__   \n \
 | |    |  _  /   / /\ \ | |  |  __|  \n \
 | |____| | \ \  / ____ \| |  | |____ \n\
  \_____|_|  \_\/_/    \_\_|  |______|\n \
Container Recovery and Archival ToolsEt \n\n")
print(Style.RESET_ALL)


############################
# Parse CLI Args
############################
parser = argparse.ArgumentParser(description='CRATE. Container Recovery and Archival ToolsEt.')
parser.add_argument('-z','--zip', dest='arg_zip', type=str, help='Full path to the zip file to recover')
parser.add_argument('-m','--mode', dest='arg_mode', type=str, help='Which mode the script should run in [bl,rl] or [backup-local, recover-local]')
parser.add_argument('-srm','--skip-rm', dest='arg_skiprm', action='store_true', help='Skips removing source dir during restore task if it was recreated manually and this is a retry attempt.')
parser.add_argument('-fp','--fix-perms', dest='arg_fixperms', action='store_true', help='Sets ownership and permissions on recovered data (script must run as root)')

arguments = parser.parse_args()
RECOVERY_ZIP = arguments.arg_zip
RUN_MODE = arguments.arg_mode
SKIP_RM = arguments.arg_skiprm
FIX_PERMS = arguments.arg_fixperms

# Patch job - host pulled from config ini before remote modes deprecated
HOSTS = str(socket.gethostname()) 
RECOVERY_HOST  = str(socket.gethostname())
############################



############################
# Parse Config
############################
# Main
SOURCE_DIR = config['MAIN']['SOURCE_DIR']
DEST_DIR = config['MAIN']['DEST_DIR']
# Offiste Backup
OFFSITE_BACKUP_ENABLED = config['OFFSITE'].getboolean('OFFSITE_BACKUP_ENABLED')
OFFSITE_BACKUP_MODE = config['OFFSITE']['OFFSITE_BACKUP_MODE']
LOCAL_OFFSITE_BACKUP_DIR = config['OFFSITE']['LOCAL_OFFSITE_BACKUP_DIR']
SFTP_USER = config['OFFSITE']['SFTP_USER']
SFTP_PASS = config['OFFSITE']['SFTP_PASS']
SFTP_HOST = config['OFFSITE']['SFTP_HOST']
SFTP_PATH = config['OFFSITE']['SFTP_PATH']
# Permissions
CONTAINER_USER = config['PERMISSIONS']['CONTAINER_USER']
PERMISSION = int(config['PERMISSIONS']['PERMISSION'])
# Retention
LOCAL_RETENTION_ENABLED = config['RETENTION'].getboolean('LOCAL_RETENTION_ENABLED')
OFFSITE_RETENTION_ENABLED = config['RETENTION'].getboolean('OFFSITE_RETENTION_ENABLED')
LOCAL_RETENTION_PERIOD_DAYS = int(config['RETENTION']['LOCAL_RETENTION_PERIOD_DAYS'])
OFFSITE_RETENTION_PERIOD_DAYS = int(config['RETENTION']['OFFSITE_RETENTION_PERIOD_DAYS'])
# Ntfy
NTFY_ENABLED = config['NTFY'].getboolean('NTFY_ENABLED')
# NTFY_HOST = str(config['NTFY']['NTFY_HOST'])     - This is now parsed directly in src/functions/ntfy.py!
# NTFY_TOPIC = str(config['NTFY']['NTFY_TOPIC'])   - This is now parsed directly in src/functions/ntfy.py!
############################


# ==================================================================================================


# Sanity check arguments
if FIX_PERMS == True and RUN_MODE not in {"recover-local", "rl"}:
    script.err_msg("Fix Permissions argument specificed but CRATE is running in recovery mode. Program will exit.\n\n")
    if NTFY_ENABLED == True:
        ntfy.ntfy_err_FP_wrong_mode_fail()
    exit()
if RUN_MODE == "backup-local" or RUN_MODE == "bl" and RECOVERY_ZIP is not None:
    script.err_msg("Zip file argument specificed but CRATE is running in backup mode. Program will exit.\n\n")
    if NTFY_ENABLED == True:
        ntfy.ntfy_err_ZIP_wrong_mode_fail()
    exit()
if RUN_MODE == "backup-local" or RUN_MODE == "bl" and SKIP_RM is True:
    script.err_msg("SRM argument specificed but CRATE is running in backup mode. Program will exit.\n\n")
    if NTFY_ENABLED == True:
        ntfy.ntfy_err_SRM_wrong_mode_fail()
    exit()
if RUN_MODE == "backup-local" or RUN_MODE == "bl" and FIX_PERMS is True:
    script.err_msg("Fix Permissions argument specificed but CRATE is running in backup mode. Program will exit.\n\n")
    if NTFY_ENABLED == True:
        ntfy.ntfy_err_FP_wrong_mode_fail()
    exit()
if RUN_MODE == "recover-local" or RUN_MODE == "rl" and RECOVERY_ZIP is None:
    script.err_msg("ZIP file not specified. Program will exit.\n\n")
    if NTFY_ENABLED == True:
        ntfy.ntfy_err_ZIP_missing_fail()
    exit()





if RUN_MODE == "backup-local" or RUN_MODE == "bl":
    script.info_msg("CRATE is running in localhost backup mode.\n\n")

    source_dir_readable = rwcheck.check_source_readable(SOURCE_DIR) # Will call exit() if unreadables are found
    if source_dir_readable == False:
        script.err_msg("Source dir is not readable. Program will exit.\n\n")
        if NTFY_ENABLED == True:
            ntfy.ntfy_err_source_dir_unreadable_fail()
        exit()

    dest_dir_writable = rwcheck.check_destination_writable(DEST_DIR) # Will call exit() if unwritable
    if dest_dir_writable == False:
        script.err_msg("Source dir is not readable. Program will exit.\n\n")
        if NTFY_ENABLED == True:
            ntfy.ntfy_err_dest_dir_unwriteable_fail()
        exit()

    
    if source_dir_readable == True and dest_dir_writable == True:
        file.create_hostname_subdirs(HOSTS, DEST_DIR, RUN_MODE)
        zip_to_offsite = file.perform_backup_local(SOURCE_DIR, DEST_DIR, NTFY_ENABLED)
        # Errors & Ntfy are handled within perform_backup_local


    # Run retention on local
    if LOCAL_RETENTION_ENABLED == True:
        script.info_msg("Running retention cleanup on local copy. Retention period: " + str(LOCAL_RETENTION_PERIOD_DAYS) + " days")
        retention.localhost_basic_retention(DEST_DIR, LOCAL_RETENTION_PERIOD_DAYS, NTFY_ENABLED)
    else:
        script.info_msg("Local retention cleanup disabled, skipping retention cleanup.\n\n")


    # Ntfy for local backup completion
    if NTFY_ENABLED == True:
        ntfy.ntfy_ok_local_backup_complete()


    # Run Offsite backup
    if OFFSITE_BACKUP_ENABLED == True:
        script.info_msg("Offsite backup is enabled. Offsite mode: " + str(OFFSITE_BACKUP_MODE))


        if OFFSITE_BACKUP_MODE == "local":
            file.copy_to_offsite_dir(zip_to_offsite, LOCAL_OFFSITE_BACKUP_DIR, HOSTS, NTFY_ENABLED)
            #Ntfy handled within function


        if OFFSITE_BACKUP_MODE == "sftp":
            sftp.copy_to_sftp_dir(zip_to_offsite, HOSTS, SFTP_USER, SFTP_PASS, SFTP_HOST, SFTP_PATH, NTFY_ENABLED)
            #Ntfy handled within function

    else:
        script.info_msg("Offsite backup disabled, skipping...")



    # Run retention on offsite 
    if OFFSITE_RETENTION_ENABLED == True:
        script.info_msg("Running retention cleanup on offsite copy. Retention period: " + str(LOCAL_RETENTION_PERIOD_DAYS) + " days")

        if OFFSITE_BACKUP_MODE == "local":
            retention.localhost_basic_retention(LOCAL_OFFSITE_BACKUP_DIR, LOCAL_RETENTION_PERIOD_DAYS, NTFY_ENABLED)
        
        elif OFFSITE_BACKUP_MODE == "sftp":
            retention.sftp_basic_retention(HOSTS, SFTP_USER, SFTP_PASS, SFTP_HOST, SFTP_PATH, OFFSITE_RETENTION_PERIOD_DAYS, NTFY_ENABLED)

    else:
        script.info_msg("Offsite retention cleanup disabled, skipping retention cleanup.")













elif RUN_MODE == "recover-local" or RUN_MODE == "rl":
    script.info_msg("CRATE is running in localhost recovery mode.\n\n")

    confirmed = script.recovery_confirmation(RECOVERY_ZIP, RECOVERY_HOST, SOURCE_DIR, RUN_MODE) # Will call exit() if arguments missing
    if confirmed:
        source_dir_writable = rwcheck.check_source_writable(SOURCE_DIR) # Will call exit() if unreadable files are found
        dest_dir_readable = rwcheck.check_destination_readable(RECOVERY_ZIP) # Will call exit() if zip is unreadable

        if source_dir_writable == True and dest_dir_readable == True:
            docker_installed = container.is_docker_installed()
            podman_installed = container.is_podman_installed()
           
            if docker_installed:
                container.kill_and_delete_docker_containers()

            if podman_installed:
                container.kill_and_delete_podman_containers()

            recovery_status = file.perform_recovery_local(RECOVERY_ZIP, SOURCE_DIR, SKIP_RM) # Will call exit if no perms to delete SOURCE_DIR and -srm is not used
            if recovery_status == "ok":
                script.ok_msg("Recovery successful!\n\n")
                if NTFY_ENABLED == True:
                    ntfy.ntfy_ok_recovery_sucess()
            if recovery_status == "badzip":
                script.err_msg("Recovery failed due to an invalid zip archive. Try again as root or with a different archive.\n\n")
                if NTFY_ENABLED == True:
                    ntfy.ntfy_err_recovery_zip_error()
            if recovery_status == "error":
                script.err_msg("Recovery failed due to an unknown error. Try again as root or with a different archive.\n\n\\s")
                if NTFY_ENABLED == True:
                    ntfy.ntfy_err_recovery_unknown_error()

            if FIX_PERMS == True:
                perms_valid = file.sanity_check_permission_config(CONTAINER_USER, PERMISSION)
                if perms_valid == True:
                    file.fix_recovery_permissions(SOURCE_DIR, CONTAINER_USER, PERMISSION) # Will call exit if not running as root
                else:
                    script.err_msg("Permission configuration sanity check failed. Program will now exit...")
                    if NTFY_ENABLED == True:
                        ntfy.ntfy_err_recovery_unknown_error()
                    exit()
            else:
                script.info_msg("Fix permissions was not specified - skipping... (use -fp and try again as root if this was unintentional)")

        else:
            confirmed = script.recovery_confirmation(arguments.arg_recover, arguments.arg_zip, RECOVERY_ZIP, RECOVERY_HOST, SOURCE_DIR)


else:
    script.err_msg("Invalid run mode selected.\nRun with -m [bl,rl] or --help for more.\n\n")
    if NTFY_ENABLED == True:
        ntfy.ntfy_err_invalid_run_mode()
    exit()







