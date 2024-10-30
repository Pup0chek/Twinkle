from abc import abstractmethod
import threading
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
class Human:
    count = 0

    #INIT method
    def __init__(self, name, age, proff):
        self.name = name
        self.age = age
        self.proff = proff
        Human.count += 1

    @classmethod
    def print_count(cls):
        print(f"Count of created humans={Human.count}")

    @staticmethod
    def calculate(age):
        print(f'You will be {age+6} in 2030')

    @abstractmethod
    def dream(self):
        print(f'Humans dream about happiness')

    def __str__(self):
        return f"name:{self.name}, age:{self.age}"

class Lia(Human):
    name = "Lia"
    def __init__(self, age, proff, durost):
        super().__init__(Lia.name, age, proff)
        self._durost = durost

    def dream(self):
        super().dream()
        print(f'{Lia.name} dreams about {self._durost}')

    @property
    def durost(self):
        return f"Lia's biggest dream right now, is to {self._durost}"

    @durost.setter
    def durost(self, new_durost):
        if new_durost != " ":
            self._durost = new_durost
        else:
            print("Durost can't be empty")

    @staticmethod
    def add_tea(funs):
        def wrapp(*args, **kwargs):
            print(f"Drinks tea")
            funs(*args, **kwargs)
        return wrapp

    @staticmethod
    @add_tea
    def eat_choco(choco):
        print(f"Eats {choco} choco")

Human.calculate(1)
Ilya = Human("Ilya",20,'Pythonist')
Ilya.dream()
Lia = Lia(20,'pentester','to throw pentest and enroll into the development')
Lia.dream()
Human.print_count()
Lia.durost = " "
print(Lia.durost)
print(Lia)
Lia.eat_choco("white")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI")
        self.setGeometry(600, 250, 700, 500)

app = QApplication([sys.argv])
window = MainWindow()
window.show()
sys.exit(app.exec_())