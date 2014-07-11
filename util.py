from HTMLParser import HTMLParser
import os

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed) 

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

def mkdir(path_to_dir):
    try:
        os.makedirs(path_to_dir)
    except:
        pass