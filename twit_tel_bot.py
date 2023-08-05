import asyncio
import telebot
from cachetools import cached, TTLCache
from datetime import datetime, timedelta, time
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from sql_scripts import *
from language_script import *
from async_funcs import *
from config import *


bot = AsyncTeleBot(telegram_token)
cache = TTLCache(maxsize=1000, ttl=60)


@bot.message_handler(commands=['start', 'menu'])
async def start(message):
    try:
        user_id = message.chat.id

        if check_verification(user_id) == 1:

            with open(admin_username_txt, 'r') as file:
                admin_usrname = file.readline()
                link_to_chat = 'https://t.me/' + admin_usrname

            button_list1 = [
                types.InlineKeyboardButton(btn['admin_contact'], url=link_to_chat),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['create_order'], callback_data="create_order"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3])
            old_menu = check_start_menu_id(user_id)
            if old_menu:
                try:
                    await bot.delete_message(message.chat.id, old_menu)
                except telebot.apihelper.ApiException as error:
                    pass

            menu_message = await bot.send_message(message.chat.id, text=dct['verif_menu'], reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)
        else:
            if not user_exists(user_id):
                try:
                    username = message.chat.username
                    add_user_to_db(user_id, username)
                    add_user_to_ver_db(user_id, username)
                except telebot.apihelper.ApiException as error:
                    print(error)
            else:
                username = message.chat.username
                update_username(user_id, username)


            button_list1 = [
                types.InlineKeyboardButton(btn['start_apply'], callback_data="start_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])

            old_menu = check_start_menu_id(user_id)
            if old_menu:
                try:
                    await bot.delete_message(message.chat.id, old_menu)
                except Exception as error:
                    pass

            menu_message = await bot.send_message(message.chat.id, dct["start"], reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)
    except telebot.apihelper.ApiException as e:
        print(e)


@bot.message_handler(commands=['time_left'])
async def time_left_user_command(message):
    try:
        user_id = message.chat.id

        if check_verification(user_id) == 1:
            if order_create_status(user_id) == 0:
                old_date_str = get_date_last_create(user_id)
                if old_date_str != None:
                    try:
                        old_date = datetime.strptime(old_date_str, "%d/%m/%y")

                        current_date = datetime.now()
                        current_date_str = current_date.strftime("%d/%m/%y")

                        time_difference = current_date - old_date
                        time_left = timedelta(days=7) - time_difference
                        days_left = time_left.days
                        if 5 <= days_left <= 7:
                            await bot.send_message(user_id, dct['time_left1'].format(days_left))
                        elif 2 <= days_left <= 4:
                            await bot.send_message(user_id, dct['time_left2'].format(days_left))
                        elif days_left == 1:
                            await bot.send_message(user_id, dct['time_left3'].format(days_left))
                        elif days_left == 0:
                            await bot.send_message(user_id, dct['time_left4'])
                    except telebot.apihelper.ApiException as error:
                        pass
            else:
                await bot.send_message(user_id, dct['ava_order_create'])
        else:
            await bot.send_message(user_id, dct['error_time_left'])
    except telebot.apihelper.ApiException as e:
        print(e)


@bot.message_handler(commands=['ban'])
async def ban_admin_command(message):
    try:
        user_id = message.chat.id

        with open(admin_id_txt, 'r') as file:
            admin_id = file.readline()

        if user_id == int(admin_id):
            username = await clean_text(message.text, '/ban')
            ban_by_admin(username)
            await bot.send_message(int(admin_id), dct['ban_user'].format(username))
        else:
            await bot.send_message(user_id, dct['dont_have_perm'])
    except telebot.apihelper.ApiException as e:
        print(e)


@bot.message_handler(commands=['unban'])
async def unban_admin_command(message):
    try:
        user_id = message.chat.id

        with open(admin_id_txt, 'r') as file:
            admin_id = file.readline()

        if user_id == int(admin_id):
            username = await clean_text(message.text, '/unban')
            unban_by_admin(username)
            await bot.send_message(int(admin_id), dct['unban_user'].format(username))
        else:
            await bot.send_message(user_id, dct['dont_have_perm'])
    except telebot.apihelper.ApiException as e:
        print(e)


@bot.message_handler(commands=['del_task'])
async def delete_task_admin_command(message):
    try:
        user_id = message.chat.id

        with open(admin_id_txt, 'r') as file:
            admin_id = file.readline()

        if user_id == int(admin_id):
            task_id = await clean_text(message.text, '/del_task')
            delete_order_by_admin(task_id)
            await bot.send_message(int(admin_id), dct['del_task'].format(task_id))
        else:
            await bot.send_message(user_id, dct['dont_have_perm'])
    except telebot.apihelper.ApiException as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    if call.data == "start_apply":
        user_id = call.message.chat.id
        if check_verification(user_id) == 1:

            with open(admin_username_txt, 'r') as file:
                admin_usrname = file.readline()
                link_to_chat = 'https://t.me/' + admin_usrname

            button_list1 = [
                types.InlineKeyboardButton(btn['admin_contact'], url=link_to_chat),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['create_order'], callback_data="create_order"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=dct['verif_menu'], reply_markup=reply_markup)

        elif check_verification(user_id) == 2:
            with open(admin_username_txt, 'r') as file:
                admin_usrname = file.readline()
                link_to_chat = 'https://t.me/' + admin_usrname

            button_list1 = [
                types.InlineKeyboardButton(btn['admin_contact'], url=link_to_chat),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=dct['bloced_user'], reply_markup=reply_markup)
        else:
            if get_verif_status_menu(user_id) == 1:
                button_list2 = [
                    types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                ]

                reply_markup2 = types.InlineKeyboardMarkup([button_list2])

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=dct["wait"],
                                            reply_markup=reply_markup2)
            else:
                update_user_menu_status(user_id, 1)
                user_twitter = await data_clean(get_user_info(user_id))


                button_list1 = [
                    types.InlineKeyboardButton(btn['user_twitter'], callback_data="user_twitter"),
                    ]
                button_list2 = [
                    types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
                ]
                button_list3 = [
                    types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                ]

                reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3])

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=dct['profile'].format(user_twitter),
                                            reply_markup=reply_markup)

    elif call.data == "user_twitter":
        user_id = call.message.chat.id
        update_user_menu_status(user_id, 2)
        button_list1 = [
            types.InlineKeyboardButton(btn['cancel'], callback_data="cancel"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['twitter_entry'], reply_markup=reply_markup)

    elif call.data == "create_order":
        user_id = call.message.chat.id

        if get_task_id_completed(user_id) == True:
            button_list1 = [
                types.InlineKeyboardButton(btn['creation_of_task'], callback_data="creation_task"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['back_to_verif_menu'], callback_data="back_to_verif_menu"),
            ]

            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=dct['create_task'], reply_markup=reply_markup)
        else:
            await bot.send_message(chat_id=call.message.chat.id, text=dct['complete_other_tasks'])

    elif call.data == "creation_task":
        user_id = call.message.chat.id

        if order_create_status(user_id) == 1:
            update_user_menu_status(user_id, 4)
            uniq_order_id = await random_order_number_generation()
            pre_create_order(uniq_order_id, user_id)

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=dct['link_entry'])
        else:
            await bot.send_message(user_id, dct['error_create_task'])

    elif call.data == "back_to_verif_menu":
        user_id = call.message.chat.id

        with open(admin_username_txt, 'r') as file:
            admin_usrname = file.readline()
            link_to_chat = 'https://t.me/' + admin_usrname

        button_list1 = [
            types.InlineKeyboardButton(btn['admin_contact'], url=link_to_chat),
        ]
        button_list2 = [
            types.InlineKeyboardButton(btn['create_order'], callback_data="create_order"),
        ]
        button_list3 = [
            types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['verif_menu'], reply_markup=reply_markup)

    elif call.data == "cancel":
        user_id = call.message.chat.id
        update_user_menu_status(user_id, 1)

        user_twitter = await data_clean(get_user_info(user_id))

        button_list1 = [
            types.InlineKeyboardButton(btn['user_twitter'], callback_data="user_twitter"),
        ]
        button_list2 = [
            types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
        ]
        button_list3 = [
            types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
        ]

        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['profile'].format(user_twitter),
                                    reply_markup=reply_markup)

    elif call.data == "start":
        user_id = call.message.chat.id
        update_user_menu_status(user_id, 0)

        button_list1 = [
            types.InlineKeyboardButton(btn['start_apply'], callback_data="start_apply"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        menu_message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                   text=dct["start"],
                                                   reply_markup=reply_markup)
        menu_id = menu_message.message_id
        add_start_menu_id(user_id, menu_id)

    elif call.data == "send_apply":
        user_id = call.message.chat.id
        username = call.message.chat.username

        user_twitter = get_user_info(user_id)
        add_app_number(user_id, await apply_number_generation())
        user_app_number = get_number_app(user_id)

        button_list1 = [
            types.InlineKeyboardButton(btn['accept_app'], callback_data="accept"),
            types.InlineKeyboardButton(btn['decline_app'], callback_data="decline"),
        ]
        reply_markup1 = types.InlineKeyboardMarkup([button_list1])

        button_list2 = [
            types.InlineKeyboardButton(btn['start_apply'], callback_data="start_apply"),
        ]

        reply_markup2 = types.InlineKeyboardMarkup([button_list2])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["wait"],
                                    reply_markup=reply_markup2)

        with open(admin_id_txt, 'r') as file:
            admin_id = file.readline()
            message = await bot.send_message(admin_id, dct["users_apply"].format(user_app_number, username, user_twitter[0]), reply_markup=reply_markup1)
            update_verif_status_menu(user_id, 1)
            update_user_menu_status(user_id, 10)
            message_id = message.message_id
            user_message_id(user_id, message_id)

    elif call.data == "accept":
        message_id = call.message.message_id
        user_id = get_user_id(message_id)

        user_twitter = get_user_info(user_id)
        user_app_number = get_number_app(user_id)

        update_verif_status_menu(user_id, 2)
        verification_status(user_id, 1)
        add_user_id_to_user_task_table(user_id)

        await bot.send_message(user_id, dct['once_congrat_verif'])

        list_of_order = get_orders_by_date()
        if len(list_of_order) > 0:
            for order_id in list_of_order:
                order_type = await get_random_order_for_task()

                busy_users = get_user_completed_list(order_id)

                if str(user_id) not in busy_users:
                    if order_type == 1:

                        twitter_link = get_twitter_link(order_id)

                        button_list1 = [
                            types.InlineKeyboardButton(btn['fullfill_order'], callback_data="press_complete_button"),
                        ]
                        reply_markup = types.InlineKeyboardMarkup([button_list1])
                        task_message = await bot.send_message(user_id, text=dct["order_notification_like"].format(order_id, twitter_link),
                                               reply_markup=reply_markup)
                        task_id = task_message.message_id
                        add_task_id_to_user_task_table(user_id, task_id)
                        add_user_in_task_order(order_id, user_id)
                    elif order_type == 2:

                        twitter_link = get_twitter_link(order_id)

                        button_list1 = [
                            types.InlineKeyboardButton(btn['fullfill_order'], callback_data="press_complete_button"),
                        ]
                        reply_markup = types.InlineKeyboardMarkup([button_list1])
                        task_message = await bot.send_message(user_id, text=dct["order_notification_like_repost"].format(order_id, twitter_link),
                                               reply_markup=reply_markup)
                        task_id = task_message.message_id
                        add_task_id_to_user_task_table(user_id, task_id)
                        add_user_in_task_order(order_id, user_id)
                    elif order_type == 3:

                        twitter_link = get_twitter_link(order_id)

                        button_list1 = [
                            types.InlineKeyboardButton(btn['fullfill_order'], callback_data="press_complete_button"),
                        ]
                        reply_markup = types.InlineKeyboardMarkup([button_list1])
                        task_message = await bot.send_message(user_id, text=dct["order_notification_like_com"].format(order_id, twitter_link),
                                               reply_markup=reply_markup)
                        task_id = task_message.message_id
                        add_task_id_to_user_task_table(user_id, task_id)
                        add_user_in_task_order(order_id, user_id)

        set_order_create_status(user_id, 1)

        username = get_username(message_id)
        link_to_chat = 'https://t.me/' + username

        button_list1 = [
            types.InlineKeyboardButton(btn['contact'], url=link_to_chat),
        ]

        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["users_apply_accepted"].format(user_app_number, username, user_twitter[0]),
                                    reply_markup=reply_markup)

    elif call.data == "decline":
        message_id = call.message.message_id
        user_id = get_user_id(message_id)
        user_twitter = get_user_info(user_id)
        user_app_number = get_number_app(user_id)


        button_list1 = [
            types.InlineKeyboardButton(btn['decline_reason1'], callback_data="decline_reason1"),
        ]
        button_list2 = [
            types.InlineKeyboardButton(btn['decline_reason2'], callback_data="decline_reason2"),
        ]

        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["users_apply_declined"].format(user_app_number, user_twitter[0]),
                                    reply_markup=reply_markup)

    elif call.data == "press_complete_button":
        user_id = call.message.chat.id
        task_id = call.message.message_id
        add_task_id_to_user_task_completed(user_id, task_id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == "decline_reason1":
        message_id = call.message.message_id
        user_id = get_user_id(message_id)
        user_twitter = get_user_info(user_id)
        user_app_number = get_number_app(user_id)

        update_verif_status_menu(user_id, 3)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["users_apply_declined"].format(user_app_number, user_twitter[0]))

        await bot.send_message(chat_id=user_id, text=dct['deacline_reason1'])

    elif call.data == "decline_reason2":
        message_id = call.message.message_id
        user_id = get_user_id(message_id)
        user_twitter = get_user_info(user_id)
        user_app_number = get_number_app(user_id)

        update_verif_status_menu(user_id, 3)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["users_apply_declined"].format(user_app_number, user_twitter[0]))

        await bot.send_message(chat_id=user_id, text=dct['deacline_reason2'])


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    user_id = message.chat.id
    if check_user_menu_status(user_id) == 2:
        twitter_id = message.text
        twitter_id_entry(user_id, twitter_id)
        update_user_menu_status(user_id, 1)

        old_menu = check_start_menu_id(user_id)
        if old_menu:
            try:
                await bot.delete_message(message.chat.id, old_menu)
            except:
                pass

        user_twitter = await data_clean(get_user_info(user_id))

        button_list1 = [
            types.InlineKeyboardButton(btn['user_twitter'], callback_data="user_twitter"),
        ]
        button_list2 = [
            types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
        ]
        button_list3 = [
            types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
        ]

        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3])

        menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_twitter),reply_markup=reply_markup)
        menu_id = menu_message.message_id
        add_start_menu_id(user_id, menu_id)

    elif check_user_menu_status(user_id) == 4:
        twitter_link = await check_twitter_link(message.text)
        if twitter_link:
            confirm_create_order(user_id, message.text)
            update_user_menu_status(user_id, 1)
            old_menu = check_start_menu_id(user_id)
            if old_menu:
                try:
                    await bot.delete_message(message.chat.id, old_menu)
                except:
                    pass

            button_list1 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])
            menu_message = await bot.send_message(message.chat.id, text=dct['succ_create_order'], reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)
            set_order_create_status(user_id, 0)
        else:
            del_pre_create_order(user_id)
            update_user_menu_status(user_id, 1)
            old_menu = check_start_menu_id(user_id)
            if old_menu:
                try:
                    await bot.delete_message(message.chat.id, old_menu)
                except:
                    pass

            button_list1 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])
            menu_message = await bot.send_message(message.chat.id, text=dct['invalid_link'], reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)


