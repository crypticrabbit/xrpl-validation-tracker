'''
Listen for messages in the queue, then dispatch them to connected websocket clients.
'''
import asyncio
import logging
import json
import time
import websockets

import settings_aggregator as settings

class WsServer:
    '''
    Websocket server.
    '''
    def __init__(self):
        self.clients = set()
        self.queue_send = None

    async def remove_client(self, client):
        '''
        Remove clients who are no longer connected from the self.clients set.

        :param client: Client that has disconnected
        '''
        logging.info(f"Client disconnected from WS server: {client}.")
        self.clients.remove(self, client)

    async def outgoing_server(self, websocket, path):
        '''
        Listen for messages in the outgoing queue, then dispatch
        them to connected clients.

        :param websocket: Websocket client connection
        '''
        try:
            self.clients.add(websocket)
            logging.info(f"A new user with IP: {websocket.remote_address[0]} connected to the WS server.")
            while True:
                outgoing_message = json.dumps(await self.queue_send.get())
                # The following (if self.clients) if statement might not be necessary.
                if self.clients:
                    for client in self.clients:
                        if client.open:
                            await client.send(outgoing_message)
        except (
                AttributeError,
                websockets.exceptions.ConnectionClosedError,
                ConnectionResetError,
        ) as error:
            logging.warning(f"Error with outgoing websocket server: {error}.")
            await self.remove_client(websocket)
        except (websockets.exceptions.ConnectionClosedOK) as error:
            logging.info(f"Websocket server connection closed: {error}")
            await self.remove_client(websocket)
        finally:
            await self.remove_client(websocket)

    async def start_outgoing_server(self, queue_send):
        '''
        Start listening for client connections.

        :param asyncio.queues.Queue queue_send: Queue for outgoing websocket messages
        '''
        self.queue_send = queue_send
        logging.info(f"Starting the websocket server on IP: {settings.SERVER_IP}:{settings.SERVER_PORT}.")
        await websockets.serve(self.outgoing_server, settings.SERVER_IP, settings.SERVER_PORT)

if __name__ == "__main__":
    START_SERVER = websockets.serve(
        WsServer.outgoing_server,
        settings.SERVER_IP,
        settings.SERVER_PORT
    )
    asyncio.get_event_loop().run_until_complete(START_SERVER)
    asyncio.get_event_loop().run_forever()
