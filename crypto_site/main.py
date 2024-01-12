import os
import pywebio
import threading
from pywebio.output import *
import pywebio.input as inp

from handlers.menu import TaskHandler
from handlers.parcer import check_coins_balance


@pywebio.config(theme='dark')
async def main():
    clear() #Очищаем интерфейс от лишнего
    threading.Thread(target=check_coins_balance).start()

    task = TaskHandler()
    logo_path = os.path.join('data', 'logo.jpg') #Путь к лого
    put_image(open(logo_path, 'rb').read()) #Прочитываем изображение

    method = await inp.select( #inp.select - ждёт ввод любых данных
        'Выберите нужный вариант',
        [
            'Добавить задание',
            'Список заданий',
        ])

    if 'Добавить задание' == method:
        await task.add_task_in_list()
    elif 'Список заданий' == method:
        task.get_task_list()


if __name__ == '__main__':
    #172.17.128.1 - IPv4-адрес
    pywebio.start_server(main, host='172.31.160.1', port=4547)

