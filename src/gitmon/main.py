import sys
import os
import re
import requests
from pathlib import Path


def commits(url):
    
    r = requests.get(url)
    commitCount = re.findall('commitCount":"[0-9]+', r.text)
    count = re.findall("[0-9]+",commitCount[0])
    
    return count[0]

def add(url):
    
    user=str(Path.home())
    if not os.path.isdir(f'{user}/.gitmon'):
        os.makedirs(f'{user}/.gitmon')
    
    with open(f"{user}/.gitmon/data.txt", "a") as f:
        f.write(f'{url} {commits(url)}\n')

def check():
    
    user=str(Path.home())
    newdata=[]
    try:
        with open(f'{user}/.gitmon/data.txt', 'r') as file:
            for line in file:
                list=line.split(' ')
                url=list[0]
                prevcommits=list[1][:-1]
                newcommits=commits(url)
                diff= int(newcommits)-int(prevcommits)
                print(f'{diff} new commits on {url}')
                
                if diff==0:
                    newdata.append(line)
                    continue
                
                newdata.append(f'{url} {newcommits}\n')

           

    except OSError:
        print(f"Reading {user}/.gitmon/data.txt failed")
    

    try:
        with open(f'{user}/.gitmon/data.txt', 'w') as file:
            for line in newdata:
                file.write(line)

    except OSError:
        print(f"Writing to {user}/.gitmon/data.txt failed")

    return


def main():
    
    if len(sys.argv)>1:
        if sys.argv[1]=='add':
            add(sys.argv[2])
    else:
        check()
    
    return 0


if __name__ == "__main__":
    main()
