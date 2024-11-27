## Change log

### V 1.2
- Implement ntfy notifications
- Added some missing error messages before exit conditions


### V 1.1
- Broke changelog out into its own file
- Moved issues from readme to git issues 
- Added retention policy to offsite backup
- Added second offsite backup mode (now supports local and SFTP)


### V 1.0
- Public refactor of V1.3 CERN
	- Removed AFS/Kerberos support (propriatery to CERN)
	- Deprecated internal spec/cron files and moved them to an example dir
	- Santised config.ini
	- Removed mail support (propriatery to CERN)
	- Removed selfcheck (monitor/alert system) support (propriatery to CERN)
- Overhauled Readme 
- Refactored the ok/warn/err/info messages to make printing them more efficient 
- Implemented primative argument clash validity checks
- Implemented user and chmod value validity check for recover mode
- Scrapped the backup remote and recover remote SFTP modes - they were too unreliable
- Bug fixes


### V 1.3 - CERN
- Implemented support for renewing kerberos tokens for AFS
- CRON time changed from 20:30 to 06:30 and 18:30 (needs to run twice daily due to 24h AFS token expiration) 
- Bug fixes 


### V 1.2 - CERN
- Implemented self-check (only in backup local mode with arg to enable)
- Implemented remote recovery via SSH
- Overhaul of remote backup and some SSH related functions
- Bug fixes


### V 1.1 - CERN
- Implemented colorama and improved messages for overall better shell output
- Implemented remote backups via SSH
- Implemented email notifications for backup-local success/failure and backup-remote summary
- Implemented a basic retention policy (delete after X days)
- Fixed spec file, RPM should now be build-able
- Many bug fixes


### V 1.0 - CERN
- Initial no-thrills release. Still experimental/WIP but local recover/backup are working. 



______________________
&nbsp;
&nbsp;


## Feature wish-list
- Short term: 
	- Add RW tests for remote backup and restore with error on cant read/write correctly (partially implemented???)
	- Add support for permission fixing and recovery validity after running remote restore (partially implemented???)
	- Re-implement mail errors or add Ntfy notifications
	- Add zip validation to remote backup (on-hold as the method used in local is currently broken, see known bugs)
	- Add ability to blacklist certain files that become problematic (eg always open log files or symlinks - although only the latter should be problematic if containers are killed first)
	- Add ability for occasional snapshots (say in in every X number) to be copied to a second location to enable offsite backup
		- In my case, fileserver SMB shares OneDrive
	- Change from shutil to zipfile so that zips can have compression
- Long term:
	- Add TQDM progress bars (or at least some indication the archive process is working as many GB = no output for a few mins) - although maybe not necessary if running with CRON anyway
	- Add proper python logging - could eventually be attached to error emails or Ntfy notifications
	- Add advanced retention policy (keep 1 yearly, 1 monthly, 1 weekly until end of month, daily for a week etc)  
	- Add support for Docker's/Podman's "Volumes"
	- Publish docker container version