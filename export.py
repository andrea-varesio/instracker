#!/bin/python3
#https://github.com/andrea-varesio/instagram-unfollowers-finder-tracker

print('\n**************************************************')
print('"Instracker: Instagram unfollowers finder/tracker" - Find and keep track of who unfollows you on Instagram.')
print('Copyright (C) 2022 Andrea Varesio (https://www.andreavaresio.com/).')
print('This program comes with ABSOLUTELY NO WARRANTY')
print('This is free software, and you are welcome to redistribute it under certain conditions')
print('Full license available at https://github.com/andrea-varesio/instracker')
print('**************************************************\n\n')

import argparse
import getpass
import os
import subprocess
import sys
from datetime import datetime
from igramscraper.instagram import Instagram
from time import sleep

def parser():
    parser = argparse.ArgumentParser()
    passgroup = parser.add_mutually_exclusive_group()
    targetgroup = parser.add_mutually_exclusive_group()
    parser.add_argument('-u', '--username', help='Your username', type=str)
    passgroup.add_argument('-p', '--password', help='Your password', type=str)
    passgroup.add_argument('--password-file', help='Read the password from a file', type=str)
    targetgroup.add_argument('-t', '--target', help='Username of the account to analyze', type=str)
    targetgroup.add_argument('-s', '--self', help='Analyze your own account', action='store_true')
    parser.add_argument('-q', '--quiet', help='Disable the majority of prompts and verbosity', action='store_true')
    parser.add_argument('--save-cookie', help='Save a session cookie', action='store_true')
    return parser.parse_args()

args = parser()
instagram = Instagram()

if args.username != None:
    username = args.username
else:
    username = input('Enter your username: ')

if args.password == None and args.password_file == None:
    password = getpass.getpass('Enter your password: ')
elif args.password != None:
    password = args.password
elif os.path.isfile(args.password_file):
    f = open(args.password_file,'r')
    password = str(f.readlines()[0])
    f.close()
else:
    if args.quiet == False:
        print('Invalid file')
    sys.exit(1)

if args.self:
    target = username
elif args.target != None:
    target = args.target
else:
    target = input(f'Enter the username of the account to analyze (leave blank for {username}): ')
    if not target:
        target = username

instagram.with_credentials(username, password)
instagram.login(force=False,two_step_verificator=False)

password = None; del password

if args.save_cookie == False:
    Instagram.instance_cache.empty_saved_cookies()

now = datetime.now()
exportDir = (target + now.strftime('_%Y%m%d%H%M%S'))
os.mkdir(exportDir)

sleep(2)

account = instagram.get_account(target)

if args.quiet == False:
    print('Fetching followers. This may take a while ...')
followers = []
sleep(1)
followers = instagram.get_followers(account.identifier, 10000, 250, delayed=True)
for follower in followers['accounts']:
    f = open(os.path.join(exportDir, 'followers_raw.txt'), 'a')
    f.write(str(follower))
    f.close()
if args.quiet == False:
    print('Followers fetched')

sleep(2)

if args.quiet == False:
    print('Fetching following users. This may take a while ...')
following = []
sleep(1)
following = instagram.get_following(account.identifier, 10000, 250, delayed=True)
for following_user in following['accounts']:
    f = open(os.path.join(exportDir, 'following_raw.txt'), 'a')
    f.write(str(following_user))
    f.close()
if args.quiet == False:
    print('Following users fetched')

f = open('var.tmp', 'w')
f.write('export exportDir=' + exportDir)
f.close()

subprocess.run(
    '''
        source var.tmp
        grep "Username: " ${exportDir}/following_raw.txt | sed 's/Username: //g' >> ${exportDir}/following.txt
        grep "Username: " ${exportDir}/followers_raw.txt | sed 's/Username: //g' >> ${exportDir}/followers.txt
        grep -xivFf  ${exportDir}/followers.txt ${exportDir}/following.txt > ${exportDir}/not_following_back.txt
    ''',
    shell=True, check=True,
    executable='/bin/bash')

os.remove('var.tmp')

if args.quiet == False:
    print('Finished')
    print('All the files are available in the following directory:')
    print(os.path.join(os.getcwd(),exportDir))

sys.exit(0)
