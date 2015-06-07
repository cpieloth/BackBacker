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
$ backbacker -j jobs/example.bb
```


Installation & Usage
--------------------

* Clone repository:
```
$ git clone https://github.com/cpieloth/BackBacker.git BackBacker
```
* Install BackBacker:
```
$ cd BackBacker
$ python setup.py install
```
* Modify config (optional):
```
$ vi configs/backbacker.cfg
```
* Create a backup job:
```
$ cp jobs/example.bb jobs/myjob.bb   
$ vi jobs/myjob.bb
```
* Run your backup job (NOTE: Use absolute paths!)
```
$ backbacker -c configs/backbacker.cfg -j jobs/myjob.bb
```
* Create a cron job (optional):
```
$ crontab -e
```


Coding Style
------------

* https://www.python.org/dev/peps/pep-0008
* https://www.python.org/dev/peps/pep-0257
* http://editorconfig.org
* See .editorconfig in project root


TODO
----

* scp
* variables in job script, e.g. ${BACKUP_DIR} is replaced by pre-processing config file.
