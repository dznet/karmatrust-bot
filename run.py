#!/usr/bin/env python3

from karmatrust import KarmaTrustBot


TELEGRAM_BOT_TOKEN = ''

bot = KarmaTrustBot(TELEGRAM_BOT_TOKEN)

if __name__ == '__main__':
  try:
    bot.start()
  except:
    bot.stop()
