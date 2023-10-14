import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Conectado ao servidor websocket na porta 3001')

@sio.on('disconnect')
def on_disconnect():
    print('Desconectado do websocket!')

@sio.on('message')
def on_event(data):
    print(f'Eventos do servidor: {data}')
    self.env['linhafala.asterisk'].handleEvent(data)



if __name__ == "__main__":
    server_url = "http://localhost:3001" 
    sio.connect(server_url)

    sio.wait() 
