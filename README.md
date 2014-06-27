BackBacker - A light backup tool.
=================================

in progress


Concept
-------

Run backup job:
```
$python backbacker.py config=~/backbacker.cfg job=~/myjob.bb
```

Config file:
```
$backbacker.cfg  
log_type=file
log_file=/var/log/backup.log
```

Job script with one instruction per line:
```
$cat myjob.bb
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
tar.gz: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
```
