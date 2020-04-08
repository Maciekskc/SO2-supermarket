# SYMULACJA SUPERMARKETU
# Autor: Emilia Augustyn, Maciej Białkowski
# Przedmiot: Systemy Operacyjne 2
# Prowadzący: dr. inż Dominik Żelazny

import threading
import random
import time

CLIENT_NUMBEROF = 5
CASHIER_NUMBEROF = 2
TROLLEY_NUMBEROF = 4 #no czemu tu jest kurwa błąd
PRODUCT_NUMBEROF = 30 
SHELF_NUMBEROF = PRODUCT_NUMBER//3

#TODO 
PRODUCTS = {1:"cheese", 2:"ham", 3:"butter", 4:"..."}

class Client(threading.Thread):
    # co ma klient
    position
    destination
    shoppinglist = []

class Cashier(threading.Thread):



# Główna fukncja programu
def simulation():
    # Tworzenie zamków
    trolley = [threading.Lock() for i in range(TROLLEY_NUMBEROF)]
    shelf = [threading.Lock() for i in range(SHELF_NUMBEROF)]

    # Tworzenie wątków

    # Tworzenie zasobów (?)

    # Uruchomienie wątków



# Start symulacji
simulation()

