"""Make a file organizer using os, shutil and sys modules in python which has the following functionalities:
● User inputs the directory path in which he/she wants to organize files.
● Create subdirectories for files with different extensions and organize it as per file
extensions."""

#solution
import os 
import shutil

Fpath=input("Please enter the folder path\n")

os.chdir(Fpath)

DFE = set()

Files=os.listdir(Fpath)

for file in Files:
    file_extension = os.path.splitext(file)[1]
    temp = file_extension[1:]
    if(temp==''): continue
    DFE.add(temp)

for x in DFE:
    if(os.path.exists(f"{Fpath}/{x}")):continue
    os.mkdir(x)

for file in Files:
    file_extension = os.path.splitext(file)[1]
    temp = file_extension[1:]
    if(temp==''): continue
    shutil.move(f"{Fpath}/{file}", f"{Fpath}/{temp}")

print("Successfully organize files in a given folder based on their extensions.")