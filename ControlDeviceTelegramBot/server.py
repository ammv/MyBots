import socket
import json

from threading import Thread
from time import sleep
from tg_bot.utils.utils import get_devices, update_status, get_ip_devices, get_device, update_all_status

class Server:
    def __init__(self, bot):
        self.ip = ''
        self.port = 8888
        self.bot = bot
                
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        
        self.BUFFER = 4096
        self.conns = dict()
        self.tasks = dict()
        self.ip_devices = dict()
        
        self.actions = {'ping': self.ping}
        
        self.update_addrs()
        update_all_status()
        
    async def send_text(self, chat_id, text):
        await self.bot.send_message(chat_id=chat_id, text=text)
        
    def update_addrs(self):
        def _update_addrs():
            while True:
                self.addrs = get_devices(True)[:-1]
                self.ip_devices = get_ip_devices()
                sleep(1)
        Thread(target=_update_addrs).start()
        
    def add_task(self, task):
        self.tasks[task['addr']] = (task['id'], task['task'])
        
    def ping(self, conn, addr):
        conn.send(b'ping')
        data = conn.recv(self.BUFFER).decode('utf-8')
        send_message(self.tasks[addr][0], data)
        
    def clock(self, addr):
        time = 0
        while not self.conns[addr][1]:
            time += 1
            if time == 5: #5sec timeout
                self.conns[addr][0] = False
                break
            sleep(1)
                
    def _update_status(self, addr):
        device = get_device(self.ip_devices[addr])
        if device[1] == '❌':
            self.send_text(device[2], 'Соеденение с устройством потеряно, вы перенесены в главное меню')
        update_status(self.ip_devices[addr], 0)
        
    def client(self, conn, addr):
        while self.conns[addr][0]:
            
            #keep alive
            conn.send(b'1')
            Thread(target=self.clock, args=(addr,)).start()
            data = conn.recv(self.BUFFER)
            
            if data == b'2':
                self.conns[addr][1] = True
            
            if addr in self.tasks:
                self.actions[tasks[addr][1]](conn, addr)
                del self.tasks[addr]
                
        del self.conns[addr]
        
        print('Соеденение разорвано: ' + addr )
               
        self._update_status(addr)
        
        conn.close()
                
    def get_tasks(self, conn):
        while True:
            data = conn.recv(self.BUFFER).decode('utf-8')
            self.add_task(json.loads(data))
        
    def run(self):
        Thread(target=self._run).start()
        
    def _run(self):
        print('[SERVER] Wait command sender...')
        command_sender = self.sock.accept()[0]
        Thread(target=self.get_tasks, args=(command_sender,)).start()
        print('[SERVER] Command sender connected...')
        
        print('[SERVER] Wait clients...')
        while True:
            conn, addr = self.sock.accept()
            addr = addr[0]
            print('This addres try connect:', addr)
            if addr in self.addrs:
                print('connected', addr)
                
                self.conns[addr] = [True, False]
                Thread(target=self.client, args=(conn, addr)).start()
                
                update_status(self.ip_devices[addr], 1)
            else:
                conn.close()