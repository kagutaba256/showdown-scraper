"""
An example client that joins all OU battles
and saves replays.
"""
import showdown
from os import path
import logging

logging.basicConfig(filename='download.log',
                    level=logging.INFO)

with open('login.txt', 'rt') as f:
    username, password = f.read().strip().splitlines()

logging.info("started")


class ReplayClient(showdown.Client):
    async def on_query_response(self, response_type, data):
        if response_type == 'roomlist':
            for battle_id in set(data['rooms']) - set(self.rooms):
                await self.join(battle_id)

    async def on_receive(self, room_id, inp_type, params):
        if inp_type == 'win':
            if path.exists('/data/' + room_id):
                logging.info('/data/' + room_id + ' already exists')
            else:
                with open('/data/' + room_id, 'wt') as f:
                    f.write('\n'.join(self.rooms[room_id].logs))

    @showdown.Client.on_interval(interval=0.1)
    async def check_ou(self):
        await self.query_battles(battle_format='')


ReplayClient(name=username, password=password).start(autologin=False)
