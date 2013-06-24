# JIRA Replace Label

Small script to replace/rename labels in JIRA.

Bulk replaces in the UI can only replace the entire contents of the labels field, obliterating other labels. This small script uses the excellent python-jira library to replace individual label names within the field, preserving other labels.

You will need to install python-jira 0.13 or better.

## Debianizing

Build a `debian` directory:

```
sudo apt-get install python-all python-stdeb
python setup.py --command-packages=stdeb.command debianize
```

Note the required python-jira package is not currently in the main Debian/Ubuntu repositories.

## Building a Debian package from checkout

```
sudo apt-get install python-all python-stdeb
python setup.py --command-packages=stdeb.command bdist_deb
```
