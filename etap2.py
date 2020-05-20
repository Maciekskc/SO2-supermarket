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
        

    def run(self):
        while self.running:
            self.generate_shopping_list()
            self.position = 0
            print("Klient %i próbuje pobrać wózek..." % self.client_id)
            self.take_trolley()
            print("Klient %i pobrał wózek i zaczyna zakupy..." % self.client_id)
            self.shopping()
        
        
    def generate_shopping_list(self):
        self.number_of_products = random.randint(1,PRODUCT_NUMBEROF)
        for i in range(0,self.number_of_products):
            self.shopping_list.append(random.randint(1,PRODUCT_NUMBEROF))

    def take_trolley(self):
        trolley = self.client_trolley

        while self.running:
            locked = trolley.acquire(False)
            if locked:
                break
            # print("%i ma wózek i nie odda ;x" % self.client_id )

    # TODO 
    def shopping(self):
        # Robimy zakupy wg. listy
        pass
        
        
# TODO
class Cashier():
    # Obsługuje klientów przez czas proporcjonalny do dł. listy zakupów
    pass

# Główna fukncja programu
def simulation():
    # Tworzenie wątków
    clients = [Client(i,trolleys[i % TROLLEY_NUMBEROF]) for i in range(CLIENT_NUMBEROF)]

    # Uruchomienie wątków
    Client.running = True
    for c in clients:
        c.start()

# Start symulacji
simulation()

