# Необходимо создать класс Bank со следующими свойствами:
#
# Атрибуты объекта:
# balance - баланс банка (int)
# lock - объект класса Lock для блокировки потоков.

from threading import Thread, Lock
import time
from random import randint

class Bank:

    def __init__(self):
        self.balance = 0
        self.lock = Lock()

#Метод deposit:
    # Будет совершать 100 транзакций пополнения средств.
    # Пополнение - это увеличение баланса на случайное целое число от 50 до 500.
    # Если баланс больше или равен 500 и замок lock заблокирован - lock.locked(), то разблокировать его методом release.
    # После увеличения баланса должна выводится строка "Пополнение: <случайное число>. Баланс: <текущий баланс>".
    # Также после всех операций поставьте ожидание в 0.001 секунды, тем самым имитируя скорость выполнения пополнения.

    def deposit(self):
        for _ in range(100):
            sum_balance = randint(a=50, b=500)

            """if self.balance >= 500 and self.lock.locked(): # lock.locked() - заблокирован
                self.lock.release()"""

            with self.lock:
                self.balance += sum_balance
                print(f'Пополнение: {sum_balance}. Баланс: {self.balance}')

            time.sleep(0.001)

#Метод take:

   # 1. Будет совершать 100 транзакций снятия.
   # 2. Снятие - это уменьшение баланса на случайное целое число от 50 до 500.
   # 3. В начале должно выводится сообщение "Запрос на <случайное число>".
   # 4. Далее производится проверка: если случайное число меньше или равно текущему балансу,
   #    то произвести снятие, уменьшив balance на соответствующее число и вывести на экран "Снятие: <случайное число>.
   #    Баланс: <текущий баланс>".
   # 5. Если случайное число оказалось больше баланса, то вывести строку "Запрос отклонён, недостаточно средств"
   #    и заблокировать поток методом acquire.

    def take(self):
        for _ in range(100):
            sum_balance = randint(a=50, b=500)
            print(f"Запрос на {sum_balance}")

            self.lock.acquire()
            try:
                if sum_balance <= self.balance:
                    self.balance -= sum_balance
                    print(f'Снятие: {sum_balance}. Баланс: {self.balance}')
                else:
                    print('Запрос отклонён, недостаточно средств')
            finally:
                self.lock.release()
            time.sleep(0.001)

# Далее создайте объект класса Bank и создайте 2 потока для его методов deposit и take. Запустите эти потоки.
# После конца работы потоков выведите строку: "Итоговый баланс: <баланс объекта Bank>".

# По итогу вы получите скрипт разблокирующий поток до баланса равному 500 и больше или блокирующий,
# когда происходит попытка снятия при недостаточном балансе.

bk = Bank()
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')

#Примечания:

   # Для генерации случайного целого числа используйте функцию randint из модуля random.
   # Для ожидания используйте функцию sleep из модуля time.
   # Особо важно соблюсти верную блокировку: в take замок закрывается, в deposit открывается.