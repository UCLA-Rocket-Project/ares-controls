ares-controls :rocket:
=============
Control systems software for the Ares rocket

## Getting Started

#### 1. Clone the repository
```bash
$> # clone repository (HTTP):
$> git clone https://github.com/UCLA-Rocket-Project/ares-controls
$> # OR use SSH:
$> git clone git@github.com:UCLA-Rocket-Project/ares-controls
```

#### 2. Install Dependencies, as needed

MCU:
> For building the MCU software, you will need to import the project into the Arduino IDE

CDH and MOIST:
```bash
$> # 1. Python3
$> apt-get install python3 #  this may not work - see online for better instructions
$> # 1.5. pip3
$> apt-get install python3-pip
$> # 2. pyserial
$> pip3 install pyserial
$> # 3. zip (for deployment via makefile)
$> apt-get install zip
```
> Make sure you use sudo if needed! (if anything ever complains about permissions, try sudo)

> Both cdh and moist will run on any device with python3, with certain functionality only available on the Raspberry Pi (more details on configuring Raspberry Pi to be included later)

#### 3. Edit projects, as needed

Read the project-specific documentation (README.md within each subfolder) for more information on each project

> Edit projects using your favorite editor - we suggest the Arduino IDE for the MCU project, and something like atom for the others (or vim/nano/emacs if running via ssh on the Raspberry Pi)

#### 4. Testing and Deployment

###### MCU:
For Arduino projects, test using the Arduino IDE

###### MOIST/CDH:
Run the project by calling one of the following (replace `cdh` or `cdhserv` with `moist`)
```bash
$> # To test without building via make:
$> python3 cdh/ # OR USE
$> python3 cdh/__main__.py
$> # To make an executable but test locally:
$> make cdh
$> ./bin/cdhserv # run the file (note: typing out python3 is optional)
$> # To make and deploy for production:
$> make cdh-deploy
$> /deploy/cdhserv
```

> For info on using MOIST and CDH programs as services with systemd, see their respective README files

#### 5. Contributing Code

When you have finished writing and testing your code:

```bash
$> # run git status to get the current status of our working copy
$> git status

$> # make sure we have the latest of what's on the server
$> git fetch

$> # make sure we're on a branch (not master!), related to whatever changes we made
$> git checkout -b [branchName] # if the branch needs to be created
$> git checkout [branchName] # if the branch already exists

$> # stage the files that we'd like to commit
$> git add . # stage all files
$> git add file1 file2 file3 # stage specific files
$> git add -p # patch add: lets you stage individual changes (useful!)

$> # if you accidentally stage something you don't want to commit:
$> git reset filename # this doesn't delete your changes, it just unstages them
$> git reset --hard filename # WARNING: this reverts all changes

$> # commit our changes
$> git commit -m "commit message here" # if git is configured with your name/email
$> git commit -m "commit message here" --author="Some Name <someone@ucla.edu>"

$> # push our changes to the repository!
$> git push -u origin [branchName] # if the branch was newly created
$> git push # if the branch already exists on the repository
$> # Note: merging might be required if changes were made upstream
```
> Make sure you **commit very frequently**, and break up commits so that each commit only includes changes within its scope. Don't be afraid to commit dozens of times in a day!

> ```git add -p``` can be your best friend when you have lots of changes that you're trying to split into several commits

> Obviously, this is just a brief primer on git. For more details, check out [this really neat tutorial.](https://www.atlassian.com/git/tutorials)

##### Merging into Production
When you are ready to integrate your code into the master branch:
[Create a Pull Request!](https://github.com/UCLA-Rocket-Project/ares-controls/compare)
> use `master` as the base, and compare your own branch
