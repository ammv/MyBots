import configparser
import os.path
import json
import logging
import sys
import requests
import threading
import pyfiglet
import vk_api

from random import randint, shuffle
from time import sleep
from post_stack import PostStack
from group import Group
#from .private_group import PrivateGroup


def get_logger():
    logging.basicConfig(level=logging.INFO)
    # Create a custom logger
    logger = logging.getLogger('bot.py')
    
    # remove vk_api handler
    logging.getLogger().removeHandler(logging.getLogger().handlers[0])

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('bot_logs.log', mode='a')
    #c_handler.setLevel(logging.INFO)
    #f_handler.setLevel(logging.INFO)
    
    # Create formatters and add it to handlers
    c_format = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    f_format = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger
    
logger = get_logger()
    
    
class MinerBot:
    def __init__(self):
        self.bot_work = True
        self.vk_pointer = [None]
        
        self.load_config()
        self.load_groups()
        self.auth_vk()
        self.load_private_group_id()
       
    # Загружает данные из config.ini
    def load_config(self):
        logger.info('Загрузка конфигурации')
        
        self.config = config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        self.account = self.config['Account']
        self.groups_id_file_path = self.config['Data files']['groups_id_file']
        self.delays = {}
        
        for key, item in self.config['Delays'].items():
            self.delays[key] = int(item)
        
        logger.info(
            '\n' + 'Конфигурация'.center(50, '=') + '\n' +
            f'Логин: {self.account["login"]}\n' +
            f'Пароль: {self.account["password"]}\n' +
            f'{"="*50}\n')
            
    # Загружает ссылку на частную группу из config.ini
    def load_private_group_id(self):
        logger.info('Получение ID частной группы')
        private_group_id = self.get_group_id(self.config['Private group']['group'])
        if(not private_group_id):
            logger.error('Частная группа не была найдена: ' + self.config['Private group']['group'])
            input('Проверьте ссылку на частную группу в config.ini и запустите программу. Нажмите Enter чтобы закрыть:')
            self.bot_work = False
            sys.exit(1)
            
        self.private_group = Group(private_group_id, self.vk_pointer)
        
    # Авторизируется в ВК
    def auth_vk(self):
        logger.info('Вход в аккаунт')
        auth_again = True
        attemps = 0
        
        while auth_again:
            attemps += 1
            try:
                vk_session = vk_api.VkApi(login=self.account['login'], password=self.account['password'])
                #vk_session = vk_api.VkApi(app_id=51470678, client_secret='98cf370f98cf370f98cf370fd59bde5659998cf98cf370ffba515c6ab1961749c5ba492')
                vk_session.auth(token_only=True)
                
                self.vk = vk_session.get_api()
                self.vk_pointer[0] = self.vk
            
                logger.info('Успешный вход в аккаунт')
                break
                
            except vk_api.exceptions.BadPassword:
                logger.error('Неверный пароль')
                print('Чтобы выйти введите "q".')
                print('Чтобы продолжить попытки нажмите Enter.')
                action = input()
                if action.lower() == 'q':
                    sys.exit(1)
                else:
                    attemps = 0
                
            except requests.exceptions.ConnectionError as err: 
                logger.error(f'ConnectionError: {str(err)}')
                print('Проверьте интернет соеденение')
                print('Чтобы выйти введите "q".')
                print('Чтобы продолжить попытки нажмите Enter.')
                action = input()
                if action.lower() == 'q':
                    sys.exit(1)
                
            except Exception as err:
                logger.error(f'{err.__class__.__name__}: {str(err)}')
                if(attemps == 5):
                    print('Было совершено 5 неудачных попыток входа.')
                    print('Чтобы выйти введите "q".')
                    print('Чтобы продолжить попытки нажмите Enter.')
                    action = input()
                    if action.lower() == 'q':
                        sys.exit(1)
                    else:
                        attemps = 0
            finally:
                sleep(1)
                
    def extract_group_id(self, group):
        group = group.lower().strip()
        
        if r'https://vk.com/' in group:
            slice_len = 15
            
        elif r'vk.com/' in group:
            slice_len = 7
            
        else:
            return False
            
        return group[slice_len:]
                    
    # Получает ID группы по запросу
    def get_group_id(self, group):
        extracted_group_id = self.extract_group_id(group)
        
        if extracted_group_id:
            logger.info('Получение ID группы по запросу: ' + group)
            try:
                result = self.vk.groups.getById(group_id=extracted_group_id)
                if(result):
                    return -result[0]['id']
                else:
                    logger.warning('Группа не найдена: ' + group)

            except vk_api.exceptions.ApiError as err:
                logger.error('ApiError: ' + str(err))
                self.bot_work = False
                
            except Exception as err:
                logger.error(err.__class__.__name__, exc_info=True)
        else:
            logger.warning('Неправильная ссылка на группу: ' + group)
        
    # Добавляет группу в список групп
    def add_group(self, group):
        try:
            logger.info('Добавление группы: ' + group)
            
            group_id = self.get_group_id(group)
            
            if group_id and group_id not in self.groups_id:
                self.groups_id.append(group_id)
                self.groups[group_id] = Group(group_id, self.vk_pointer)
            
                with open(self.groups_id_file_path, 'w') as f:
                    json.dump(self.groups_id, f)
                    
                logger.info('Группа добавлена: ' + group)
                
        except Exception as err:
            logger.error(err.__class__.__name__, exc_info=True)
        
    # Загружает список групп из файла
    def load_groups(self):
        if not os.path.exists(self.groups_id_file_path):
            open(self.groups_id_file_path, 'a').close()
            self.groups_id = []
        else:
            try:
                with open(self.groups_id_file_path) as f:
                    self.groups_id = json.load(f)
            except:
                self.groups_id = []
        
        self.groups = {}
                
        for group_id in self.groups_id:
            group = Group(group_id, self.vk_pointer)
            self.groups[group_id] = group
        
    # Слушает группы на новые посты
    def _listen_groups(self):
        logger.info('Начинаю просмотр постов групп')
        while self.bot_work:
            groups_posts = {}
            items = tuple(self.groups.items())
            for group_id, group in items:
                try:
                    groups_posts[group_id] = group.get_new_posts()
                    #sleep(self.delays['viewing_other_groups'])
                    sleep(3)
                    
                except vk_api.exceptions.ApiError as err:
                    logger.error(err.__class__.__name__, exc_info=True)
                    self.bot_work = False

                except Exception as err:
                    logger.error(err.__class__.__name__, exc_info=True)
                    
            group_posts_shuffled = []
            for group, posts in groups_posts.items():
                for post in posts:
                    group_posts_shuffled.append((group, post))
                    
            shuffle(group_posts_shuffled)
            
            #logger.info(str(group_posts_shuffled))

            for (group, post) in group_posts_shuffled:
                try:
                    logger.info(f'Ставлю лайк на пост группы: {group}, поста: {post["id"]}')
                    self.vk.likes.add(type='post', owner_id=group, item_id=post['id'])
                    sleep(randint(self.delays['like_min'], self.delays['like_max']))

                    logger.info(f'Делаю репост поста группы: {group}, поста: {post["id"]}')
                    self.vk.wall.repost(object=f'wall{group}_{post["id"]}')
                    sleep(randint(self.delays['repost_min'], self.delays['repost_max']))

                    self.groups[group].add_viewed_post_id(post)

                except vk_api.exceptions.ApiError as err:
                    logger.error(err.__class__.__name__, exc_info=True)
                    self.bot_work = False

                except Exception as err:
                    logger.error(err.__class__.__name__, exc_info=True)
                    
            
                    
    # Слушает частную группу для получения ID групп для мониторинга
    def _listen_private_group(self):
        logger.info('Просмотр постов с ID групп в частной группе')
        while self.bot_work:
            try:
                posts = self.private_group.get_new_posts()
                
                if(posts):
                    self.private_group.add_viewed_post_id(*posts)
                        
                    groups = [post['text'] for post in posts if post['text']]
                    
                    logger.info('Найдены следующие группы:\n' +
                        '\n'.join(f'{i}. {group}' for i, group in enumerate(groups, start=1)))
                        
                    for group in groups:
                        self.add_group(group)

            except vk_api.exceptions.ApiError as err:
                logger.error(err.__class__.__name__, exc_info=True)
                self.bot_work = False
                        
            except Exception as err:
                    logger.error(err.__class__.__name__, exc_info=True)
            sleep(self.delays['viewing_private_group'])
        
       
    # Запускает новый поток с прослушиванием приватной группы
    def listen_private_group(self):
        threading.Thread(target = self._listen_private_group, daemon=True).start()
        #self._listen_private_group()

    # Запускает новый поток с прослушиванием групп
    def listen_groups(self):
        threading.Thread(target = self._listen_groups, daemon=True).start()
        #self._listen_private_group()
        
    def mainloop(self):
        while True:
            sleep(1)

def main():
    # Приветствие
    print (pyfiglet.Figlet(font='slant').renderText('VK MinerBot'))
    
    bot = MinerBot()
    #bot.add_group('https://vk.com/python_django_programirovanie')
    bot.listen_private_group()
    bot.listen_groups()
    bot.mainloop()
    
    #test()
    
if __name__ == '__main__':
    main()