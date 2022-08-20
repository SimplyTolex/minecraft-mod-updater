# minecraft-mod-updater -- TUI application to check updates for mods for Minecraft and an option to update them.
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

input_url = "https://modrinth.com/mod/midnightcontrols"
headers = {'user-agent': 'github.com/SimplyTolex/minecraft-mod-updater dev0.1 (Open an issue or discussion if something went wrong)'}
testmod = "midnightcontrols"


def send_request(url, payload):
    # TODO: make an additional check that the loader and game versions are *actually* correct
    # params=payload makes from "game_versions": ["1.18.2"] -> "game_versions": "1.18.2" which apparantly makes queries to not work.
    
    r = requests.get(url, params=payload, headers=headers, timeout=7)
    print(f"Sending request to: {r.url}")
    r.raise_for_status()
    return print(r.json())      # NOTE: will need to remove print() for return to work (otherwise it will return null)


def modrinth_search(input_url):
    ripped_mod_slug = "midnightcontrols"
    url = "https://api.modrinth.com/v2/search"
    
    payload = {"query": ripped_mod_slug, "limit": 1}

    send_request(url, payload)    


def modrinth_get_versions(mod_id):
    url = f"https://api.modrinth.com/v2/project/{mod_id}/version"
    
    payload = {"loaders": ["fabric"], "game_versions": ["1.18.2"]}

    send_request(url, payload)


# modrinth_search(input_url)
modrinth_get_versions(testmod)