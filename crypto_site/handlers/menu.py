import json
import asyncio
from functools import partial
from pywebio.output import *
import pywebio.input as inp
from pywebio.session import run_js


class TaskHandler:
    def __init__(self):
        self.coins = ['BTC', 'ETH']

    @staticmethod
    def read_task_file():
        with open('tasks.json', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def add_task_to_file(data: dict): #Принимаем словарь data
        last_changes = TaskHandler.read_task_file() #Получаем старые изменения
        last_changes[data['name']] = data['price to alert'] #Вносим кориктировки

        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(last_changes, file, indent=4)

    @staticmethod
    def delete_task_in_file(coin_name, update=True): #Перезапись инфы
        last_changes = TaskHandler.read_task_file()
        try:
            del last_changes[coin_name]  #Перезаписываем токен

            with open('tasks.json', 'w', encoding='utf-8') as file: #Перезапись ключа
                json.dump(last_changes, file, indent=4)
        except KeyError:
            print('Ключ отсутствует в списке заданий')
        if update:
            run_js('location.reload()')

    @staticmethod
    def get_task_list(): #Получаем все задания 
        result = []
        tasks = TaskHandler.read_task_file() 

        for name, price in tasks.items(): #Пробигаемся по файле собирая все значения
            result.append([
                name,
                price,
                put_button(f'delete {name}', onclick=partial(TaskHandler.delete_task_in_file, name))
            ])

        put_table( #Добавляем таблицу
            result,
            header=['name', 'price to alert', 'delete?']
        )
        put_button('Назад', onclick=lambda: run_js('location.reload()')) #Вызываем джс скрипт что бы возвращало на главный екран

    @staticmethod
    def add_task_validate(data): #Вызываем когда выбираеться монета
        if data is None or data == '':
            return 'Вы не заполнели поле'

    async def add_task_in_list(self):
        coin_ticker = await inp.select('Выберите монету', self.coins, multiple=False)#предлагаем выбор
        price = await inp.input('Введите ожидаемую цену', validate=TaskHandler.add_task_validate)

        if all([coin_ticker, price]): #Если пользователь ввёл все значения
            toast(['Задание было создано'])
            await asyncio.sleep(1)
            run_js('local.reload()') #Перезагрузка страницы
            TaskHandler.add_task_to_file({
                'name': coin_ticker.lower(),
                'price to alert': price.replace('.', '',).replace(',', ''.lower())
                })
            run_js('location.reload()')
