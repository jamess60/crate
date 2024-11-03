# CRATE (Container Recovery and Archival ToolsEt)
## Introduction

CRATE is a utility I wrote in my final days at CERN to facilitate the backup and restore of local container data (Docker, podman etc). This is a majorly re-factored fork to remove any CERN branding or propriatery libraries, but also add some new features.

CRATE has 2 modes:
- backup-local (Runs on localhost, auto/silent with cron/sysd, backups up data to a local path and optionally a local or sftp offsite path)
- recover-local (Runs on the local host, restores a backup archive to the data path - interactive only)
CRATE used to support backup remote and recover remote (multi host single instance via SFTP), but this was deprecated due to design shortfalls and reliability issues. 

For EL distibutions, there is a draft spec file included (in example dir) if you wish to build and distribute as RPM.
For any other distro, you will need to manually git clone to /usr/share and configure cron (example also included).
I may consider the inclusion of CRATE as a container in an upcomming release.

CRATE requires container data to be stored in a local directory, NOT within a docker volume. This is for 2 reasons - Firstly, this tool was initally designed to be used primarily with a really old Podman version where volumes weren't mature, Secondly, I much prefer a flat file system approach for my production containers as I like to know where my critical data actually lives. If docker volume support is heavily demanded, I may implement this in the future...


______________________
&nbsp;
&nbsp;

## How to use
1) Git Clone this repo to /usr/share
2) Install python3 and any additional dependencies (a requirements.txt is provided but you may need the python3-pkgname packages depending on distro)
	- Colorama
	- ast
	- configparser
	- datetime
	- pysftp
3) Edit conf/config.ini to configure CRATE for your environment
4) Run CRATE with syntax: `python3 src/crate.py -m $mode $args` (or let cron take care of it...)

Arguments:
| Short Arg    | Long Arg           | Action                                                     | Applies to                   |
|--------------|--------------------|------------------------------------------------------------|------------------------------|
| -h           | --help             | Display help info                                          | All cases                    |
| -m $mode     | --mode $mode       | Select which mode the script runs in                       | All cases                    |
| -z $zip_path | --zip $zip_path    | Provide zip to recover from                                | Recovery mode (mandatory)    |
| -srm         | --skip-rm          | Skips removing source dir before unzipping when recovering | Recovery mode (optional)     |
| -fp          | --fix-perms        | Chowns and chmods recovered data to values in config.ini   | Recovery mode (optional)     |


### Example commands:
#### backup-local (bl)
- Run command:
	Short example: `python3 src/crate.py -m bl`
	Long example: `python3 src/crate.py --mode backup-local`


#### recover-local (rl)
- Run command:
	Short example (skip remove source): `python3 src/crate.py -m rl -z /tmp/2023-08-23---16-25-25.zip -srm`
	Short example (fix perms): `python3 src/crate.py -m rl -z /tmp/2023-08-23---16-25-25.zip -fp`
	Long example (skip remove source): `python3 src/crate.py --mode recover-local --zip /tmp/2023-08-23---16-25-25.zip --skip-rm`
	Long example (fix perms): `python3 src/crate.py --mode recover-local --zip /tmp/2023-08-23---16-25-25.zip --fix-perms`



______________________
&nbsp;
&nbsp;


## Config file breakdown 
This section provides an explanation for each configurable within the config file. 


### Main
| Configurable | Description                                                                             |
|--------------|-----------------------------------------------------------------------------------------|
| SOURCE_DIR   | The directory that will be backed up in backup mode, or written to in recovery mode     |
| DEST_DIR     | The directory that will be written to in backup mode, contains the zips to restore from |


### Permissions 
| Configurable   | Description                                                                                 |
|----------------|---------------------------------------------------------------------------------------------|
| CONTAINER_USER | Recovery mode with fix permissions enabled will chown the restored data to this user        |
| PERMISSION     | Recovery mode with fix permissions enabled will chmod the restored data to this chmod value |


### Offsite
| Configurable              | Description                                                              |
|---------------------------|--------------------------------------------------------------------------|
| OFFSITE_BACKUP_ENABLED    | "True" or "False" Enables/Disables creating a 2nd offsite copy           |
| OFFSITE_BACKUP_MODE       | "local" (copies to a local file path) or "sftp" - Uploads to SFTP server |
| LOCAL_OFFSITE_BACKUP_DIR  | Path for offsite backup in local mode                                    |
| SFTP_USER                 | Username for SFTP Server                                                 |
| SFTP_PASS                 | Password for SFTP Server                                                 |
| SFTP_HOST                 | SFTP Server address/ip                                                   |
| SFTP_PATH                 | SFTP Server backup directory path                                        |



### Retention
| Configurable                  | Description                                                               |
|-------------------------------|---------------------------------------------------------------------------|
| LOCAL_RETENTION_ENABLED       | "True" or "False" Enables/Disables retentionc cleanup on the local copy   |
| OFFSITE_RETENTION_ENABLED     | "True" or "False" Enables/Disables retentionc cleanup on the offsite copy |
| LOCAL_RETENTION_PERIOD_DAYS   | Store backups for X days. Older backups will be deleted.                  |
| OFFSITE_RETENTION_PERIOD_DAYS | Store backups for X days. Older backups will be deleted.                  |



______________________
&nbsp;
&nbsp;

## Future expectations
Im a solo SysAdmin/Homelabber who wrote CRATE to automatically backup my own container data. This is not a full time job and I am not a software developer by trade. I anticipate updates (especially feature adds) will be slow at best. All the time it functions to a good enough degree in my homelab environment, thats that. That said, im open to taking feature suggestions and im open to anyone else who wishes to contribute/fork/maintain. This should be considered FOSS. 



## Screenshot
![screenshot](https://jamesmaple.co.uk/downloads/gitimg/crate/readme-screenshot.png)

	
