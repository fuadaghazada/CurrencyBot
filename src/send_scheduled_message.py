import sys
from currency_bot import sendMessage, cmd_best_helper

chat_id = sys.argv[1]
currency = sys.argv[2]

buy_or_sell = ["I want to buy {}".format(currency), "I want to sell {}".format(currency)]

cmd_best_helper(currency, buy_or_sell, buy_or_sell[0], chat_id)
cmd_best_helper(currency, buy_or_sell, buy_or_sell[1], chat_id)
