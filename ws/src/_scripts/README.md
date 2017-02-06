RSS-Team9 Convenience Scripts
===============
Introduction:
----------------
This folder contains useful scripts that make working with git, the daughter bot, and ros easier.

Installation:
----------------
```
./INSTALLME.sh
```

Note: will install sshpass package to simplify ssh'ing into the dbot and automatically executing commands

Usage:
----------------
Installation will add the following bash scripts to your environment:
```
--LOCAL COMMANDS--
cdws - cd to the dbot source folder of the catkin workspace
sshcar - ssh to the dbot
rosenv - print out ros environment variables
gs - git status
gpush $1 - Full commit from racecar repository root directory, where first argument is commit message
gpull - pull current branch from racecar repository root directory
gmb $1 - make git branch where branch name is first arguement. Branch is pushed to origin and upstream is set.
roslocal - set ros environments for local/simulator usage
rosremote - set ros environment for roscore on physical dbot
cm - catkin_make from correct directory (accelerated)
cmr - catkin_make from correct directory (release build)
cmc - catkin_make from correct directory (rebuild)

--REMOTE COMMANDS--
rmake - remote catkin_make on robot
rpull - remote git pull
rlaunch $1 $2 - remote launch a launch file $1=package $2=launch file
gpp $1 - "git push pull" Push locally then pull on remote $1 = commit msg
```
