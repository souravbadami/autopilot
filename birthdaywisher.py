import facebook
import time 
import csv

_list={}

with open('birthdays.csv') as f:
    '''
    Gets the data from csv file.
    '''
    c = csv.reader(f)
    for row in c:
        if row[0] not in _list:
            _list[row[0]] = [row[1]]
        else:
            _list[row[0]].append(row[1])

def timer():
    '''
    This timer calls the main every 24 hours from when the script gets deployed.
    '''
    i=0 
    while (1): 
        main() 
        time.sleep(86400)

def main():     
    today = time.strftime("%x")
    if today in _list:
        for i in xrange(len(_list[today])):
            wish_message = 'Happy Birthday ' + _list[today][i] + '!\n We hope your special day will bring you lots of happiness, love and fun. You deserve them a lot. Enjoy!'
            graph = facebook.GraphAPI('access-token')
            graph.put_object("page-id", "feed", message=wish_message)
    
if __name__ == '__main__':
    timer()
