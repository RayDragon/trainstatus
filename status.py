import bs4, sys, requests

def get_status(number, date=0, stn='jabalpur'):
    date = ['yesterday', 'today','tomorrow'][int(date)+1]
    soup = bs4.BeautifulSoup(requests.get('https://trainstatus.info/running-status/'+str(number)+'-'+date).text, 'html.parser')
    table = soup.find_all('table')[0]
    data = []
    usable = []
    for row in table.find_all('tr'):
        r=[]
        s_found = False
        count =0
        for col in row.find_all('td'): 
            if count == 1:
                try:
                    # print('comparing',col.text ,stn.upper())
                    i = col.text.index(stn.upper())
                    s_found=True
                    #print('Found')
                except Exception as e:
                    #print('Not found', e)
                    pass
            r.append(col.text)
            count += 1
        if len(r)!=0:
            data.append(r)
        if s_found:
            usable = r
    if len(usable) != 0:
        print("""
        Train status found
        """)
        print(usable)
        time = usable[-1]
        message = ''
        if time == '':
            time = 0
            message= 'is currently at Station ' + stn
        else:
            from datetime import timedelta, datetime
            time = int(time)
            if time > 0:
                t = datetime(1,1,1)  + timedelta(minutes=time)
                message= 'should reach ' + stn + ' in ' + str(t.day-1)+' days ' + str(t.hour) +' hours '+ str(t.minute)+ ' minutes ' #+ str(t.second) + ' seconds'
            else:
                t = datetime(1,1,1)  + timedelta(minutes=-1*time)
                message= 'already left ' + stn + ' approximately ' + str(t.day-1)+' days ' + str(t.hour) +' hours '+ str(t.minute)+ ' minutes before'
        print('The train '+message)
        
    else:
        from pprint import pprint
        print("""
        Train status cant be found, below are the details
        """)
        pprint(data, indent=5, width=300)
    print("\n\n")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('''
        Sample use case ...
            python .\status.py 11062 -1
        where 11062 is train number
        -1 0 1 represent the start date of train
        ''')
        exit()
    get_status(*sys.argv[1:])

