import json

path = r'data\devices.json'

def add_device(device, ip):
    with open(path, encoding='utf-8') as f:
        try:
            devices = json.load(f)
            devices[device] = (ip, '💤', None)
        except Exception as e:
            devices = {device: (ip, '💤', None)}
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(devices, f, ensure_ascii=False)
        
def update_all_status(status=0):
    emoji = ('💤', '✅', '❌')[status]
    with open(path, encoding='utf-8') as f:
        try:
            devices = json.load(f)
            for device, data in devices.items():
                devices[device] = (data[0], emoji, data[2])
                
        except:
            devices = dict()
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(devices,f, ensure_ascii=False)
        
def update_status(device, status=1, find_by_user=False, set_user=False):
    emoji = ('💤', '✅', '❌')[status]
    user = False if status in (0,1) else set_user
    
    with open(path, encoding='utf-8') as f:
        devices = json.load(f)
        
        if find_by_user:
            for _device in devices:
                if user in devices[_device]:
                    devices[_device] = (devices[_device][0], emoji, user)
                    break
                    
        else:
            devices[device] = (devices[device][0], emoji, user)
        
    with open(path, 'w', encoding='utf-8') as f:
        
        json.dump(devices, f, ensure_ascii=False)
        
def get_device_ip(device):
    with open(path, encoding='utf-8') as f:
        try:
            ip = json.load(f)[device][0]
        except:
            return 'None'
        
    return ip
    
def get_ip_devices():
    with open(path, encoding='utf-8') as f:
        try:
            devices = json.load(f)
            ip_devices = {value[0]: key for key, value in devices.items()}
        except:
            ip_devices = dict()
        
    return ip_devices
        
def get_devices(ip=False, keys=False):
    with open(path, encoding='utf-8') as f:
        try:
            if ip:
                devices = [i[0] for i in json.load(f).values()]
            else:
                if keys:
                    devices = list(json.load(f))
                else:
                    devices = [key + ' ' + value[1] for key, value in json.load(f).items()]
        except Exception as e:
            devices = []
        
    return devices + ['Назад ⬅️']
    
def get_device(device, _id=False):
    with open(path, encoding='utf-8') as f:
        devices = json.load(f)
        if _id:
            for _device in devices:
                if _id in devices[_device]:
                    return devices[_device]
                    
        else: 
            return devices[device]
    
def check_device_ip(deviceip):
    if ':' in deviceip:
        deviceip = deviceip.split(':')
        if len(deviceip) == 2 and deviceip[0] != '':
            deviceip = deviceip[1].split('.')
            if len(deviceip) == 4:
                for i in deviceip:
                    if i == '':
                        return 'Должно быть 4 числа от 0 до 255 перечисленные через точку. Посмотрите пример'
                    if 0 > int(i) or int(i) > 255:
                        return f'Числа должны быть в диапозоне от 0 до 255. Посмотрите пример'
                return True
            return 'Должно быть 4 числа от 0 до 255 перечисленные через точку. Посмотрите пример'
        return 'Неправильный формат данных. У вас присутствует лишнее ":" или название пустое. Посмотрите пример'
    return 'У вас отсутствует ":". Посмотрите пример'