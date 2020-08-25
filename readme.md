TaskWarriorOpenProject
=============================

Purpose of this projects is to scratch my own itches:

1. Synchronize my TaskWarrior tasks with Team OpenProject Server
2. Learn some git
3. Learn some python

I try to it generic, but covering my needs.

Feel free to use it, but at your own risc.

### TODO
[ ] Make code cleaner. It is a confusion.
[ ] When create new task, also update the status and do not leave as new


### Using it

    $ git clone https://github.com/flippipe/twop
    $ cd twop
    $ twop/bin/twop.sh

Firt time it run, tries to generate the configuration file. Be prepared to fullfield your `OpenProject URL`  and your `API Key`.

### thanks for...

Scot, for your [python-packaging tutorial](https://python-packaging.readthedocs.io/en/latest/about.html)


### Lessons Learned

| Context | Problem | Resolution | 
|---|---|---|
|OpenProject| PATCH call returns error: "Could not update the resource because of conflicting modifications." | In API call must be sent lockVersion attribute with the version return earlier |