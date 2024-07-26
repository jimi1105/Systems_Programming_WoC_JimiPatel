import sys
import os 
import json 
import datetime
import hashlib
import base64
    
def hashfile(file):
    BUF_SIZE = 65536  # Define a buffer size of 65536 bytes (64 KB) for reading the file in chunks

    md5 = hashlib.md5()  # Create an md5 hash object from the hashlib module

    with open(file, 'rb') as f:  # Open the file in binary read mode ('rb')
        while True:  # Start an infinite loop
            data = f.read(BUF_SIZE)  # Read a chunk of the file with the size of BUF_SIZE
            if not data:  # If the read chunk is empty (end of file), break the loop
                break
            md5.update(data)  # Update the md5 hash object with the read chunk

    return md5.hexdigest()  # Return the hexadecimal digest of the hash object


# def write_json(new_data, filename):
#     with open(filename,'r+') as file:
#         file_data = json.load(file)
#         file_data["emp_details"].append(new_data)
#         file.seek(0)
#         json.dump(file_data, file, indent = 4)




def status():
    currdir=os.getcwd()
    Files=os.listdir(currdir)  #file and directories both
    filename=f"{currdir}/.VCS/branches/main/index.json"
    file_data=dict()

    check_file = os.stat(filename).st_size
    
    

    if(check_file == 0):
        for file in Files :
            file_extension = os.path.splitext(file)[1]
            temp = file_extension[1:]
            if(temp==''): continue
            print(file)
        return 
    

    with open(filename,'r+') as file:
        file_data = json.load(file)
    for file in Files:

        file_extension = os.path.splitext(file)[1]
        temp = file_extension[1:]
        if(temp==''): continue
        file_path = os.path.join(currdir, file)
        file_hash = hashfile(file_path)
        if file in file_data:
            if(file_data[file]!=file_hash):
                print(file)
        else:
             print(file)
    
    

def add():
     filename=sys.argv[2]
     currdir=os.getcwd()
     file_path = os.path.join(currdir, filename)
     if(os.path.exists(file_path)==0):
         print("File Not Exists")
         return
     file_hash = hashfile(file_path)


     jfilename=f"{currdir}/.VCS/branches/main/added.json"
     file_data=dict()
     check_file = os.stat(jfilename).st_size
     if(check_file != 0):
       with open(jfilename,'r+') as file:
        file_data = json.load(file)
     file_data[filename]=(file_hash)
   
     json_data = json.dumps(file_data, indent=4)
     added_file_path = f"{currdir}/.VCS/branches/main/added.json"
    
  
     with open(added_file_path, 'w') as json_file:
      json_file.write(json_data)

     jfilename = f"{currdir}/.VCS/branches/main/index.json"
     file_data=dict()
     check_file = os.stat(jfilename).st_size
     if(check_file != 0):
       with open(jfilename,'r+') as file:
        file_data = json.load(file)
     file_data[filename]=(file_hash)
   
     json_data = json.dumps(file_data, indent=4)
     index_file_path = f"{currdir}/.VCS/branches/main/index.json"
        
     with open(index_file_path, 'w') as json_file:
      json_file.write(json_data)

     print("added succesfully")
  



def init():
    # Step 1: Ask the user to set the username
    username = input("Enter your username: ")
    currdir=os.getcwd()
    branches_directory = os.path.join(".VCS", "branches")
    main_branch_directory = os.path.join(branches_directory, "main")
    if(os.path.exists(f"{currdir}/.VCS")==False):
        os.mkdir(".VCS")
        # if already exists then check
        
        # print(branches_directory)
        objects_directory = os.path.join(".VCS", "objects")
        os.mkdir(branches_directory)
        os.mkdir(objects_directory)

        
        os.makedirs(main_branch_directory)

        added_json_path = os.path.join(main_branch_directory, "added.json")
        index_json_path = os.path.join(main_branch_directory, "index.json")
        

        with open(added_json_path, 'w') as added_file:
            json.dump({}, added_file)

        with open(index_json_path, 'w') as index_file:
            json.dump({}, index_file)

    users_txt_path = os.path.join(main_branch_directory, "users.txt")                             
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(users_txt_path, 'w') as users_file:
        users_file.write(f"Date: {current_datetime}, Username: {username}\n")

