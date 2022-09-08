# minecraft-mod-updater -- Check updates for Minecraft mods and optionally update them.
# Copyright (C) 2022  SimplyTolex
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from github import Github

headers = {'accept': 'application/vnd.github+json'}

username = "SimplyTolex"     # TODO: set up username in settings to use github
# password = ""              # TODO: how do you even store passwords in files like these?
g = Github(username)


def parse_response(response):
    try:
        print("GH | version_name: " + response[0]["name"])
        return response[0]["name"]
    except IndexError:
        print("GH | IndexError! Does the repo exists? Does the repo containes any *releases*?")
        print("GH | Expected a list with a \"name\" in the object 0 but got this instead:")
        print(response)


def send_request(url, payload):
    if username == None or username == "":
        raise Exception("Add your username in preferences to use Github API")
    else:
        r = requests.get(url, params=payload, headers=headers, timeout=10)
        print(f"GH | Sending request to: {r.url}")
        r.raise_for_status()
        print(r.json())

        return parse_response(r.json())


def check_releases(owner, repo):
    """
    Sends a request to the API to check for *releases* of a certain repository, then return the name of the latest release.
    NOTE: It will not check for tags, use `check_tags` (which I didn't wrote yet) for that instead.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    payload = {"per_page": 1}

    return send_request(url, payload)


if __name__ == "__main__":
    print("GH | `github_api.py` is not supposed to be run like that! Execute `gui.py` instead!")
