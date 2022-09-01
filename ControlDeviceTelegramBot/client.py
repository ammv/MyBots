import socket
from time import sleep


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUFFER = 4096

def ping():
    print('[CLIENT][COMMAND] Get ping')
    sock.send(b'pong')
    print('[CLIENT][COMMAND] send pong')

actions = {b'ping': ping}

def run():
    while True:
        sleep(1)
        data = sock.recv(BUFFER)
        if data == b'1':
            sock.send(b'2')
         
        elif data in actions:
            actions[data]()

while True:
    try:
        sock.connect(('localhost', 8888))
        print('[CLIENT] Успешно! Удалось подключиться к серверу.')
        run()
        
    except Exception as e:
        print('[CLIENT] Ошибка! Не удалось подключиться к серверу. Попробуйте позже')
        answer = input('q - выйти, enter - попробовать ещё раз')
        
        if answer == 'q':
            break
        
