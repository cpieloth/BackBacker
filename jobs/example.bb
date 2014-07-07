# Example backup script, change folders for your system.
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/home/user/tmp;
hg_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/home/user/tmp;
gzip: src_dir=/home/user/workspace/BackBacker; dest_dir=/home/user/tmp;
mysqldump_gzip: db_name=database; user=user; passwd=password; dest_dir=/home/user/tmp;
redmine_am: src_dir=/var/www/redmine; db_name=redmine; user=redmine; passwd=password; dest_dir=/home/user/tmp;
mount_smb: cfg_file=/home/user/workspace/BackBacker/configs/samba.cfg; url=//127.0.0.1/Backup; dest_dir=/media/backup;
mv_timestamp: datefmt=%Y-%m-%d; src_dir=/home/user/tmp; dest_dir=/media/backup;
backup_rotation: dir=/home/user/tmp; rotate=3;
umount: dir=/media/backup;