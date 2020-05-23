# SYMULACJA SUPERMARKETU
# Autor: Emilia Augustyn, Maciej Białkowski
# Przedmiot: Systemy Operacyjne 2
# Prowadzący: dr. inż Dominik Żelazny

import threading
import random
import time

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
    shopping_list = []
  
    def __init__(self,client_id,client_trolley):
        threading.Thread.__init__(self)
        self.client_id = client_id
        self.client_trolley = client_trolley
        self.shopping_list = Client.generate_shopping_list()
        

    def run(self):
        while self.running:
            self.position = 0
            print("Klient %i próbuje pobrać wózek..." % self.client_id)
            self.take_trolley()
            print("Klient %i pobrał wózek i zaczyna zakupy..." % self.client_id)
            self.shopping()
        
        
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
            next_product = self.shopping_list[0]
            next_target = self.shopping_list[0]//3
            while self.position != next_target:
                print("Klient "+ str(self.client_id)+ " znajduje sie przy półce "+ str(self.position)+" i kieruje się do półki "+ str(next_target)+" po kolejny produkt")
                time.sleep(1)
                if self.position > next_target:
                    self.position = self.position - 1
                if self.position < next_target:
                    self.position = self.position+ 1
            print("Klientowi "+ str(self.client_id) +" prubuje dostać się do półki ")   
            locked=shelves[next_target-1].locked
            if locked:
                print("Klient "+str(self.client_id)+" dotarł do półki "+str(self.position)+", znalazł produkt! Pobiera go z półki i sprawdza czy zostało mu coś jeszcze na liście")
                self.shopping_list.pop(0)
                time.sleep(2)
                print("Klientowi "+ str(self.client_id) +" pozostało " + str(len(self.shopping_list)) + " produktów!")
                shelves[next_target-1].release
            else:
                time.sleep(1)
                self.shopping_list.append(self.shopping_list[0]-1)
                self.shopping_list.pop(0)
                print("Klient "+ str(self.client_id) +" dotarł do półki " + str(self.position) + " jednak ktoś przy niej stoi, rusza więc po kolejny produkt")
        print("Lista zakupów została skompletowana!")
        exit(0)
        pass
      
# TODO
class Cashier():
    # Obsługuje klientów przez czas proporcjonalny do dł. listy zakupów
    pass

# Główna fukncja programu
def simulation():
    # Tworzenie wątków
    clients = [Client(i,trolleys[i % TROLLEY_NUMBEROF]) for i in range(CLIENT_NUMBEROF)]
    
    #for i in range(CLIENT_NUMBEROF):
    #    print("CLIENT ID: ",clients[i].client_id,"SHOPPING LIST: ",clients[i].shopping_list)

    # Uruchomienie wątków
    Client.running = True
    for c in clients:
        c.start()

# Start symulacji
simulation()

