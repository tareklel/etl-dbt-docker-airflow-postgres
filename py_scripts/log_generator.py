from faker import Faker
import datetime
import time
import random
import numpy


def generate_logs():
    flag = True
    log_lines = 100
    faker = Faker()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    otime = datetime.datetime.now()
    # name log
    outFileName = 'access_log_'+timestr+'.log'
    response=["200","404","500","301"]
    verb=["GET","POST","DELETE","PUT"]
    resources=["/list","/content","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/cart"]
    users = ["Jimmy", "Janet", "Jason", "Julie", "Jack"]
    ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]
    f = open('../staging/' + outFileName,'w')
    
    for x in range(log_lines):
        increment = datetime.timedelta(seconds=random.randint(30, 300))
        otime += increment 
        us = numpy.random.choice(users,p=[0.2,0.2,0.2,0.2,0.2])
        ip = faker.ipv4()
        dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
        tz = datetime.datetime.now().strftime('%z')
        vrb = numpy.random.choice(verb,p=[0.6,0.1,0.1,0.2])
        uri = random.choice(resources)
        resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
        byt = int(random.gauss(6000, 10))
        referer = faker.uri()
        useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
        f.write('%s - %s [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip,us,dt,tz,vrb,uri,resp,byt,referer,useragent))
        f.flush
