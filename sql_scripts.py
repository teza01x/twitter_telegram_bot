import sqlite3
from datetime import datetime, timedelta, time
from config import *


def user_exists(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id,))
    exists = bool(len(result.fetchall()))

    conn.close()

    return exists


def add_user_to_db(user_id, username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    reg_time = datetime.now().strftime("%d/%m/%y")
    cursor.execute("INSERT INTO user (user_id, username, status_verif, start_menu, date_reg, status_menu) VALUES(?, ?, ?, ?, ?, ?)",
                   (user_id, username, 0, None, reg_time, 0,))

    conn.commit()
    conn.close()


def add_user_to_ver_db(user_id, username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO verified_user (user_id, username, user_twitter, message_id, status_menu, count_tasks_completed, count_tasks_created, number_app, date_created_order, order_create_status) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, username, None, None, 0, 0, 0, None, None, 0,))

    conn.commit()
    conn.close()


def check_start_menu_id(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT start_menu FROM user WHERE user_id = ?", (user_id,))
    id_menu = cursor.fetchone()[0]

    conn.close()

    return id_menu


def add_start_menu_id(user_id, menu_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET start_menu = ? WHERE user_id = ?", (menu_id, user_id,))

    conn.commit()
    conn.close()


def check_verification(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT status_verif FROM user WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    conn.close()

    try:
        if data != None:
            return data[0]
    except:
        return 0


def check_user_menu_status(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT status_menu FROM user WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def update_user_menu_status(user_id, status_menu):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET status_menu = ? WHERE user_id = ?", (status_menu, user_id,))

    conn.commit()
    conn.close()


def get_user_info(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_twitter FROM verified_user WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return [data]


def twitter_id_entry(user_id, user_twitter):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE verified_user SET user_twitter = ? WHERE user_id = ?", (user_twitter, user_id,))

    conn.commit()
    conn.close()


def update_verif_status_menu(user_id, status_menu):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE verified_user SET status_menu = ? WHERE user_id = ?", (status_menu, user_id,))

    conn.commit()
    conn.close()


def user_message_id(user_id, message_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE verified_user SET message_id = ? WHERE user_id = ?", (message_id, user_id,))

    conn.commit()
    conn.close()


def get_user_id(message_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM verified_user WHERE message_id = ?", (message_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def verification_status(user_id, ver_status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET status_verif = ? WHERE user_id = ?", (ver_status, user_id,))

    conn.commit()
    conn.close()


def get_username(message_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM verified_user WHERE message_id = ?", (message_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def get_uniq_app_number():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT number_app FROM verified_user")
    data = cursor.fetchall()

    conn.close()

    data = [i[0] for i in data]

    return data


def add_app_number(user_id, app_number):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE verified_user SET number_app = ? WHERE user_id = ?", (app_number, user_id,))

    conn.commit()
    conn.close()


def get_number_app(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT number_app FROM verified_user WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def get_verif_status_menu(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT status_menu FROM verified_user WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()[0]

    conn.close()

    return data


def get_user_stats(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT count_tasks_completed, count_tasks_created FROM verified_user WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()[0]

    conn.close()

    return data


def get_uniq_order_id():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM task_order")
    data = cursor.fetchall()

    conn.close()

    data = [i[0] for i in data]

    return data


def order_create_status(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT order_create_status FROM verified_user WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()[0]

    conn.close()

    return data[0]


def set_order_create_status(user_id, order_status):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE verified_user SET order_create_status = ? WHERE user_id = ?", (order_status, user_id,))

    conn.commit()
    conn.close()


def pre_create_order(order_id, user_id_creator):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    date_created = datetime.now().strftime("%d/%m/%y")

    cursor.execute("INSERT INTO task_order (order_id, times_completed, users_completed, order_status, user_id_creator, date_created, twitter_link) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   (order_id, 0, None, 0, user_id_creator, date_created, None,))

    conn.commit()
    conn.close()


def del_pre_create_order(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM task_order WHERE user_id_creator = ? AND order_status = ?", (user_id, 0,))

    order_id = cursor.fetchone()[0]

    cursor.execute("DELETE FROM task_order WHERE order_id = ?", (order_id,))

    conn.commit()
    conn.close()


def confirm_create_order(user_id, twitter_link):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM task_order WHERE user_id_creator = ? AND order_status = ?", (user_id, 0,))

    order_id = cursor.fetchone()[0]

    cursor.execute("UPDATE task_order SET twitter_link = ?, order_status = ? WHERE order_id = ?", (twitter_link, 1, order_id,))

    date_created = datetime.now().strftime("%d/%m/%y")
    cursor.execute("UPDATE verified_user SET date_created_order = ? WHERE user_id = ?", (date_created, user_id,))

    conn.commit()
    conn.close()


def get_active_orders():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT order_id FROM task_order WHERE order_status = ?", (1,))

    result = cursor.fetchall()
    result = [i[0] for i in result]

    conn.close()

    return result


def get_order_link(order_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT twitter_link FROM task_order WHERE order_id = ?", (order_id,))

    result = cursor.fetchone()[0]

    conn.close()

    return result


def add_user_in_task_order(order_id, user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT users_completed FROM task_order WHERE order_id = ?", (order_id,))
    users = cursor.fetchone()[0]
    if users != None:
        updated_list = users + str(user_id) + ":"
    else:
        updated_list = "" + str(user_id) + ":"

    cursor.execute("UPDATE task_order SET users_completed = ? WHERE order_id = ?", (updated_list, order_id,))

    conn.commit()
    conn.close()


def get_verified_users():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM user WHERE status_verif = ?", (1,))

    result = cursor.fetchall()
    result = [i[0] for i in result]

    conn.close()

    return result


def get_twitter_link(order_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT twitter_link FROM task_order WHERE order_id = ?", (order_id,))

    result = cursor.fetchone()[0]

    conn.close()

    return result


def get_user_completed_list(order_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT users_completed FROM task_order WHERE order_id = ?", (order_id,))

    result = cursor.fetchone()[0]

    if result is not None:
        result = result.split(":")
        result = [i for i in result if len(i) > 0]
        return result
    else:
        return []

    conn.close()


def change_order_status(order_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("UPDATE task_order SET order_status = ? WHERE order_id = ?", (2, order_id,))

    conn.commit()
    conn.close()


def get_orders_by_date():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    current_date_str = datetime.now().strftime("%d/%m/%y")

    cursor.execute("SELECT order_id FROM task_order WHERE date_created = ?", (current_date_str,))
    result = cursor.fetchall()

    conn.close()

    if result != None:
        return [i[0] for i in result]
    else:
        return []


def get_date_last_create(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT date_created_order FROM verified_user WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()[0]

    conn.close()

    return result


def get_verified_users_ids():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM user WHERE status_verif = ?", (1,))
    result = cursor.fetchall()

    conn.close()

    return [i[0] for i in result]


def delete_order_by_admin(order_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM task_order WHERE order_id = ?", (order_id,))

    conn.commit()
    conn.close()


def ban_by_admin(username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]

    cursor.execute("UPDATE user SET status_verif = ? WHERE user_id = ?", (2, user_id,))

    conn.commit()
    conn.close()


def unban_by_admin(username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]

    cursor.execute("UPDATE user SET status_verif = ? WHERE user_id = ?", (1, user_id,))

    conn.commit()
    conn.close()


def add_user_id_to_user_task_table(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user_task_count (user_id, task_received, task_completed) VALUES(?, ?, ?)",
                   (user_id, None, None,))

    conn.commit()
    conn.close()


def add_task_id_to_user_task_table(user_id, task_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT task_received FROM user_task_count WHERE user_id = ?", (user_id,))
    task_id_list = cursor.fetchone()[0]


    if task_id_list != None:
        updated_list = task_id_list + str(task_id) + ":"
    else:
        updated_list = "" + str(task_id) + ":"

    cursor.execute("UPDATE user_task_count SET task_received = ? WHERE user_id = ?", (updated_list, user_id,))

    conn.commit()
    conn.close()


def get_task_id_completed(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute("SELECT task_received FROM user_task_count WHERE user_id = ?", (user_id,))

    task_received = cursor.fetchone()[0]

    if task_received is not None:
        task_received = task_received.split(":")
        task_received = [i for i in task_received if len(i) > 0]
    else:
        task_received = []

    cursor.execute("SELECT task_completed FROM user_task_count WHERE user_id = ?", (user_id,))

    task_completed = cursor.fetchone()[0]

    if task_completed is not None:
        task_completed = task_completed.split(":")
        task_completed = [i for i in task_completed if len(i) > 0]
    else:
        task_completed = []

    conn.close()

    count = 0
    for task_rec in task_received:
        if task_rec in task_completed:
            count += 1

    if count == len(task_received):
        return True
    else:
        return False


def add_task_id_to_user_task_completed(user_id, task_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT task_completed FROM user_task_count WHERE user_id = ?", (user_id,))
    task_id_list = cursor.fetchone()[0]


    if task_id_list != None:
        updated_list = task_id_list + str(task_id) + ":"
    else:
        updated_list = "" + str(task_id) + ":"

    cursor.execute("UPDATE user_task_count SET task_completed = ? WHERE user_id = ?", (updated_list, user_id,))

    conn.commit()
    conn.close()


def update_username(user_id, username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET username = ? WHERE user_id = ?", (username, user_id,))

    cursor.execute("UPDATE verified_user SET username = ? WHERE user_id = ?", (username, user_id,))

    conn.commit()
    conn.close()