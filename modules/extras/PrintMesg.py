import datetime
from termcolor import colored
def main(_head,_text,_color='green',_thread='Thread-??'):
    print(colored(str(datetime.datetime.now()) + ' | ','blue') + colored('%-14s | ' %(_thread),'magenta') + colored(' %-8s | %s' %(_head,_text),_color))