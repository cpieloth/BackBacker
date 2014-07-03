BackBacker - A light backup tool.
=================================

BackBacker is a light backup tool with a "declarative" job file based on simple commands with arguments.


Concept
-------

Job script with one instruction per line:
```
$ cat jobs/example.bb
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
gzip: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
```

Run backup job:
```
$ python backbacker.py -j jobs/example.bb
```


Installation & Usage
--------------------

* Clone repository.
```
$ git clone https://github.com/cpieloth/BackBacker.git BackBacker
```
* Create a new branch for your backup jobs (optional).
```
$ cd BackBacker
$ git checkout -b jobs
```
* Modify config (optional).
```
$ vi configs/backbacker.cfg
```
* Create a backup job.
```
$ cp jobs/example.bb jobs/myjob.bb
$ vi jobs/myjob.bb
```
* Commit your setup (optional).
* Run your backup job (NOTE: Use absolute paths!)
```
$ python backbacker.py -c configs/backbacker.cfg -j jobs/myjob.bb
```
* Create a cron job (optional). 
```
$ crontab -e
```
