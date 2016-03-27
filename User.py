#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
from operator import itemgetter

class User:
    """"""
    def __init__(self, name, size):
        """"""
        self.name = name
        self.scores = np.zeros((size, size), dtype=np.int32)
        # use only lower part of the array
        np.fill_diagonal(self.scores, np.iinfo(np.int32).min)
        # self.scores += np.triu(np.full((size, size), -np.inf, dtype=np.int32))
        print(self.scores)
        
    def get_random_contest(self):
        """"""        
        cpt = 0
        result = np.where(self.scores == cpt)    
        while not result[0].size:
            cpt = cpt +1
            result = np.where(self.scores == cpt)
            print('try with score : ', cpt)

        result = np.dstack(result).reshape((-1, 2))
        return random.choice(result)
        
    def choice(self, winner, looser):
        """"""
        self.scores[winner, looser] += 2
        self.scores[looser, winner] -= 2
        
        print('col =\n', self.scores[:,looser])
        for idx, val in enumerate(self.scores[:,looser]):
            if val < 0 and val != np.iinfo(np.int32).min:
                self.scores[winner, idx] += 1
                print('add ', winner, idx)
        print('self.scores =\n', self.scores)
        
    def draw(self, img0, img1):
        """"""
        self.scores[img0, img1] += 1
        self.scores[img1, img0] += 1
        # tmp = np.copy(self.scores)
        # np.fill_diagonal(tmp, 0)
        # result = enumerate(np.sum(tmp, axis=1))
        # print('result =\n', result)
        # print('result =\n', sorted(result, key=itemgetter(1), reverse=True))

    def eliminate(self, img):
        """"""
        # all scores are negate to a maximum
        self.scores[img,:] = -self.scores.shape[0]
        print('self.scores =\n', self.scores)
