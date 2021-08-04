import json
from sys import stderr
from itertools import cycle

import trio
from trio_websocket import open_websocket_url


def get_bus_info(bus_number):
    with open(f'routes/{bus_number}.json') as f:
        return json.loads(f.read())


async def main():
    bus_info = get_bus_info(156)
    while True:
        try:
            async with open_websocket_url('ws://127.0.0.1:8080') as ws:
                for lat, lon in cycle(bus_info['coordinates']):
                    message = {
                        'busId': 'c790cc',
                        'lat': lat,
                        'lon': lon,
                        'route': 156
                    }
                    print(message)
                    await ws.send_message(json.dumps(message))
                    await trio.sleep(1)
        except OSError as ose:
            print('Connection attempt failed: %s' % ose, file=stderr)


if __name__ == '__main__':
    trio.run(main)
