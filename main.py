# SYMULACJA SUPERMARKETU
# Autor: Emilia Augustyn 241248, Maciej Białkowski 
# Przedmiot: Systemy Operacyjne 2
# Prowadzący: dr. inż Dominik Żelazny

import threading
import random
import time
import os

CLIENT_NUMBEROF = 5
CASHIER_NUMBEROF = 2
TROLLEY_NUMBEROF = 4
PRODUCT_NUMBEROF = 10
SHELF_NUMBEROF = PRODUCT_NUMBEROF//3

PRODUCTS = {1:"cheese", 2:"ham", 3:"butter", 4:"milk", 5:"yoghurt", 6:"juice", 7:"bread",\
            8:"tomatoes", 9:"cucumber", 10:"pasta"}

trolleys = [threading.Lock() for i in range(TROLLEY_NUMBEROF)]
shelves = [threading.Lock() for i in range(SHELF_NUMBEROF)]

trolleys_queue = []

class Client(threading.Thread):
    running = True
    position=0
    next_product=0
    number_of_products = 0
    state = "Czeka na wózek"
    shopping_list = []
    
    def __init__(self,client_id,client_trolley):
        threading.Thread.__init__(self)
        self.client_id = client_id
        self.client_trolley = client_trolley
        

    def run(self):
        while self.running:
            self.shopping_list = Client.generate_shopping_list()
            self.position = 0
            self.take_trolley()
            self.shopping()
            self.go_to_cash()
            self.client_trolley.release()
            time.sleep(0.4+random.uniform(0,0.2))

        
        
    def generate_shopping_list():
        shopping_list = []
        number_of_products = random.randint(0,10)
        for i in range(number_of_products):
            shopping_list.append(random.choice(list(PRODUCTS.keys())))
        return shopping_list

    def take_trolley(self):
        trolley = self.client_trolley
        while self.running:
            locked = trolley.acquire(False)
            self.state = "Czeka na wózek"
            if locked:
                self.state = "Zabiera wózek"
                time.sleep(0.4+random.uniform(0,0.2))
                break

    def shopping(self):
        while len(self.shopping_list)!=0:
            self.state = "Idzie po kolejny produkt"
            self.next_product = self.shopping_list[0]
            next_target = self.shopping_list[0]//3
            while self.position != next_target:
                time.sleep(0.4+random.uniform(0,0.2))
                if self.position > next_target:
                    self.position = self.position - 1
                if self.position < next_target:
                    self.position = self.position+ 1
            self.state = "Dotarł do półki z produktem" 
            locked=shelves[next_target-1].locked
            if locked:
                self.state = "Bierze produkt z półki"
                self.shopping_list.pop(0)
                time.sleep(0.4+random.uniform(0,0.2))
                shelves[next_target-1].release
            else:
                self.state = "Przy półce ktoś stoi, kieruje się po kolejny produkt z listy"
                time.sleep(0.4+random.uniform(0,0.2))
                self.shopping_list.append(self.shopping_list[0]-1)
                self.shopping_list.pop(0)
        self.state="Lista zakupów jest skompletowana"
        time.sleep(0.4+random.uniform(0,0.2))
        pass

    def go_to_cash(self):
        self.state = "Idzie do kasy"
        next_target = PRODUCT_NUMBEROF//3 + 1
        while self.position != next_target:
            time.sleep(0.4+random.uniform(0,0.2))
            if self.position > next_target:
                self.position = self.position - 1
            if self.position < next_target:
                self.position = self.position+ 1
        self.state = "Czeka na skasowanie produktów"
        time.sleep(0.4+random.uniform(0,0.2))
        self.state = "Kończy zakupy i odkłada wózek"
            
    def __str__(self):
        return("Klient: "+str(self.client_id)+" znajduje się przy półce "+str(self.position)+" i kieruje się do półki "+str(self.next_product//3))
      


class Printer(threading.Thread):
    running = True
    def __init__(self,client_list):
        threading.Thread.__init__(self)
        self.client_list = client_list
        
    def run(self):
        while self.running:
            os.system('cls')
            self.print_clients_state()
            self.print_client_maps()
            for client in self.client_list:
                print(client)
            time.sleep(0.4+random.uniform(0,0.2))

    def print_clients_state(self):
        print("-----------------------------------------------------------------------------------")
        print("                Status klientów")
        print("-----------------------------------------------------------------------------------")
        for client in self.client_list:
            print("Klient: ["+str(client.client_id)+"]:"+str(client.state)+".  Pozostała lista zakupów: "+str(client.shopping_list)+"ilość pozostałych produktów: "+str(len(client.shopping_list)))
        print("-----------------------------------------------------------------------------------")

    def print_client_maps(self):
        print("-----------------------------------------------------")
        print("                Mapa")
        print("-----------------------------------------------------")
        for client in self.client_list:
            print("   " * client.position + "X")
        print("-----------------------------------------------------")


# Główna fukncja programu
def simulation():
    clients = [Client(i,trolleys[i % TROLLEY_NUMBEROF]) for i in range(CLIENT_NUMBEROF)]
    
    #random.seed(507129)

    Client.running = True
    for c in clients:
        c.start()
    printer = Printer(clients)
    printer.running = True 
    printer.start()

# Start symulacji
simulation()

