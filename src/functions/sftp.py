import pysftp
import os
from functions import script


def copy_to_sftp_dir(zip_to_offsite, HOSTS, SFTP_USER, SFTP_PASS, SFTP_HOST, SFTP_PATH):
    # Construct SFTP destination path
    sftp_path_host_added = str(SFTP_PATH + "/" + HOSTS)


    # Check if the source ZIP file exists
    if not os.path.isfile(zip_to_offsite):
        script.err_msg(f"The file {zip_to_offsite} does not exist.")
        return


    # SFTP connection options
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key checking to prevent automation fail

    try:
        # Connect to the SFTP server
        with pysftp.Connection(host=SFTP_HOST, username=SFTP_USER, password=SFTP_PASS, cnopts=cnopts) as sftp:
            # Navigate to the desired path on the remote server
            sftp.makedirs(sftp_path_host_added)  # Create the directory if it doesn't exist
            sftp.chdir(sftp_path_host_added)

            # Upload the file
            sftp.put(zip_to_offsite)

            script.ok_msg("Offsite backup zip successfully uploaded to the SFTP server.\n\n")
    

    except Exception as e:
        script.err_msg("An error occured, unable to backup to the SFTP server:\n")
        print(e)


