#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# my.karma.red bot v.0.0.2
# https://github.com/dznet/karmatrust-bot

import logging
from os import getcwd
from json import loads
from requests import Session
from sys import exc_info
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import Updater


LOG_FORMAT = '%(asctime)s %(lineno)d - %(name)s %(levelname)s: %(message)s'
LOG_PATH = '{}/{}.log'.format(getcwd(), __name__)

logger = logging.getLogger(__name__)
formatter = logging.Formatter(LOG_FORMAT)
logfile = logging.FileHandler(LOG_PATH)
logfile.setFormatter(formatter)
logfile.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(logfile)


class KarmaTrustBot():

  __instances = {}
  __query = '''query\nq{orders(first:5){edges{node{application{data}offer{data}}}}}'''
  __data = {'variables':None, 'operationName':'q', 'query':__query}
  __endpoint = 'https://my.karma.red/graphql/'

  def __init__(self, token):
    self.message = Messages()
    self.updater = Updater(token)
    self.bot = self.updater.bot.get_me()
    self.dp = self.updater.dispatcher
    self.__instances[token] = self

    self.dp.add_handler(
                CallbackQueryHandler(self.hit_link,
                                     pattern='action'
                                   )
              )
    self.dp.add_handler(
                CommandHandler('start',
                               self.greeting
                               )
              )
    self.dp.add_handler(
                CommandHandler('about',
                               self.about
                               )
              )
    self.dp.add_handler(
                CommandHandler('market',
                               self.market
                               )
              )
    self.dp.add_handler(
                CommandHandler('help',
                               self.help
                               )
              )
    self.dp.add_handler(
                MessageHandler(Filters.text,
                               self.greeting
                               )
              )

  @classmethod
  def get_instance(class_, token):
    return class_.__instances[token]

  def start(self):
    self.updater.start_polling()
    logger.info(
                self.message.bot_start(
                                   self.bot.username
                                )
            )

  def stop(self):
    self.updater.stop()
    logger.info(
                self.message.bot_stop(
                                    self.bot.username
                                )
            )

  def error(self, bot, update, error):
    logger.warning(
                self.message.bot_error(
                                    self.bot.username
                                )
            )

  def greeting(self, bot, update):
    update.message.reply_text(
                        self.message.greeting(),
                        parse_mode='Markdown'
                    )

  def help(self, bot, update):
    update.message.reply_text(
                        self.message.help(),
                        parse_mode='Markdown'
                    )

  def about(self, bot, update):
    update.message.reply_text(
                        self.message.about(),
                        parse_mode='Markdown',
                        reply_markup=self.message.keyboard()
                    )

  def market(self, bot, update):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=self.request_data(),
                     parse_mode='Markdown',
                     reply_markup=self.message.keyboard()
                    )

  def hit_link(self, bot, update):
    __hit_data = update.callback_query
    logger.info(self.message.action(__hit_data))

  def request_data(self):
    session = Session()
    response = session.post(
                          self.__endpoint,
                          data=self.__data
                        )
    result = loads(response.content)
    orders = result['data']['orders']['edges']
    message = ['Активные предложения заемщиков:\n']

    for data in orders:
      application = loads(data['node']['application']['data'])
      offer = loads(data['node']['offer']['data'])

      message.append(
                '*{companyName}*\nСумма: {maxValue} ₽'.format(
                                                           **application
                                                         )
              )
      message.append(
                'Ставка: {interestRate} %\nСрок займа:{duration} мес.\n'.format(
                                                                             **offer
                                                                           )
              )
    return '\n'.join(message)


class Messages():

  __start = '''Приветствую! Это бот платформы p2p-кредитования `my.karma.red`
\nМои команды:\n/about - коротко о проекте\n/market - активные заявки на займ
/help - ответы на частые вопросы и поддержка'''

  __about = '''Карма – платформа p2p-кредитования, где каждый может \
инвестировать в живой бизнес. Минуя банки и бумажную \
волокиту, из любой точки планеты:\n- минимальная инвестиция 7000 рублей,
- доход до 24% годовых,\n- e-contract, имеющий юридическую силу.
\nСреди заемщиков только проверенные предприниматели, \
только живой бизнес. Мы хотим чтобы деньги работали и верим \
что экономика – это люди, а не банки и системы.
\nПрисоединяйтесь: my.karma.red
\nВся самая актуальная информация для инвесторов в специальном \
(Telegram-чате)[https://t.me/karmainvest]'''

  __help = '''[Ответы на частые вопросы](https://karmatrust.ru/#faq)
\n\nНаш e-mail: help@karma.red\nТелефон: +7 495 134 24 70
\n\n[Telegram-чат для инвесторов](https://t.me/karmainvest)'''

  def __init__(self):
    super().__init__()

  def about(self):
    return self.__about

  def greeting(self):
    return self.__start

  def help(self):
    return self.__help

  def hit_market_link(self, data):
    #datastr = '{message_id} {date}'.format(**data)
    #print(message)
    #data.message.message_id,
    #data.message.from_user,
    #data.message.date
    return 'datastr'

  def bot_start(self, bot_username):
    return '@{} running.'.format(
                               bot_username
                            )

  def bot_stop(self, bot_username):
    return '@{} shutdown ...'.format(
                                   bot_username
                                )

  def bot_error(self, bot_username):
    return '@{} update error {}.'.format(
                                      bot_username,
                                      error
                                    )
  def keyboard(self):
    button = InlineKeyboardButton(
                               text='Показать ещё',
                               callback_data='action',
                               url='https://my.karma.red/market'
                            )
    return InlineKeyboardMarkup([[button]])

# dzNetwork 2018
