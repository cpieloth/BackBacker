BackBacker - A light backup tool.
=================================

BackBacker is a light backup tool with a batch file based on simple commands with arguments.


Concept
-------

Job script with one instruction per line:
```
$ cat examples/job.bb
git_bundle -r /tmp/git_repo -d /tmp
hg_bundle -r /tmp/hg_repo -d /tmp
```

Run backup job:
```
$ backbacker.py batch examples/batch.bb
```

Additional you can run or use each command in your own script by using it as a sub-command:
```
$ backbacker.py git_bundle -r /tmp/git_repo -d /tmp
$ backbacker.py hg_bundle -r /tmp/hg_repo -d /tmp
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
$ editor examples/myconfig.ini
```
* Create a backup batch:
```
$ cp examples/batch.bb examples/batch.bb
$ editor examples/batch.bb
```
* Run your backup job
```
$ backbacker batch -c examples/config.ini examples/batch.bb
```
* Create a cron job (optional):
```
$ crontab -e
```
