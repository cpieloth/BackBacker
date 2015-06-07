BackBacker - A light backup tool.
=================================

BackBacker is a light backup tool with a "declarative" job file based on simple commands with arguments.
BackBacker requires Python 3, but a backport to Python 2 can be done easily.


Concept
-------

Job script with one instruction per line:
```
$ cat examples/job.bb
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
gzip: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
```

Run backup job:
```
$ backbacker examples/job.bb
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
$ python3 setup.py install
```
* Create a config (optional):
```
$ cp examples/config.ini examples/myconfig.ini
$ vi examples/myconfig.ini
```
* Create a backup job:
```
$ cp examples/jobs.bb examples/myjob.bb
$ vi examples/myjob.bb
```
* Run your backup job
```
$ backbacker -c examples/myconfig.ini examples/myjob.bb
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
