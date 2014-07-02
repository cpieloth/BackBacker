BackBacker - A light backup tool.
=================================

BackBacker is a light backup tool with a "declarative" job file based on simple commands with arguments.


Concept
-------

Job script with one instruction per line:
```
$ cat jobs/example.bb
git_bundle: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
tar.gz: src_dir=/home/user/workspace/BackBacker; dest_dir=/tmp;
```

Run backup job:
```
$ python backbacker.py -j jobs/example.bb
```


Installation & Usage
--------------------

1. Clone repository
```
$ git clone https://github.com/cpieloth/BackBacker.git BackBacker
```
2. Create a new branch for your backup jobs
```
$ cd BackBacker
$ git checkout -b jobs
```
3. Modify config (optional)
```
$ vi configs/backbacker.cfg
```
4. Create a job
```
$ cp jobs/example.bb jobs/myjob.bb
$ vi jobs/myjob.bb
```
5. Commit your setup (optional)
6. Run your backup job (NOTE: Use absolute paths!)
```
$ python backbacker.py -c configs/backbacker.cfg -j jobs/myjob.bb
```