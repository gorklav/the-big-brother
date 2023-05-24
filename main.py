import hashlib
import os
import logging
from time import sleep
from optparse import OptionParser




#THE BIG BROTHER: BASIC FILE INTEGRITY MONITOR



#Options
parser= OptionParser()

parser.add_option('-d', '--directory', dest= 'directory', help= "Specify directory")

parser.add_option('-r', '--reset-baseline', dest= 'reset_baseline', action="store_true", default= False, help= '(Optional) Deletes the existing baseline, creates a new one and exits')

parser.add_option('-a', '--algorithm', dest= 'algorithm', help= 'Choose hashing algorithm (default: sha256): md5, sha1, sha224, sha256, sha384, sha512')

parser.add_option('-l', '--log-file', dest='log_file', default='events.log', help='Name the log file (default: events.log)')

parser.add_option("-b","--baseline",dest= "baseline", help= "Name the baseline file (default: baseline_[hash algorithm]_[Destination Folder].txt)")

#Help Output
parser.description = "THE BIG BROTHER: BASIC FILE INTEGRITY MONITOR"
parser.usage = "Usage: %prog [options]"

(options, args) = parser.parse_args()




#Calculate hashes of files 
def hash_file(file_name, algorithm):
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'sha224':
        hasher = hashlib.sha224()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'sha384':
        hasher = hashlib.sha384()
    elif algorithm == 'sha512':
        hasher = hashlib.sha512()
    else:
        raise ValueError(f'Invalid algorithm: {algorithm}')
    
    #Reads the file in binary mode and returns the content in chunks of 65536 bytes.
    with open(file_name,"rb") as f:
        content = f.read(65536)
        hasher.update(content)
    return hasher.hexdigest()


#Calculate hashes of the files in the directory
def calculate_hashes(file_name):
    hashes = {}
    for root,dirs,files in os.walk(file_name):
        for file in files:
            file_name = os.path.join(root,file)
            file_hash = hash_file(file_name, hash_algorithm)
            hashes[file_name] = file_hash
    return hashes


    

#Store hashes in a txt file
def create_new_baseline(file_path):
    hashes = calculate_hashes(file_path)
    with open(baseline_file,"w",encoding="utf-8") as f:
        for key,value in hashes.items():
            f.write(f"{key} | {value}\n")

    logging.info(f"Baseline Updated: {file_path}")
    sleep(1)
    print("Baseline Updated")


#Monitoring Proccess
def monitor_files():
    print("THE BIG BROTHER IS WATCHING YOUR FILES".center(50,"-"))
    sleep(1)
    print(f"\nMonitoing started: {file_path}")
    logging.info(f"Monitoing started: {file_path}")
    

    while True:
        try:    
            
            #Read existing baseline if there's none creates a new one
            try:
                baseline_hashes = {}
                with open(baseline_file,"r",encoding="utf-8") as f:
                    for line in f:
                        filepath, file_hash = line.split("|")
                        baseline_hashes[filepath.strip()] = file_hash.strip()
            
            except FileNotFoundError:
                print("\nNo baseline found. Creating new one.")
                create_new_baseline(file_path)
                


            #Calculate current paths and hashes
                current_hashes = calculate_hashes(file_path)
                current_paths = set(current_hashes.keys())
            
            #Check for new and changed files
            for root,dirs,files in os.walk(file_path):
                for file in files:
                    filepath = os.path.join(root,file)

                    if not filepath in baseline_hashes:
                        with open(baseline_file,"a",encoding="utf-8") as f:
                            f.write(f"{filepath} | {hash_file(filepath,hash_algorithm)}")

                        print(f"New file added: {filepath}")
                        logging.info(f"New file added: {filepath}")
                        create_new_baseline(file_path)
                        continue

                    elif current_hashes[filepath] != baseline_hashes[filepath]:
                        print(f"File changed: {filepath}")
                        logging.info(f"File changed: {filepath}")
                        create_new_baseline(file_path)
                        continue

            #Check for deleted files
            for filepath in baseline_hashes.keys():
                if filepath not in current_paths:
                    print(f"File deleted: {filepath}")
                    logging.info(f"File deleted: {filepath}")
                    create_new_baseline(file_path)
                    continue    

        #Close the program
        except KeyboardInterrupt:
            create_new_baseline(file_path)
            sleep(1)
            print("Exiting...")
            exit()    



file_path = options.directory


if not options.directory:
    parser.print_help()
    exit()


#Check the given path exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f'No such file or directory: {file_path}')
    


#sha256 algorithm is default unless user specifies another algorithm
hash_algorithm = "sha256"

if options.algorithm:
    hash_algorithm= options.algorithm


#Unlike Linux, Windows operating systems use backslash (\) instead of slash (/).
#This if statement makes this program usable with both operating systems. 
slash = "/"
if "\\" in file_path:
    slash = "\\" 
    file_path= file_path + slash


baseline_file= f"baseline_{hash_algorithm}_{file_path.split(slash)[-2]}.txt"

#User can name the baseline file instead of using the default name
if options.baseline:
    baseline_file = options.baseline


#Resets the baseline and exits
if options.reset_baseline:
    create_new_baseline(file_path)
    exit()


#This program creates a log file if there's none
#Every time the program started, the program appends events in the log file
log_file = 'events.log'

#User can enter a name for the log file
if options.log_file:
    log_file = options.log_file

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s', handlers=[logging.FileHandler(log_file, mode='a')])



try:
    while True:
        monitor_files()

except KeyboardInterrupt:
    print("Exiting")
    sleep(1)
    logging.INFO("Program closed")
    exit()
