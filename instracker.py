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
import glob
import os
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

def splitter(file_input, file_output, query):
    with open(file_input, 'r') as file:
        for line in file:
            if query in line:
                f = open(file_output, 'a')
                f.write(line.split(query)[1])
                f.close()

def join_path(file):
    return os.path.join(export_dir, file)

def find(filename, path):
  for root, dirs, files in os.walk(path):
    if filename in files:
      yield root

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

dirlist = []
for result in glob.iglob(f'{target}_*'):
    if os.path.isdir(result):
        for dirname in find('not_following_back.txt', result):
            dirlist.append(int(dirname.split(f'{target}_')[1]))

now = datetime.now()
export_dir = (target + now.strftime('_%Y%m%d%H%M%S'))
os.mkdir(export_dir)

sleep(2)

account = instagram.get_account(target)

if args.quiet == False:
    print('Fetching followers. This may take a while ...')
followers = []
sleep(1)
followers = instagram.get_followers(account.identifier, 10000, 250, delayed=True)
for follower in followers['accounts']:
    f = open(join_path('followers_raw.txt'), 'a')
    f.write(str(follower))
    f.close()
if args.quiet == False:
    print('Followers fetched')
splitter(join_path('followers_raw.txt'), join_path('followers.txt'), 'Username: ')

sleep(2)

if args.quiet == False:
    print('Fetching following users. This may take a while ...')
following = []
sleep(1)
following = instagram.get_following(account.identifier, 10000, 250, delayed=True)
for following_user in following['accounts']:
    f = open(join_path('following_raw.txt'), 'a')
    f.write(str(following_user))
    f.close()
if args.quiet == False:
    print('Following users fetched')
splitter(join_path('following_raw.txt'), join_path('following.txt'), 'Username: ')

with open(join_path('followers.txt'), "r") as followers:
    with open(join_path('following.txt'), "r") as following:
        for item in set(following).difference(followers):
            f = open(join_path('not_following_back.txt'), 'a')
            f.write(item)
            f.close()

if dirlist:
    with open(os.path.join(f'{target}_{max(dirlist)}', 'not_following_back.txt'), "r") as old_unfollowers:
        with open(join_path('not_following_back.txt'), "r") as new_unfollowers:
            for item in set(new_unfollowers).difference(old_unfollowers):
                f = open(join_path('new_unfollowers.txt'), 'a')
                f.write(item)
                f.close()

if args.quiet == False:
    print('Finished')
    print('All the files are available in the following directory:')
    print(os.path.join(os.getcwd(),export_dir))

sys.exit(0)
