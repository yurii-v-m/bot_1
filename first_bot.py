'''Simple bot'''
import json
from telebot import TeleBot


TOKEN = '5023359444:AAEM5NkwoOf4VX2HBmBplrk5A6WiNvHwA8Y'

bot = TeleBot(TOKEN)


def load_tasks_from_file():
    """load from json"""
    with open('tasks.json', 'r') as tasks_json_obj:
        to_do_list = json.load(tasks_json_obj)
    return to_do_list


def get_all_str():
    """get all strings from to do list """
    to_do_list = load_tasks_from_file()
    str_result = ''

    for deal_date in to_do_list:
        str_result += f'{deal_date}\n'
        num_deal = 0
        for deal in to_do_list[deal_date]:
            str_deal = f'{num_deal} {deal}'
            str_result += f'{str_deal}\n'
            num_deal += 1
        str_result += '\n'
    return str_result


@bot.message_handler(commands=['input_task'])
def input_task(message):
    bot.reply_to(message, text="Write date for new deal:")
    bot.register_next_step_handler(message, get_task_date)


def get_task_date(message):
    task_date = message.text
    bot.reply_to(message, f'Write new task for {task_date}:')
    bot.register_next_step_handler(message, add_task_action, task_date)


def add_task_action(message, task_date):
    task = message.text
    to_do_list = load_tasks_from_file()
    if task_date not in to_do_list:
        to_do_list[task_date] = [task, ]
    else:
        to_do_list[task_date].append(task)

    with open("tasks.json", "w", encoding="utf-8") as tasks_json_obj:
        json.dump(to_do_list, tasks_json_obj, indent=4, ensure_ascii=False)

    bot.reply_to(message, text="Done")


@bot.message_handler(commands=['print_all_tasks'])
def print_all_tasks(message):
    bot.reply_to(message, text=get_all_str())


@bot.message_handler(commands=["del_by_date"])
def del_by_date(message):
    bot.reply_to(message, text="Write date to delete tasks:")
    bot.register_next_step_handler(message, get_date_and_del)


def get_date_and_del(message):
    del_date = message.text
    to_do_list = load_tasks_from_file()
    to_do_list.pop(del_date)
    bot.reply_to(message, f'Write new task for {del_date}:')
    bot.register_next_step_handler(message, add_task_action, del_date)
    with open("tasks.json", "w", encoding="utf-8") as tasks_json_obj:
        json.dump(to_do_list, tasks_json_obj, indent=4, ensure_ascii=False)

    bot.reply_to(message, text='done')
    print_all_tasks(message)


bot.polling()