def encode_file_content_to_base64(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return base64.b64encode(binary_data).decode('utf-8')
# def hashfile(file):
#     BUF_SIZE = 65536  # Define a buffer size of 65536 bytes (64 KB) for reading the file in chunks

#     sha256 = hashlib.sha256()  # Create a SHA-256 hash object from the hashlib module

#     with open(file, 'rb') as f:  # Open the file in binary read mode ('rb')
#         while True:  # Start an infinite loop
#             data = f.read(BUF_SIZE)  # Read a chunk of the file with the size of BUF_SIZE
#             if not data:  # If the read chunk is empty (end of file), break the loop
#                 break
#             sha256.update(data)  # Update the SHA-256 hash object with the read chunk

#     return sha256.hexdigest()  # Return the hexadecimal digest of the hash object

def commit():
 
    
   
    currdir=os.getcwd()
    fpath=f"{currdir}/.VCS/branches/main/added.json"
    check_file = os.stat(fpath).st_size

    if(check_file==0) :
       print("No changes available")
       return
 
    file_hash=hashfile(fpath)
    objectPath = f"{currdir}/.VCS/objects"

    cfiles=os.listdir(objectPath)

    match="0"
    last=""

    add_data={}
    with open(f"{fpath}", 'r') as file:
        add_data = json.load(file)
   
    if not cfiles:
        temp_data={}

        new_data={}
    
        for file in add_data:
            temp_path=f"{currdir}/{file}"
            encoded_data=encode_file_content_to_base64(temp_path)
            new_data[file]=encoded_data

        # with open(new_file_path, 'w') as json_file:
        #  json_file.write(json_data)

        temp_data["changes"]=new_data
        temp_data["all"]=new_data
        temp_data["message"]=sys.argv[3]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        temp_data["timestamp"]=timestamp

        new_file_path = f"{objectPath}/{file_hash}.json" 
        json_data = json.dumps(temp_data, indent=4)

        with open(new_file_path, 'w') as json_file:
         json_file.write(json_data)

        # empty_dict={}
        # json_data = json.dumps(empty_dict)

        with open(fpath, 'w') as file:
          file.write("")
    
        # with open(fpath, 'w') as json_file:
        #     json_file.write(json_data)

        print("Done successfully")
        
        return 


    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file
    
    last_data={}
    with open(f"{objectPath}/{last}", 'r') as file:
        last_data = json.load(file)

    new_data={}
    
    for file in add_data:
            temp_path=f"{currdir}/{file}"
            encoded_data=encode_file_content_to_base64(temp_path)
            new_data[file]=encoded_data

    temp_data={}
    temp_data["changes"]=new_data
    # new_data = {
    # "changes": add_data
    # } 
    
    for key in temp_data["changes"]:
        last_data["all"][key]=temp_data["changes"][key]
    
    last_data["changes"]=temp_data["changes"]
    last_data["message"]=sys.argv[3]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    last_data["timestamp"]=timestamp

    new_file_path = f"{objectPath}/{file_hash}.json" 
    json_data = json.dumps(last_data, indent=4)

    with open(new_file_path, 'w') as json_file:
      json_file.write(json_data)

    with open(fpath, 'w') as file:
           file.write("")

    print("Done successfully")

def rmcommit():

    match="0"
    last=""
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    os.remove(f"{objectPath}/{last}")

    match="0"
    last=""
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    last_commit_path=f"{objectPath}/{last}"
    state={}

    with open(f"{last_commit_path}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    all_file=os.listdir(currdir)

    for file in all_file:
          if(file=="main.py"):continue
          destination_path=os.path.join(currdir,file)
          if(os.path.isfile(os.path.join(currdir,file))):
              if file in all.keys():
                  decodedContent=base64.b64decode(all[file])

                  with open(destination_path, 'wb') as file:
                        file.write(decodedContent)
              else :
                os.remove(destination_path)
  
    print("Done Successfully")


def log():
    log={}
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"
    cfiles=os.listdir(objectPath)

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         log[creation_time_readable]=file
        
    myKeys = list(log.keys())
    myKeys.sort()
    sorted_log = {i: log[i] for i in myKeys}

    for x in sorted_log:
        fileName=sorted_log[x]
        filePath=f"{objectPath}/{fileName}"
        with open(f"{filePath}", 'r') as file:
         tempD = json.load(file)
        
        print("Author: Jimi Patel\n")
        print(f"Commit: {fileName[:-5]}\n")

        print("All files\n")

        for y in tempD["all"]:
            print(f"    {y}:{tempD["all"][y]}\n")

        print("Modified files\n")

        for y in tempD["changes"]:
            print(f"    {y}:{tempD["changes"][y]}\n")
    
        print(f"Message:{tempD["message"]}\n")
        print(f"Time Stamp:{tempD["timestamp"]}\n\n\n")

        

def checkout():
    hashvalue=f"{sys.argv[2]}.json"

    print(hashvalue)
    
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"

    creation_time = os.path.getctime(f"{objectPath}/{hashvalue}")
    hashtime = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cfiles=os.listdir(objectPath)

    for file in cfiles:
        creation_time = os.path.getctime(f"{objectPath}/{file}")
        creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if(creation_time_readable>hashtime):
            os.remove(f"{objectPath}/{file}")
   
    state={}

    with open(f"{objectPath}/{hashvalue}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    all_file=os.listdir(currdir)

    for file in all_file:
          if(file=="main.py"):continue
          destination_path=os.path.join(currdir,file)
          if(os.path.isfile(os.path.join(currdir,file))):
              if file in all.keys():
                  decodedContent=base64.b64decode(all[file])

                  with open(destination_path, 'wb') as file:
                        file.write(decodedContent)
              else :
                os.remove(destination_path)
  
    print("Done Successfully")
    
def push():
    destPath=sys.argv[2]
    match="0"
    last=""
    currdir=os.getcwd()
    objectPath = f"{currdir}/.VCS/objects"
    cfiles=os.listdir(objectPath)
    if(len(cfiles) == 0):
         print("No commits yet")

    for file in cfiles: 
         creation_time = os.path.getctime(f"{objectPath}/{file}")
         creation_time_readable = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         if(creation_time_readable>match):
            match=creation_time_readable
            last=file

    last_commit_path=f"{objectPath}/{last}"
    state={}

    with open(f"{last_commit_path}", 'r') as file:
        state = json.load(file)
    
    all={}
    all=state["all"]

    for file in all:
        decodedContent=base64.b64decode(all[file])
        file_path = os.path.join(destPath, file)

        with open(file_path, 'wb') as f:
         f.write(decodedContent)
    print("Done Successfully")
  
def rmadd():

    currdir=os.getcwd()
    fpath=f"{currdir}/.VCS/branches/main/added.json"
    with open(fpath, 'w') as file:
           file.write("")

    print("Done successfully")

        

if len(sys.argv) > 1:
    command = sys.argv[1]
    
    match command:
        case "init":
            init()
        case "add":
            add()
        case "status":
            status()
        case "commit":
            commit()
        case "rmcommit":
            rmcommit()
        case "log":
            log()
        case "checkout":
            checkout()
        case "push":
            push()
        case "rmadd":
            rmadd()
        case _:
            help_message = """
            VCS - A Version Control System
            
            VCS init - Initialize a new VCS repository
            
            VCS add <file> - Add a file to the index
            
            VCS commit -m <message> - Commit changes with a message
            
            VCS rmadd <file> - Remove a file from the index
            
            VCS rmcommit - Remove last commit
            
            VCS log - Display commit log
            
            VCS checkout <commit> - Checkout a specific commit
            
            VCS help - To see this usage help
            
            VCS status - To see status
            
            VCS user show - To see present user
            
            VCS user set <username> - To change user
            
            VCS push <path> - To push your file to another folder
            
            Created by - Jimi Patel
            """
            print(help_message)