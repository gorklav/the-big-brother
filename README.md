# The Big Brother
 The Big Brother is a simple file integrity monitoring tool written with python. The tool scans all the files in the given path continuously and warns the user for any changes. The tool also saves all the events in a log file. The tool uses sha256 hashing algorithm by default. md5, sha1, sha224, sha384 and sha512 are also supported. User can specify these other hashing algorithms.

## Installation
This tool requires Python. You have to install Python in your system first. Then clone this repository to your system.
### On linux
```
sudo apt get-install python
git clone https://github.com/gorklav/the-big-brother.git  
```
## Usage
```
python main.py -d PATH
```
To see the help message use ```main.py -h``` or ```main.py --help```

### The help message
```Usage: Usage: main.py [options]

THE BIG BROTHER: BASIC FILE INTEGRITY MONITOR

Options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory=DIRECTORY
                        Specify directory
  -r, --reset-baseline  (Optional) Deletes the existing baseline, creates a
                        new one and exits
  -a ALGORITHM, --algorithm=ALGORITHM
                        Choose hashing algorithm (default: sha256): md5, sha1,
                        sha224, sha256, sha384, sha512
  -l LOG_FILE, --log-file=LOG_FILE
                        Name the log file (default: events.log)
  -b BASELINE, --baseline=BASELINE
                        Name the baseline file (default: baseline_[hash algorithm]_[Destination Folder].txt)```
