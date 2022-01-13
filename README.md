# Instracker: Instagram unfollowers finder/tracker

## What is it
It's a tool that fetches "following" and "followers" and then finds ~and keeps track of~ (soon&trade;) the usernames of the accounts that are not following you back.

## Requirements
`pip install igramscraper`

## How to use it
Launch `export.py` (ie. `python3 export.py`), then login with your credentials and type the username of the account for which you want to find / ~track~ (soon&trade;) unfollowers.

The script will generate an `Export_***` folder that contains the raw and cleaned lists as well as `not_following_back.txt`.

## Limits
This script fetches up to 10000 followers (and up to 10000 following), 250 at a time with a random delay between each request. These limits can be edited and the delay can be removed, but beware that, as indicated [upstream](https://github.com/realsirjoe/instagram-scraper), too many requests within a short period of time will result in a 429 error.

## Contributions
Contributions are welcome, feel free to submit issues and/or pull requests.

### To-Do
- Allow authentication with 2FA enabled (see known issues).
- Associate usernames with user IDs for better filtering when tracker is complete.
- Keep track of new unfollowers: keep generating `not_following_back.txt` but also create a `tracker.txt` in the root directory to keep track of new unfollowers.
- Explore alternative ways instead of running a bash subprocess for `grep` + `sed`.
- Figure out how to use the cookie (if saved).

### Known issues
- Login with 2FA enabled doesn't seem to be working, there are several open issues [upstream](https://github.com/realsirjoe/instagram-scraper/issues?q=is%3Aissue+InstagramAuthException). The only way for now seems to be to temporarily disable 2FA on your Instagram account. Otherwise you can try switching `two_step_verificator=False` to `True`.

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
