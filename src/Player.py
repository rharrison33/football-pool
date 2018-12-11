'''
Created on Nov 4, 2018

@author: robert harrison
'''

class Player(object):
    '''
    classdocs
    '''


    def __init__(self, id, name, picks):
        self.id = id
        self.name = name
        self.picks = picks
        self.tbpts = picks[-1] #last element of pick array is tb points
        self.record = [0, 0, self.tbpts]