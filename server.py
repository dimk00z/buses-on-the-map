import trio
import json
from trio_websocket import serve_websocket, ConnectionClosed
from functools import partial

import logging

logging.basicConfig(level=logging.INFO)
buses = {}
logger = logging.getLogger(__name__)


async def talk_to_browser(request):
    logger.info('talk_to_browser is runnig')
    ws = await request.accept()
    while True:
        try:
            result = []
            for bus_id, bus_info in buses.items():
                lat = bus_info['lat']
                lng = bus_info['lng']
                route = bus_info['route']
                result.append(
                    {
                        'busId': bus_id,
                        'lat': lat,
                        'lng': lng,
                        'route': route
                    }
                )
            message = {
                'msgType': 'Buses',
                'buses': result}
            # logger.info(message)
            await ws.send_message(json.dumps(message))
            await trio.sleep(1)
            # logger.info('talk_to_browser is still runnig')
            # await trio.sleep(1)

        except ConnectionClosed:
            break


async def update_buses(request):
    logger.info('update_buses is runnig')
    global buses
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            current_bus_info = json.loads(message)

            # logging.info(current_bus_info)

            buses[current_bus_info['busId']] = current_bus_info

        except ConnectionClosed:
            break


async def main():
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    update_buses_callback = partial(
        serve_websocket,
        handler=update_buses,
        host='127.0.0.1',
        port=8080,
        ssl_context=None
    )
    talk_to_browser_callback = partial(
        serve_websocket,
        handler=talk_to_browser,
        host='127.0.0.1',
        port=8000,
        ssl_context=None
    )
    async with trio.open_nursery() as nursery:
        logger.info('Server start')
        nursery.start_soon(update_buses_callback)
        nursery.start_soon(talk_to_browser_callback)


trio.run(main)
