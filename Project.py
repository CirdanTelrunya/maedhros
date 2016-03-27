#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import fnmatch
from User import User

class Project:
    """"""
    def __init__(self):
        """"""
        self.directory = None
        self.images = []
        self.users = []
        self.current_user = None
        
    def set_directory(self, directory):
        self.directory = directory
        self.images.extend(self._find_files(directory, '*.jpg', '*.JPG'));
        print('length =', len(self.images))

    def _find_files(self, directory, *patterns):
        
        for root, dirs, files in os.walk(directory):
            for basename in files:
                for pattern in patterns:
                    if fnmatch.fnmatch(basename, pattern):
                        filename = os.path.join(root, basename)
                        yield filename

    def add_user(self, name):
        """"""
        new_user = User(name, len(self.images))
        self.users.append(new_user)

    def select_user(self, name):
        """"""
        self.current_user = next(user for user in self.users if user.name == name)
        print('selet ', self.current_user.name)
        
    def get_random_contest(self):
        """"""
        return self.current_user.get_random_contest()
    
if __name__ == '__main__':
    p = Project()
    p.set_directory('/home/cirdan/Photos/Cambodge_2015/Done/init')
    p.add_user('Ronan')
    result = p.users[0].get_random_contest()
    print(result)
    p.select_user('Ronan')
    
    pass
