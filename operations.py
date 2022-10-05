import csv
import string
from typing import List


'''
глобальный список для записи контактов. 
'''
global tasks
global searched_tasks
tasks = []
searched_tasks = [] 


def add_task(key:str, value:str) -> None:
    '''
    добавить в список контакт
    '''
    tasks[key] = value


def search_task(searchstring: str, tasks:List):
    '''
    Поиск в телефонной книге
    '''
    for task in tasks:
        for value in task.values():
            if searchstring in value:
                   searched_tasks.append(task)
    return searched_tasks        


def delete_task() -> None:
    '''
    Удалить контакт из списка 
    '''
    tasks = [task for task in tasks if task in searched_tasks]
    return tasks

def edit_contact(index, value) -> None:
    '''
    Редактирование контакта. 
    '''
    contact_list[index] = value

def view_tasks(tasks: List) -> string:
    '''
    Запись в строку для Telegram
    '''
    strings =[]
    for task in tasks:
        for key, value in task.items():
            strings.append('{}: {}'.format(key.capitalize(), value))
        strings.append(' ')        
    result ='\n'.join(strings)        
    return result


def read_csv():
    '''
    Чтение из файла csv
    '''
    with open('todo.csv','r', encoding='utf-8') as f:
        tasks = [{key: value  for key, value in task.items()}
                for task in csv.DictReader(f, skipinitialspace=True)]
    return tasks
 
#print(read_csv())

def write_csv(tasks: List) -> None:
    '''
    Запись в csv фаил. 
    '''
    fieldnames = tasks[0].keys()
    with open('todo.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,lineterminator='\n')
        writer.writeheader()
        writer.writerows(tasks)
        


print(tasks)
