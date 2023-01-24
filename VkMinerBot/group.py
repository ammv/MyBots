import json
import os

from post_stack import PostStack

class Group:
    def __init__(self, group_id, vk):
        self.group_id = group_id
        self.posts_file = f"data\posts\{str(self.group_id)}.json" 
        self.viewed_posts_id = PostStack()
        self.vk = vk
        self.load()
        
    def add_viewed_post_id(self, *posts_id):
        self.viewed_posts_id.add(*posts_id)
        self.save()
                    
    def filter_posts(self, posts):
        new_posts = list(filter(lambda post: post['id'] not in self.viewed_posts_id.items, posts))
        return new_posts
        
    def save(self):
        with open(self.posts_file, 'w') as f:
            json.dump(self.viewed_posts_id.get_file_version(), f)
            
    def load(self):
        if not os.path.exists(self.posts_file):
            open(self.posts_file, 'a').close()
            self.viewed_posts_id = PostStack()
        else:
            try:
                with open(self.posts_file) as f:
                    data = json.load(f)

                    pointer, data = data[0] ,data[1:]
                    size = len(data)

                    self.viewed_posts_id = PostStack(size, pointer)

                    self.viewed_posts_id.from_data(data)
            except Exception as err:
                print('Error', err)
            
    def get_new_posts(self, n=5):
        if self.vk[0] != None:
            items = self.vk[0].wall.get(owner_id=self.group_id, count=5)['items']
            return self.filter_posts(items)
        return []