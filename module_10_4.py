import threading
import time
import random
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Имитация времени пребывания гостя за столом
        time_to_stay = random.randint(3, 10)
        time.sleep(time_to_stay)


class Cafe:
    def __init__(self, *tables):
        self.tables = list(tables)
        self.queue = Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            assigned_table = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    assigned_table = True
                    break

            if not assigned_table:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(t.guest is not None for t in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            # Даем немного времени для проверки состояний
            time.sleep(1)


# Пример использования:
table1 = Table(1)
table2 = Table(2)
cafe = Cafe(table1, table2)

guest1 = Guest("Vasya")
guest2 = Guest("Petya")
guest3 = Guest("Masha")
guest4 = Guest("Katya")

cafe.guest_arrival(guest1, guest2, guest3, guest4)
cafe.discuss_guests()
