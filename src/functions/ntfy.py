import requests
import socket
from configparser import ConfigParser 


############################
# Parse NTFY Config
############################
config = ConfigParser()
config.read('/usr/share/ContainerCleaner/conf/config.ini')

NTFY_HOST = str(config['NTFY']['NTFY_HOST'])
NTFY_TOPIC = str(config['NTFY']['NTFY_TOPIC'])
############################


hostname = str(socket.gethostname())





# Start of script argument sanity check errors 
def ntfy_err_FP_wrong_mode_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Fix Permissions argument specificed but CRATE is running in recovery mode. Mode/Arg are incompatible - check run command.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })

def ntfy_err_ZIP_wrong_mode_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Zip file argument specificed but CRATE is running in backup mode. Mode/Arg are incompatible - check run command.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })   

def ntfy_err_SRM_wrong_mode_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Skip remove argument specificed but CRATE is running in backup mode. Mode/Arg are incompatible - check run command.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })       

def ntfy_err_FP_wrong_mode_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Fix permissions argument specificed but CRATE is running in backup mode. Mode/Arg are incompatible - check run command.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })     

def ntfy_err_ZIP_missing_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Zip file not specificed but CRATE is running in recovery mode. Mode/Arg are incompatible - check run command.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })        

def ntfy_err_invalid_run_mode():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Invalid run mode. Check run command.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })         




# Backup Local mode - Local backup
def ntfy_err_source_dir_unreadable_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Source dir is not readable.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })  


def ntfy_err_dest_dir_unwriteable_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Run failed on " + hostname + " - Destination dir is not readable.",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })      



def ntfy_err_ZIP_validation_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data=hostname + " - Backup ZIP failed validity check. Needs manual investigation to ensure file integrity.",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "x,pensive"
        }) 

def ntfy_warn_ZIP_validation_fail():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data=hostname + " - Backup ZIP validity check shows potential error. Needs manual investigation to ensure file integrity.",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "exclamation,raised_eyebrow"
        })      


def ntfy_ok_local_backup_complete():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Local backup complete on " + hostname,
        headers={
            "Title": "CRATE",
            "Priority": "default",
            "Tags": "white_check_mark,slightly_smiling_face"
        })       

def ntfy_warn_local_retention_error():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Local backup retention error on " + hostname + " - Possible permission issue?: ",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "exclamation,raised_eyebrow"
        })      




# Backup Local mode - offsite global
def ntfy_err_offsite_fail_no_zip():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Offsite backup failed on " + hostname + " - Local source ZIP doesn't exist / not readable",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "x,pensive"
        })      




# Backup Local mode - Local offsite
def ntfy_err_offsite_local_fail_dir_create():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Local offsite backup failed on " + hostname + " - Unable to create destination directory. Permission error?",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "x,pensive"
        })     

def ntfy_err_offsite_local_fail_copy():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Local offsite backup failed on " + hostname + " - Unable to copy zip to destination directory. Permission error/Out of storage?",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "x,pensive"
        })   

def ntfy_ok_offsite_local_complete():
        requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Offsite (local mode) backup complete on " + hostname,
        headers={
            "Title": "CRATE",
            "Priority": "default",
            "Tags": "white_check_mark,slightly_smiling_face"
        })  



# Backup Local mode - SFTP offsite 
def ntfy_err_offsite_sftp_connection(e):
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="SFTP offsite backup failed on " + hostname + " - Unable to connect to SFTP server: " + e,
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "x,pensive"
        })   

def ntfy_warn_sftp_retention_error():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="SFTP offsite backup retention error on " + hostname + " - Possible SFTP permission issue?",
        headers={
            "Title": "CRATE",
            "Priority": "high",
            "Tags": "exclamation,raised_eyebrow"
        })  

def ntfy_ok_offsite_sftp_complete():
        requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Offsite (sftp mode) backup complete on " + hostname,
        headers={
            "Title": "CRATE",
            "Priority": "default",
            "Tags": "white_check_mark,slightly_smiling_face"
        })  



# Recover Local mode
def ntfy_ok_recovery_sucess():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Recovery complete on " + hostname,
        headers={
            "Title": "CRATE",
            "Priority": "default",
            "Tags": "white_check_mark,slightly_smiling_face"
        })  


def ntfy_err_recovery_zip_error():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Recovery failed on " + hostname + " - ZIP error. Try again with root or use a different archive",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })   

def ntfy_err_recovery_unknown_error():
    requests.post(NTFY_HOST + "/" + NTFY_TOPIC,
        data="Recovery failed on " + hostname + " - Unknown error. Try again with root?",
        headers={
            "Title": "CRATE",
            "Priority": "urgent",
            "Tags": "x,pensive"
        })   






# ✅🙂 - "Tags": "white_check_mark,slightly_smiling_face"
# ❗🤨 - "Tags": "exclamation,raised_eyebrow"
# ❌😔 - "Tags": "x,pensive"
# https://docs.ntfy.sh/emojis/

# Priorities: urgent (5), high (4), default (none) (3), low (2), min (1)
# https://docs.ntfy.sh/publish/






















