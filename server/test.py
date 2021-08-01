import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:5000"
    async with websockets.connect(uri) as websocket:
        id = input("Qual seu ID? ")
        idfrom = input("Você quer enviar para: (ID) ")
        mensagem = input("Sua mensagem: ")
        jsonEncodeString = json.dumps({'id_send': id, 'id_from': idfrom, 'msg': mensagem, 'type': 'C'})
        await websocket.send(jsonEncodeString)
        resposta = await websocket.recv()
        print(f"{resposta}")

async def test2():
    uri = "ws://localhost:5000"
    async with websockets.connect(uri) as websocket:
        id = input("Qual o seu ID? ")
        idfrom = input("De quem você quer ver? (ID) ")
        quantasMensagens = int(input('Quantas mensagens? '))
        jsonEncodeString = json.dumps({'id_from': idfrom, 'id_to': id, 'limit': quantasMensagens, 'type': 'search'})
        await websocket.send(jsonEncodeString)
        resposta = await websocket.recv()
        print(f"{resposta}")

while True:
    type = input('Enviar ou Puxar Mensagens? (1/2) ')
    if(type == '1'):
        asyncio.get_event_loop().run_until_complete(test())
    elif(type == '2'):
        asyncio.get_event_loop().run_until_complete(test2())
    else:
        print('Selecione a opção correta!')