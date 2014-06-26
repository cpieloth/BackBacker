BackBacker - A light backup tool.
=================================

in progress


Concept
-------

python backbacker.py config=~/config.cfg job=~/job.bb

backbacker.cfg
   log_type=file|syslog|...
   log_file=/var/log/backup.log

job.bb
   mount_smb: mnt_folder=/media/backup; config=~/smb.cfg
   git_bundle: src=~/project.git; dest=/media/backup
   redmine: dest=/media/backup; folder=/var/www/redmine; dbname=...;
   ...
   umount: mnt_folder=/media/backup;