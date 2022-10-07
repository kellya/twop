TaskWarriorOpenProject
======================

This is a fork of the [original twop](https://github.com/flippipe/twop).  The
project is archived, and is the first one I found that looks to do what I wanted
out of a synchronizer.

Since I don't want to spend time figuring out all the openproject API stuff (in
particular) I am riding on the shoulders of those who have done that hard work
before me :)

### What do I want to add to this?

    - [ ] Modern tooling (poetry in particular)
    - [ ] CLI options (via click probably)
    - [ ] XDG_CONFIG_HOME based config file
    - [ ] Maybe yaml-based config
    - [ ] Others as I discover stuff I want to do that it doesn't yet :)

### Using it

    Clone the repo: git clone https://github.com/kellya/twop

    Get into the cloned dir: cd twop

    (you may want to set up a virtual environment here)

    Install this: pip install .

### Updating it
    Within the cloned repo dir:

    update from remote: git pull

    reinstall: pip install --force-reinstall .


### First run

The first time twop is run, it will generate a configuration file in the current
directory.  You must have the following information:

Your OpenProject base URL.  Something like "openproject.yourdomain.com"

Your API Key, which you can get by: 

    1. Log in to your openproject site
    2. Click on your user name in the upper right-hand corner
    3. Click on `my account`
    4. Click `Access Tokens`
    5. Click on `generate` on the API line.

After entering this information, twop will attempt to pull a project list to get
you started.
