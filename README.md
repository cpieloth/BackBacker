BackBacker - A light backup tool.
=================================

in progress


Concept
-------

Run backup job:
```
$python backbacker.py config=~/config.cfg job=~/job.bb
```

Config file:
```
$backbacker.cfg  
log_type=file
log_file=/var/log/backup.log
```

Job script with one instruction per line:
```
$cat job.bb
mount_smb: mnt_folder=/media/backup; config=~/smb.cfg
git_bundle: src=~/project.git; dest=/media/backup
redmine: dest=/media/backup; folder=/var/www/redmine; dbname=redmine; dbuser=redmine; dbpasswd=redmine
umount: mnt_folder=/media/backup;
```
