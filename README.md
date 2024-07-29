# Systems_Programming_WoC_JimiPatel
This is the Python Systems Programming repository where I upload exercise solutions and projects.

# VCS - A Version Control System

VCS is a simple version control system that allows you to manage changes to files over time. It provides functionality to initialize a repository, add files, commit changes, log commit history, checkout specific commits, and push changes to another directory.

## Features

- **Initialize a Repository**: Set up a new VCS repository.
- **Add Files**: Add files to the index to be committed.
- **Commit Changes**: Commit the current state of the index with a message.
- **Remove Last Commit**: Remove the most recent commit.
- **Log Commit History**: Display the commit history.
- **Checkout Specific Commit**: Revert the working directory to a specific commit.
- **Push Changes**: Push the latest commit to another directory.
- **Remove Added Files**: Clear the index of added files.
- **Status**: Show the status of files in the working directory.

python main.py init
python main.py add <file>
python main.py commit -m <message>
python main.py rmcommit
python main.py log
python main.py checkout <commit-hash>
python main.py push <destination-path>
python main.py rmadd
python main.py status
python main.py help
