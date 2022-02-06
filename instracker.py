#!/bin/python3
#https://github.com/andrea-varesio/instracker

'''Find and keep track of who unfollows you on Instagram'''

import argparse
import getpass
import datetime
import glob
import os
import pathlib
import sys
import time

from igramscraper.instagram import Instagram

now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def show_license():
    '''Show License'''

    print('\n**************************************************')
    print('"Instracker: Instagram unfollowers finder/tracker"')
    print('Find and keep track of who unfollows you on Instagram.')
    print('Copyright (C) 2022 Andrea Varesio (https://www.andreavaresio.com/).')
    print('This program comes with ABSOLUTELY NO WARRANTY')
    print('This is free software, and you are welcome to redistribute it under certain conditions')
    print('Full license available at https://github.com/andrea-varesio/instracker')
    print('**************************************************\n\n')

def parse_arguments():
    '''Parse arguments'''

    arg_parser = argparse.ArgumentParser()
    pass_group = arg_parser.add_mutually_exclusive_group()

    arg_parser.add_argument('-u', '--username', help='Your username', type=str)
    pass_group.add_argument('-p', '--password', help='Your password', type=str)
    pass_group.add_argument('--password-file', help='Read the password from a file', type=str)
    arg_parser.add_argument('-t', '--target', help='Username of the account to analyze', type=str)
    arg_parser.add_argument('--save-cookie', help='Save a session cookie', action='store_true')
    arg_parser.add_argument('-q', '--quiet', help='Disable verbosity', action='store_true')
    arg_parser.add_argument('-o', '--output', help='Specify output directory', type=str)

    return arg_parser.parse_args()

def print_exit(print_text, exit_status = None):
    '''Print text if args.quiet is None. If an exit status is provided, exit with status code'''

    args = parse_arguments()

    if not args.quiet:
        print(print_text)

    if exit_status:
        sys.exit(exit_status)

def get_target():
    '''Get target account username'''

    args = parse_arguments()

    if args.target:
        return args.target

    return args.username

def get_output_dir():
    '''Build output directory path from target account'''

    args = parse_arguments()
    target = get_target()

    if not args.output:
        return os.path.join(pathlib.Path.home(), f'Instracker_{target}_{now}')

    if os.path.isdir(args.output):
        return os.path.join(args.output, f'Instracker_{target}_{now}')

    return print_exit('Invalid output path', 1)

def get_credentials():
    '''Ask for the password it not provided, then attempt to login and return account info'''

    args = parse_arguments()
    instagram = Instagram()
    target = get_target()

    if not args.password and not args.password_file:
        password = getpass.getpass('Enter your password: ')
    elif args.password:
        password = args.password
        args.password = None
        del args.password
    elif os.path.isfile(args.password_file):
        with open(args.password_file, 'r', encoding='utf-8') as password_file:
            password = str(password_file.readlines()[0])
    else:
        print_exit('Invalid file', 1)

    instagram.with_credentials(args.username, password)
    instagram.login(force=False,two_step_verificator=False)

    password = None
    del password

    if not args.save_cookie:
        Instagram.instance_cache.empty_saved_cookies()

    account = instagram.get_account(target)

    return instagram, account

def get_followers(instagram, account):
    '''Save list of followers to followers_raw.txt then extract usernames to followers.txt'''

    print_exit('Fetching followers. This may take a while ...')

    followers = []
    followers = instagram.get_followers(account.identifier, 10000, 250, delayed=True)
    with open(os.path.join(get_output_dir(), 'followers_raw.txt'), 'a', encoding='utf-8') as f_raw:
        for follower in followers['accounts']:
            f_raw.write(str(follower))

    print_exit('Followers fetched')

    extract_list('followers')

def get_following(instagram, account):
    '''Save list of followers to following_raw.txt then extract usernames to following.txt'''

    print_exit('Fetching following users. This may take a while ...')

    following = []
    following = instagram.get_following(account.identifier, 10000, 250, delayed=True)
    with open(os.path.join(get_output_dir(), 'following_raw.txt'), 'a', encoding='utf-8') as f_raw:
        for following_user in following['accounts']:
            f_raw.write(str(following_user))

    print_exit('Following users fetched')

    extract_list('following')

def extract_list(filename):
    '''Take a file and extract the usernames to another file'''

    output_dir = get_output_dir()
    file_input = os.path.join(output_dir, f'{filename}_raw.txt')
    file_output = os.path.join(output_dir, f'{filename}.txt')
    query = 'Username: '

    with (
        open(file_input, 'r', encoding='utf-8') as file_input_data,
        open(file_output, 'a', encoding='utf-8') as file_output_data
    ):
        for line in file_input_data:
            if query in line:
                file_output_data.write(line.split(query)[1])

def get_not_following_back():
    '''Save list of people not following back to not_following_back.txt'''

    output_dir = get_output_dir()

    with (
        open(os.path.join(output_dir, 'followers.txt'), 'r', encoding='utf-8') as followers,
        open(os.path.join(output_dir, 'following.txt'), 'r', encoding='utf-8') as following,
        open(os.path.join(output_dir, 'not_following_back.txt'), 'a', encoding='utf-8') as nfb
    ):
        for user in set(following).difference(followers):
            nfb.write(user)

def get_new_unfollowers():
    '''Find new unfollowers if a previous file exists and save list to new_unfollowers.txt'''

    output_dir = get_output_dir()

    def find(filename, path):
        for root, dirs, files in os.walk(path):
            del dirs
            if filename in files and root != output_dir:
                yield root

    target = get_target()
    root_dir = os.path.join(pathlib.Path(output_dir).parent, f'Instracker_{target}_')
    dirlist = []
    for result in glob.iglob(f'{root_dir}*'):
        if os.path.isdir(result):
            for dirname in find('not_following_back.txt', result):
                dirlist.append(int(dirname.split(f'{root_dir}')[1]))

    if dirlist:
        old_nfb_path = os.path.join(f'{root_dir}{max(dirlist)}','not_following_back.txt')
        nfb_path = os.path.join(output_dir, 'not_following_back.txt')
        new_unfollowers_path = os.path.join(output_dir, 'new_unfollowers.txt')
        with (
            open(old_nfb_path,'r', encoding='utf-8') as old_nfb,
            open(nfb_path, 'r', encoding='utf-8') as nfb,
            open(new_unfollowers_path, 'a', encoding='utf-8') as new_unfollowers
        ):
            for item in set(nfb).difference(old_nfb):
                new_unfollowers.write(item)

def main():
    '''Main function'''

    args = parse_arguments()
    output_dir = get_output_dir()

    if not args.username:
        print_exit('Missing username', 1)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    if not args.quiet:
        show_license()

    instagram, account = get_credentials()

    get_followers(instagram, account)
    time.sleep(2)
    get_following(instagram, account)

    get_not_following_back()
    get_new_unfollowers()

    if not args.quiet:
        print('Finished')
        print('All the files are available in the following directory:')
        print(output_dir)

if __name__ == '__main__':
    main()
