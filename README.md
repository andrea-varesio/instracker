# ⚠️ WARNING ⚠️

Since the [instagram_scraper](https://github.com/realsirjoe/instagram-scraper) dependency is no longer being developed, this repository will be archived.

# Instracker: Instagram unfollowers finder/tracker

## What is it
It's a tool that fetches "following" and "followers" and then finds and keeps track of the usernames of the accounts that are not following you back and the new unfollowers.

## Requirements
`pip install -r requirements.txt`

## How to use it
Launch `instracker.py` (ie. `python3 instracker.py -u USERNAME`), then login with your credentials to find / track new unfollowers.

Note that `-u USERNAME` is required. If you want to specify a different target account, you can pass `-t TARGET` in addition to your username.

The script will generate a folder in your `$HOME` directory (unless you specify another path with `-o OUTPUT`) that contains the raw and cleaned lists as well as `not_following_back.txt` and `new_unfollowers.txt`.

Usage:
```
instracker.py [-h] [-u USERNAME] [-p PASSWORD | --password-file PASSWORD_FILE] [-t TARGET] [--save-cookie] [-q] [-o OUTPUT] [-kr] [-kc]
```

Short | Argument | Info
---|---|---
`-h` | `--help` | show this help message and exit
`-u USERNAME` | `--username USERNAME` | Your username
`-p PASSWORD` | `--password PASSWORD` | Your password
/ | `--password-file /PATH/TO/FILE` | Read the password from a file
`-t TARGET` | `--target TARGET` | Username of the account to analyze
/ | `--save-cookie` | Save a session cookie
`-q` | `--quiet` | Disable verbosity
`-o OUTPUT` | `--output OUTPUT` | Specify output directory
`-kr` | `--keep-raw` | Keep raw files
`-kc` | `--keep-clean` | Keep clean files

## Limits
This script fetches up to 10000 followers (and up to 10000 following), 250 at a time with a random delay between each request. These limits can be edited and the delay can be removed, but beware that, as indicated [upstream](https://github.com/realsirjoe/instagram-scraper), too many requests within a short period of time will result in a 429 error.

## Contributions
Contributions are welcome, feel free to submit issues and/or pull requests.

### To-Do
- Allow authentication with 2FA enabled (see known issues).
- Associate usernames with user IDs for better filtering.
- Figure out how to use the cookie (if saved).

### Known issues
- Login with 2FA enabled doesn't seem to be working, there are several open issues [upstream](https://github.com/realsirjoe/instagram-scraper/issues?q=is%3Aissue+InstagramAuthException). The only way for now seems to be to temporarily disable 2FA on your Instagram account. Alternatively, if you don't want to disable 2FA on your account, you could create another account that you will use for login, and target your actual account with the following command (note that in order for this to work, your main account must be set to 'Public'):
```
python3 instracker.py -u new_account -t main_account
```
Otherwise you can try switching `two_step_verificator=False` to `True`.

## Credits
This tool uses [instagram_scraper](https://github.com/realsirjoe/instagram-scraper) to fetch the lists of followers and following.

## LICENSE

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

"Instracker: Instagram unfollowers finder/tracker" - Find and keep track of who unfollows you on Instagram.<br />
Copyright (C) 2022 Andrea Varesio <https://www.andreavaresio.com/>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a [copy of the GNU General Public License](https://github.com/andrea-varesio/instracker/blob/main/LICENSE)
along with this program.  If not, see <https://www.gnu.org/licenses/>.

<div align="center">
<a href="https://github.com/andrea-varesio/instracker/">
  <img src="http://hits.dwyl.com/andrea-varesio/instracker.svg?style=flat-square" alt="Hit count" />
</a>
</div>
