import trio
import json
from trio_websocket import serve_websocket, ConnectionClosed

from itertools import cycle


def load_bus_route(bus_number):
    with open(f'routes/{bus_number}.json') as bus_file:
        return json.loads(bus_file.read())


async def echo_server(request):
    ws = await request.accept()

    test_bus_info = load_bus_route(156)

    while True:
        try:
            message = await ws.get_message()
            print(message)
            # for lat, lng in cycle(test_bus_info['coordinates']):
            #     test_message = {
            #         'msgType': 'Buses',
            #         'buses': [{
            #             "busId": "c790сс",
            #             'lat': lat,
            #             'lng': lng,
            #             "route": test_bus_info['name']
            #         }]}
            #     await ws.send_message(json.dumps(test_message))
            #     await trio.sleep(1)

        except ConnectionClosed:
            break


async def main():
    await serve_websocket(echo_server, '127.0.0.1', 8080, ssl_context=None)

trio.run(main)
