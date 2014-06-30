BackBacker - A light backup tool.
=================================

in progress


Concept
-------

Run backup job:
```
$python backbacker.py config=configs/backbacker.cfg job=jobs/example.bb
```

Config file:
```
$ configs/backbacker.cfg
log_type=console
# log_type=file
# log_file=/var/log/backbacker.log
```

Job script with one instruction per line:
```
$ cat jobs/example.bb
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
tar.gz: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
```
