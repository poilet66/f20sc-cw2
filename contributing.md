# Setup

## Prerequisites
 - Python 3.10 or newer


## Downloading
To download the code, you can either use the github Desktop app to clone the code or use git from the terminal as below

```
git clone git@github.com:poilet66/f20sc-cw2.git
```

## Setup

### Venv (Optional)
To set up a venv, run the following commands. If you are not setting up a venv, proceed to Installing Modules.

```
python -m venv venv

[WINDOWS ONLY]
venv/Scripts/activate.bat

[MAC/LINUX ONLY]
source venv/bin/activate
```

### Installing Modules
To install the modules required for the project to work run the following command

```
pip install -r requirements.txt
```

### Running the GUI
To run the program simply run 

```
python main.py
```

This will bring up the graphical user interface.

### Running the command line interface
Simply invoke the same way but with flags. The program will automatcially determine which mode to run in

```
python main.py -t 2a -f file.json
```

-t the task `[2a, 2b, 3a, 3b, 4, 5d, 6, 7]`
-f The file name
-u The uuid of the user to search
-d The uuid of the document to search


## Contributing

To contribute, first create a task in the project section and create a linked issue. 

Then create a branch from main, this is where you will make all your changes. 

```
git checkout -b <your branch name>
```

Frequently commit your changes to your branch with helpful commit names. Commits should be atomic, making only focused, single pupose changes.

```
git commit -m "implemented question 2a in data controller"

git push
```

Once all the features and/or have been implemented, create a pull request on GitHub from your branch into main. This pull request will then be reviewed by at least one other developer before fully merging.






