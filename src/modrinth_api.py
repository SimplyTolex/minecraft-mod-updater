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
import json
import internal_vars as internal

input_url = "https://modrinth.com/mod/midnightcontrols"
headers = {
    'user-agent': f'github.com/SimplyTolex/minecraft-mod-updater {internal.version} (Open an issue or discussion if something went wrong)'}
testmod = "midnightcontrols"
data = []


def send_request(url, payload):
    # TODO: make an additional check that the loader and game versions are *actually* correct
    # params=payload makes from "game_versions": ["1.18.2"] -> "game_versions": "1.18.2" which apparantly makes queries to not work.

    r = requests.get(url, params=payload, headers=headers, timeout=7)
    print(f"MR | Sending request to: {r.url}")
    r.raise_for_status()
    print(r.json())
    # return r.json()
    # parse_versions(r.json)


def modrinth_search(input_url):
    ripped_mod_slug = "midnightcontrols"
    url = "https://api.modrinth.com/v2/search"

    payload = {"query": ripped_mod_slug, "limit": 1}

    send_request(url, payload)


def modrinth_get_versions(mod_id):
    url = f"https://api.modrinth.com/v2/project/{mod_id}/version"

    payload = {"loaders": ["fabric"], "game_versions": ["1.18.2"]}
    # payload = json.dumps(payload, separators=(",", "="))
    print(payload)
    # url = f'{url}?loaders={payload["loaders"]}&game_versions={payload["game_versions"]}'
    send_request(url, payload)
    # print(url)


def parse_versions(r):
    # data = data
    # data = json.loads(r)
    # print(data)
    pass


if __name__ == "__main__":
    print("MR | `modrinth_api.py` is not supposed to be run like that! Execute `gui.py` instead!")

