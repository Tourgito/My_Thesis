import subprocess
import threading
import shlex
import os
from time import sleep
import sys

subs = list()
Services = ['./AccountService','./APIGateway','./CustomerService','./OrdersService','./ProductService','./CQRS']   #'./EmailService'

def RunProcess(number,a):
    if number == 0:
     if a != './CQRS' and a != './APIGateway':
        f = shlex.split('python3 EventPublisher.py')
        o = subprocess.Popen(f)
        subs.append(o)
    elif number == 1:    
        if a != './APIGateway':
            d = shlex.split('python3 KafkaConsumer.py')
            l = subprocess.Popen(d)
            subs.append(l)
    else:
        if a != './AccountService':
            k = shlex.split('python3 RestApi.py')
            n = subprocess.Popen(k)
            subs.append(n)



def a(Service):
    if Service != './AccountService':
        os.chdir('../')
    os.chdir(Service)
    u = shlex.split('pwd')
    subprocess.Popen(u)
    for number in range(0,3):
            threading.Thread(target=RunProcess, args=(number,Service,)).start()

    #subprocess.check_call(["python3", b])

#subprocess.check_call(["python3", "a.py"])
#subprocess.check_call(["python3", "b.py"])

if __name__ == "__main__":
    for Service in Services:
        threading.Thread(target=a, args=(Service,)).start()
        sleep(2)
    print(subs)    
    print()    
    print()    
    print('------------------------------------------------------------------------------------------------------')    
    while True:
        try:
            sleep(1000000000)
        except KeyboardInterrupt:        
             for sub in subs:
                print(sub) 
                sub.kill()
       
        sys.exit()
