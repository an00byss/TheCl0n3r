# by an00byss
# Made for pentesters and red teamers.

import argparse
import subprocess
import os
import shutil
import time
import datetime
import requests
from requests.exceptions import HTTPError

"""User Github API Key"""
api_key = "token " + "ADD-YOUR-GITHUB-API-KEY" # Replace API Token

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))

parser = argparse.ArgumentParser(description=prGreen("[*] TheCl0n3r will allow you to download and manage your git repositories.\n"))
parser.add_argument('-l', '--list', help='List all currently installed tools', action='store_true')
parser.add_argument('-d', '--download', help='Download git tools', action='store_true')
parser.add_argument('-a', '--add', metavar='Link', help='Add git tool, Provide a github link.', type=str)
parser.add_argument('-u', '--update', help='Update git tool, Specify "TOOL" or "all".', type=str)
parser.add_argument('-r', '--remove', metavar='Tool', help='Deletes git tools. "ALL" for all tools or "TOOL" to delete specified tool.', type=str)

""" File containing all of our tools"""
filename = "tool_list.txt"

"""Sets path of our tool"""
ourpath = os.path.dirname(os.path.abspath(__file__))


def list_tools():
    """Listing currently tools"""
    git_headers = {"User-Agent": "curl/7.68.0", "Accept": "*/*", "Authorization": api_key, "Connection": "close", "Accept-Encoding": "gzip, deflate"}
    
    try:
        list_num = 1
        tool_list = []
        with open(filename) as file_object:
            for line in file_object:
                tool = line.split('/')
                prYellow("[" + str(list_num) + "] " + tool[4].strip())
                tool_list.append(tool)
                tool_url = line.replace('https://github.com', 'https://api.github.com/repos')
                response = requests.get(tool_url.strip(), headers=git_headers)
                r_dict = response.json() # Captures json response and puts into dictionary
                if r_dict['description'] == None:
                    prPurple("[*] No description for this tool.")
                else:
                    prCyan("[*] " + r_dict['description']) # Prints 'updated at' key
                list_num += 1
    except FileNotFoundError:
        prRed("\n [*]Sorry tool list does not exist.")
    return tool_list


def add_tools(git_link):
    """Will add tool to our list"""
    tool = git_link.split("/")
    substring = '.git'
    
    if "https://github.com" not in git_link:
        prRed("\nPlease provide a github link")
    elif substring in git_link:
        git_link = git_link.replace(substring, "")
        prCyan("[*] " + tool[4].title() + " has been added to our tool list.")
        with open(filename, "a") as file_object:
                file_object.write(git_link + "\n")
    else:
        prCyan("[*] " + tool[4].title() + " has been added to our tool list.")
        with open(filename, "a") as file_object:
                file_object.write(git_link + "\n")


