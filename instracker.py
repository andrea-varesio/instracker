#!/bin/python3
#https://github.com/andrea-varesio/instagram-unfollowers-finder-tracker

import argparse
import getpass
import glob
import os
import sys
from datetime import datetime
from time import sleep

from igramscraper.instagram import Instagram


def show_license():
    print('\n**************************************************')
    print('"Instracker: Instagram unfollowers finder/tracker" - Find and keep track of who unfollows you on Instagram.')
    print('Copyright (C) 2022 Andrea Varesio (https://www.andreavaresio.com/).')
    print('This program comes with ABSOLUTELY NO WARRANTY')
    print('This is free software, and you are welcome to redistribute it under certain conditions')
    print('Full license available at https://github.com/andrea-varesio/instracker')
    print('**************************************************\n\n')

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
    with open(file_input, 'r') as file_input, open(file_output, 'a') as file_output:
        for line in file_input:
            if query in line:
                file_output.write(line.split(query)[1])

def join_path(file):
    return os.path.join(export_dir, file)

def find(filename, path):
    for root, dirs, files in os.walk(path):
        if filename in files:
            yield root

args = parser()
instagram = Instagram()

show_license()

if args.username is not None:
    username = args.username
else:
    username = input('Enter your username: ')

if args.password is None and args.password_file is None:
    password = getpass.getpass('Enter your password: ')
elif args.password is not None:
    password = args.password
    args.password = None
    del args.password
elif os.path.isfile(args.password_file):
    with open(args.password_file,'r') as f:
        password = str(f.readlines()[0])
else:
    if not args.quiet:
        print('Invalid file')
    sys.exit(1)

if args.self:
    target = username
elif args.target is not None:
    target = args.target
else:
    target = input(f'Enter the username of the account to analyze (leave blank for {username}): ')
    if not target:
        target = username

instagram.with_credentials(username, password)
instagram.login(force=False,two_step_verificator=False)

password = None
del password

if not args.save_cookie:
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

if not args.quiet:
    print('Fetching followers. This may take a while ...')
followers = []
sleep(1)
followers = instagram.get_followers(account.identifier, 10000, 250, delayed=True)
with open(join_path('followers_raw.txt'), 'a') as followers_raw:
    for follower in followers['accounts']:
        followers_raw.write(str(follower))
if not args.quiet:
    print('Followers fetched')
splitter(join_path('followers_raw.txt'), join_path('followers.txt'), 'Username: ')

sleep(2)

if not args.quiet:
    print('Fetching following users. This may take a while ...')
following = []
sleep(1)
following = instagram.get_following(account.identifier, 10000, 250, delayed=True)
with open(join_path('following_raw.txt'), 'a') as following_raw:
    for following_user in following['accounts']:
        following_raw.write(str(following_user))
if not args.quiet:
    print('Following users fetched')
splitter(join_path('following_raw.txt'), join_path('following.txt'), 'Username: ')

with open(join_path('followers.txt'), 'r') as followers, open(join_path('following.txt'), 'r') as following, open(join_path('not_following_back.txt'), 'a') as not_following_back:
    for item in set(following).difference(followers):
        not_following_back.write(item)

if dirlist:
    with open(os.path.join(f'{target}_{max(dirlist)}', 'not_following_back.txt'), 'r') as old_not_following_back, open(join_path('not_following_back.txt'), 'r') as not_following_back, open(join_path('new_unfollowers.txt'), 'a') as new_unfollowers:
        for item in set(not_following_back).difference(old_not_following_back):
            new_unfollowers.write(item)

if not args.quiet:
    print('Finished')
    print('All the files are available in the following directory:')
    print(os.path.join(os.getcwd(),export_dir))

sys.exit(0)
