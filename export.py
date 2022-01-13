#!/bin/python

#https://github.com/andrea-varesio/instagram-unfollowers-finder-tracker

print('\n**************************************************')
print('"Instracker: Instagram unfollowers finder/tracker" - Find and keep track of who unfollows you on Instagram.')
print('Copyright (C) 2022 Andrea Varesio (https://www.andreavaresio.com/).')
print('This program comes with ABSOLUTELY NO WARRANTY')
print('This is free software, and you are welcome to redistribute it under certain conditions')
print('Full license available at https://github.com/andrea-varesio/instracker')
print('**************************************************\n\n')

import sys
import os
import subprocess

from igramscraper.instagram import Instagram
from datetime import datetime
from time import sleep
import getpass

instagram = Instagram()

username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')
target = input('Enter the username of the account to analyze (leave blank for "' + username + '"): ')
if not target:
    target = username
saveCookie = input('Do you want to save a session cookie? y/n ')

instagram.with_credentials(username, password)
instagram.login(force=False,two_step_verificator=False)

password = None; del password
if saveCookie != 'y':
    Instagram.instance_cache.empty_saved_cookies()

now = datetime.now()
exportDir = ('Export_' + now.strftime('%Y%m%d%H%M%S'))
os.mkdir(exportDir)

sleep(2)

account = instagram.get_account(target)

print('Fetching followers. This may take a while ...')
followers = []
sleep(1)
followers = instagram.get_followers(account.identifier, 10000, 250, delayed=True)
for follower in followers['accounts']:
    f = open(os.path.join(exportDir, 'followers_raw.txt'), 'a')
    f.write(str(follower))
    f.close()
print('Followers fetched')

sleep(2)

print('Fetching following users. This may take a while ...')
following = []
sleep(1)
following = instagram.get_following(account.identifier, 10000, 250, delayed=True)
for following_user in following['accounts']:
    f = open(os.path.join(exportDir, 'following_raw.txt'), 'a')
    f.write(str(following_user))
    f.close()
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

print('Finished')
print('All the files are available in the following directory:')
print(os.path.join(os.getcwd(),exportDir))

sys.exit(0)
