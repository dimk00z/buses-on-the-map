import json
from sys import stderr
from itertools import cycle
from load_routes import load_routes
from random import choice, randint
import trio
from trio_websocket import open_websocket_url


def generate_bus_id(route_id, bus_index):
    return f"{route_id}-{bus_index}"


async def run_bus(channel, route, bus_id):
    start_offset = randint(1, len(route['coordinates']))
    try:
        # bus_id = uuid4().hex
        # async with open_websocket_url(url) as ws:
        for lat, lng in cycle(route['coordinates'][start_offset:]):
            message = {
                # 'busId': route['name'],
                'busId': bus_id,
                'lat': lat,
                'lng': lng,
                'route': route['name']
            }
            # await ws.send_message(json.dumps(message, ensure_ascii=False))

            await channel.send(json.dumps(message, ensure_ascii=False))
            await trio.sleep(1)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


async def main():
    url = 'ws://127.0.0.1:8080'
    channels = [trio.open_memory_channel(0) for _ in range(10)]

    async with trio.open_nursery() as nursery:
        for bus_id, route in enumerate(load_routes()):
            nursery.start_soon(run_bus, url,  route)


if __name__ == '__main__':
    trio.run(main)