def download_tools():
    """Will download all tools in list"""
    try:
        prCyan("[*] Downloading tools... Please wait.")
        with open(filename) as file_object:
            for line in file_object:
                subprocess.run(["/usr/bin/git", "clone", line.strip()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
        prYellow("[*] All tools downloaded.")

    except FileNotFoundError:
        prRed("\n [*] Sorry tools list doesn't exist.")



def remove_tools(deleted_tools):
    """Will delete specified tool in list."""        
    if deleted_tools == "ALL":
        prCyan("[*] Making a backup of tool list.")
        shutil.copy(filename, filename + ".bak")
        
        with open(filename) as file_object:
            for line in file_object:
                tool_split = line.split('/')
                delete = tool_split[4]
                subprocess.Popen(["/usr/bin/rm", "-rf", ourpath + "/" + delete.strip()])
        
        with open(filename, 'w') as file_object:
            file_object.write("")
        prYellow("[*] All Tools have been deleted!")

    elif deleted_tools == deleted_tools:
        """ Delete's specified tool."""
        found = False

        """Will delete tool if found in file and remove installation."""
        with open(filename, 'r') as file_object:
            lines = file_object.readlines()
            for line in lines:
                tool_split = line.split('/')
                if deleted_tools.strip() == tool_split[4].strip():
                    found = True
                    prCyan("[*] Your tool was found... Deleting.")
                    with open(filename, 'w') as file_object:
                            for line in lines:
                                tool_split = line.split('/')
                                delete = tool_split[4]
                                if deleted_tools.strip() not in line.strip():
                                    file_object.write(line)
                                    subprocess.Popen(["/usr/bin/rm", "-rf", ourpath + "/" + deleted_tools.strip()])
                    prYellow("[*] " + deleted_tools + " has been removed.")
                    quit()
                else:
                    found = False
        
        if found == False:
            prRed("[*] Your tool " + deleted_tools + " was not found.")




def update_tools(update_choice):
    """Will update all installed it tools"""
    
    git_headers = {"User-Agent": "curl/7.68.0", "Accept": "*/*", "Authorization": api_key, "Connection": "close", "Accept-Encoding": "gzip, deflate"}

    
    type_update = input(" [*] Do you want to 'pull' or 'fresh' update: ")
    
    if update_choice != None:
        with open(filename) as file_object:
            prCyan("[*] Updating: " + update_choice + "\n")
            for line in file_object:
                tool_url = line.replace('https://github.com', 'https://api.github.com/repos')
                response = requests.get(tool_url.strip(), headers=git_headers)
                r_dict = response.json() # Captures json response and puts into dictionary
                tool = line.split('/')
                
                # If tool is found then update.
                if update_choice == "all" or update_choice == "All":
                    prYellow("[*] Newest Update for " + tool[4].strip() + ": " + r_dict['updated_at']) # Prints 'updated at' key
                    tool_last_updated = os.path.getmtime(ourpath + "/" + tool[4].strip() +"/.git/HEAD")
                    last_update = str(datetime.datetime.fromtimestamp(tool_last_updated))
                    prYellow("[*] " + tool[4].strip() + " was last updated: " + last_update + "\n")

                    # If fresh then it will delete current tool and re-download
                    if type_update == "Fresh" or type_update == "fresh":
                        if str(r_dict['updated_at']) >= last_update:
                            tool_split = line.split('/')
                            delete = tool_split[4]
                            subprocess.run(["/usr/bin/rm", "-rf", ourpath + "/" + delete.strip()])
                            with open(filename) as file_object:
                                for line in file_object:
                                    subprocess.run(["/usr/bin/git", "clone", line.strip()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
                                prCyan("[*] " + tool_split[4].strip() + " has been updated.\n")
                            
                        else:
                            prRed("[*] No new updates, Skipping...\n")
                    
                    # If 'pull' it will git a git pull
                    elif type_update == "pull" or type_update == "Pull":
                        tool_split = line.split('/')
                        delete = tool_split[4]
                        with open(filename) as file_object:
                            for line in file_object:
                                subprocess.run(["/usr/bin/git", "pull", line.strip()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
                            prCyan("[*] " + tool_split[4].strip() + " has been updated.\n")
                    else:
                        prRed("Not a recognized update type.")

                elif update_choice.strip() == tool[4].strip():
                    prYellow("[*] Newest Update for " + tool[4].strip() + ": " + r_dict['updated_at']) # Prints 'updated at' key
                    tool_last_updated = os.path.getmtime(ourpath + "/" + tool[4].strip() +"/.git/HEAD")
                    last_update = str(datetime.datetime.fromtimestamp(tool_last_updated))
                    prYellow("[*] " + tool[4].strip() + " was last updated: " + last_update + "\n")

                    if type_update == "Fresh" or type_update == "fresh":
                        if str(r_dict['updated_at']) >= last_update:
                            tool_split = line.split('/')
                            delete = update_choice.strip() # change the tool we are deleting to our choice
                            subprocess.run(["/usr/bin/rm", "-rf", ourpath + "/" + delete.strip()])
                            with open(filename) as file_object:
                                for line in file_object:
                                    subprocess.run(["/usr/bin/git", "clone", line.strip()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
                                prCyan("[*] " + tool_split[4].strip() + " has been updated.\n")
                                quit()
                        else:
                            prRed("[*] No new updates, Skipping...\n")
                            quit()
                    elif type_update == "pull" or type_update == "Pull":
                        tool_split = line.split('/')
                        delete = update_choice.strip() # change the tool we are deleting to our choice
                        with open(filename) as file_object:
                            for line in file_object:
                                subprocess.run(["/usr/bin/git", "pull", line.strip()], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
                            prCyan("[*] " + tool_split[4].strip() + " has been updated.\n")
                    else:
                        prRed("Not a recognized update type.")
                
                else:
                    prPurple("[*] Not the specified tool tool, skipping...")
                    
                    
    else:
        prRed("[*] Please choose 'All' or 'Tool'.")



def main():
    """Will take user input and perform action"""
    args = parser.parse_args()
    
    if args.list:
        list_tools()
    
    elif args.add:
        git_link = str(args.add).strip() 
        add_tools(git_link)
    
    elif args.download:
        download_tools()

    elif args.remove:
        deleted_tools = str(args.remove).strip()
        remove_tools(deleted_tools)
    
    elif args.update:
        update_choice = str(args.update).strip()
        update_tools(update_choice)


if __name__ == "__main__":
    main()