@cached(cache)
async def order_create_status_check():
    while True:
        try:
            verif_users = get_verified_users_ids()
            await asyncio.sleep(0.1)

            for user_id in verif_users:
                old_date_str = get_date_last_create(user_id)
                if old_date_str != None:
                    await asyncio.sleep(0.1)
                    try:
                        old_date = datetime.strptime(old_date_str, "%d/%m/%y")

                        current_date = datetime.now()
                        current_date_str = current_date.strftime("%d/%m/%y")

                        time_difference = current_date - old_date
                        if time_difference >= timedelta(days=7) and order_create_status(user_id) == 0:
                            if get_task_id_completed(user_id) == True:
                                set_order_create_status(user_id, 1)
                                await bot.send_message(user_id, text=dct['update_create_status'])
                    except:
                        pass
        except telebot.apihelper.ApiException as e:
            print(e)
        cache.clear()
        await asyncio.sleep(10)


@cached(cache)
async def orders_mailing():
    while True:
        try:
            orders = get_active_orders()

            users = get_verified_users()

            await asyncio.sleep(0.1)
            for user_id in users:
                for order_id in orders:
                    order_type = await get_random_order_for_task()

                    busy_users = get_user_completed_list(order_id)

                    if str(user_id) not in busy_users:
                        await asyncio.sleep(0.1)
                        if order_type == 1:

                            twitter_link = get_twitter_link(order_id)

                            button_list1 = [
                                types.InlineKeyboardButton(btn['fullfill_order'], callback_data="press_complete_button"),
                            ]
                            reply_markup = types.InlineKeyboardMarkup([button_list1])

                            task_message = await bot.send_message(user_id, text=dct["order_notification_like"].format(order_id, twitter_link), reply_markup=reply_markup)
                            task_id = task_message.message_id
                            add_task_id_to_user_task_table(user_id, task_id)
                            add_user_in_task_order(order_id, user_id)
                        elif order_type == 2:

                            twitter_link = get_twitter_link(order_id)

                            button_list1 = [
                                types.InlineKeyboardButton(btn['fullfill_order'], callback_data="press_complete_button"),
                            ]
                            reply_markup = types.InlineKeyboardMarkup([button_list1])

                            task_message = await bot.send_message(user_id, text=dct["order_notification_like_repost"].format(order_id, twitter_link), reply_markup=reply_markup)
                            task_id = task_message.message_id
                            add_task_id_to_user_task_table(user_id, task_id)
                            add_user_in_task_order(order_id, user_id)
                        elif order_type == 3:

                            twitter_link = get_twitter_link(order_id)

                            button_list1 = [
                                types.InlineKeyboardButton(btn['fullfill_order'], callback_data="press_complete_button"),
                            ]
                            reply_markup = types.InlineKeyboardMarkup([button_list1])

                            task_message = await bot.send_message(user_id, text=dct["order_notification_like_com"].format(order_id, twitter_link), reply_markup=reply_markup)
                            task_id = task_message.message_id
                            add_task_id_to_user_task_table(user_id, task_id)
                            add_user_in_task_order(order_id, user_id)
            await asyncio.sleep(0.1)
            for order_id in orders:
                change_order_status(order_id)
        except telebot.apihelper.ApiException as e:
            print(e)
        cache.clear()
        await asyncio.sleep(10)


async def main():
    bot_task = asyncio.create_task(bot.polling())
    order_mailing_task = asyncio.create_task(orders_mailing())
    order_creating_status_task = asyncio.create_task(order_create_status_check())

    await asyncio.gather(bot_task, order_mailing_task, order_creating_status_task)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
