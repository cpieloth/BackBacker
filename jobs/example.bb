# Example backup script, change folders for your system.
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
tar.gz: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
mysqldump_gzip: db_name=database; db_user=user; db_passwd=password; dest_dir=/tmp;