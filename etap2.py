# SYMULACJA SUPERMARKETU
# Autor: Emilia Augustyn, Maciej Białkowski
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

# Zamki 
trolleys = [threading.Lock() for i in range(TROLLEY_NUMBEROF)]
shelves = [threading.Lock() for i in range(SHELF_NUMBEROF)]

trolleys_queue = []

class Client(threading.Thread):
    running = True
    position=0
    next_product=0
    number_of_products = 0
    state = "czeka na wózek"
    shopping_list = []
    
    def __init__(self,client_id,client_trolley):
        threading.Thread.__init__(self)
        self.client_id = client_id
        self.client_trolley = client_trolley
        self.shopping_list = Client.generate_shopping_list()
        

    def run(self):
        while self.running:
            self.position = 0
            self.take_trolley()
            self.state = "idzie po kolejny produkt"
            self.shopping()
            self.go_to_cash()
            s
            self.client_trolley.release()
        
        
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
            if locked:
                break
            # print("%i ma wózek i nie odda ;x" % self.client_id )

    # TODO 
    def shopping(self):
        #dopuki nie znajdziemy wszystkich zakupów
        print(self.shopping_list)
        while len(self.shopping_list)!=0:
            #wyznaczamy następną półke z produktem
            self.state = "idzie po kolejny produkt"
            self.next_product = self.shopping_list[0]
            next_target = self.shopping_list[0]//3
            while self.position != next_target:
                # print("Klient "+ str(self.client_id)+ " znajduje sie przy półce "+ str(self.position)+" i kieruje się do półki "+ str(next_target)+" po kolejny produkt")
                time.sleep(1)
                if self.position > next_target:
                    self.position = self.position - 1
                if self.position < next_target:
                    self.position = self.position+ 1
                # print("Klientowi "+ str(self.client_id) +" prubuje dostać się do półki ")  
            self.state = "dotarł do półki z produktem" 
            locked=shelves[next_target-1].locked
            if locked:
                # print("Klient "+str(self.client_id)+" dotarł do półki "+str(self.position)+", znalazł produkt! Pobiera go z półki i sprawdza czy zostało mu coś jeszcze na liście")
                self.state = "bierze produkt z półki"
                self.shopping_list.pop(0)
                time.sleep(2)
                # print("Klientowi "+ str(self.client_id) +" pozostało " + str(len(self.shopping_list)) + " produktów!")
                shelves[next_target-1].release
            else:
                self.state = "przy półce ktoś stoi, kieruje sie po kolejny produkt z listy"
                time.sleep(1)
                self.shopping_list.append(self.shopping_list[0]-1)
                self.shopping_list.pop(0)
        self.state="lista zakupów jest skompletowana"
        time.sleep(2)
                # print("Klient "+ str(self.client_id) +" dotarł do półki " + str(self.position) + " jednak ktoś przy niej stoi, rusza więc po kolejny produkt")
        # print("Lista zakupów została skompletowana!")
        pass

    def go_to_cash(self):
        while len(self.shopping_list)==0:
            #wyznaczamy następną półke z produktem
            self.state = "idzie do kasy"
            next_target = PRODUCT_NUMBEROF//3 + 1
            while self.position != next_target:
                # print("Klient "+ str(self.client_id)+ " znajduje sie przy półce "+ str(self.position)+" i kieruje się do półki "+ str(next_target)+" po kolejny produkt")
                time.sleep(1)
                if self.position > next_target:
                    self.position = self.position - 1
                if self.position < next_target:
                    self.position = self.position+ 1
            self.state = "czeka na skasowanie produktów"
            time.sleep(2)
            self.state = "kończy zakupy i odkłada wózek"
        pass
            
    def __str__(self):
        return("Klient: "+str(self.client_id)+" znajduje się przy półce "+str(self.position)+" i kieruje się do półki "+str(self.next_product//3))
      
# TODO
class Cashier():
    # Obsługuje klientów przez czas proporcjonalny do dł. listy zakupów
    pass


class Printer(threading.Thread):
    running = True
    def __init__(self,client_list):
        threading.Thread.__init__(self)
        self.client_list = client_list
        print("konstruktor W WYPISYWANIU ")
        
    def run(self):
        while self.running:
            os.system('cls')
            self.print_clients_state()
            self.print_client_maps()
            for client in self.client_list:
                print(client)
            time.sleep(1)

    def print_clients_state(self):
        print("-----------------------------------------------------------------------------------")
        print("                Status klientów")
        print("-----------------------------------------------------------------------------------")
        for client in self.client_list:
            print("     Klient: ["+str(client.client_id)+"]:"+str(client.state)+".  Pozostała lista zakupów: "+str(client.shopping_list))
        print("-----------------------------------------------------------------------------------")

    def print_client_maps(self):
        print("-----------------------------------------------------")
        print("                Mapa")
        print("-----------------------------------------------------")
        # TODO poprawić numeracje półek
        # print(for i in range(1,SHELF_NUMBEROF): str(i) + "  ")
        for client in self.client_list:
            print("   " * client.position + "X")
        print("-----------------------------------------------------")

# Główna fukncja programu
def simulation():
    # Tworzenie wątków
    clients = [Client(i,trolleys[i % TROLLEY_NUMBEROF]) for i in range(CLIENT_NUMBEROF)]
    
    # Uruchomienie wątków
    Client.running = True
    for c in clients:
        c.start()
    printer = Printer(clients)
    printer.running = True 
    printer.start()

# Start symulacji
simulation()

