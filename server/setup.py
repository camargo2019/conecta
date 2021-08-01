#!/usr/bin/python3

import asyncio
import websockets
import json
import requests

clients = {}

async def list_server(websocket, path):
        jsondecod = await websocket.recv()
        inf = json.loads(jsondecod)
        try:
            id = inf["id_to"]
        except:
            id = inf["id_send"]
        clients[websocket] = id
        if(inf["type"] == "search"):
            returna = list_mensagem(inf)
        elif(inf["type"] == "C"):
            returna = insert_db(inf)
        else:
            returna = insert_db(inf)
        for client, _ in clients.items():
            await client.send(str(returna))

        while True:
            message = await websocket.recv()
            inf = json.loads(message)
            try:
                id = inf["id_to"]
            except:
                id = inf["id_send"]
            clients[websocket] = id
            if (inf["type"] == "search"):
                returna = list_mensagem(inf)
            elif (inf["type"] == "C"):
                returna = insert_db(inf)
            else:
                returna = insert_db(inf)
            if message is None:
                their_name = clients[websocket]
                del clients[websocket]
                break

            # Send message to all clients
            for client, _ in clients.items():
                await client.send(str(returna))

def insert_db(JsonDecodeRecebimento):
    url_send = "http://34.95.239.34:8080/api/chat/message"
    valueSend = json.dumps({
        'employee_id_from': JsonDecodeRecebimento["id_from"],
        'employee_id_to': JsonDecodeRecebimento["id_send"],
        'type': JsonDecodeRecebimento["type"],
        'description': JsonDecodeRecebimento["msg"]
    })
    x = requests.post(url_send, data=valueSend)
    jsonLoadRequests = json.loads(x.text)
    if(jsonLoadRequests["status"]["result"] == "success"):
        returnInfoSocket = json.dumps({'returnInfo': 'success'})
    else:
        returnInfoSocket = json.dumps({'returnInfo': 'error'})
    #print(x.text)
    return returnInfoSocket

def list_mensagem(JsonDecodeRecebimento):
    url_send = "http://34.95.239.34:8080/api/chat/message/list?employee_id_from="+str(JsonDecodeRecebimento["id_from"])+"&employee_id_to="+str(JsonDecodeRecebimento["id_to"])+"&offset=0&limit="+str(JsonDecodeRecebimento["limit"])
    x = requests.get(url_send)
    jsonLoadRequests = json.loads(x.text)
    if(jsonLoadRequests["status"]["result"] == "success"):
        returnInfoSocket = jsonLoadRequests["messages"]
    else:
        returnInfoSocket = "Error"
    #print(x.text)
    return returnInfoSocket

start_server = websockets.serve(list_server, "", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()