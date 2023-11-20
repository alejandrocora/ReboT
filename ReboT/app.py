import argparse
import getpass

from ReboT.utils.selaux import *
from ReboT.utils.xaccount import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--firefox', dest='browser', default=False, action='store_false', help='Use Firefox.')
    parser.add_argument('--chrome', dest='browser', action='store_true', help='Use Chrome.')
    parser.add_argument('--headless', dest='mode', default=False, action='store_true', help='Use headless mode.')
    parser.add_argument('--username', required=True, dest='username', help='Username for login.')
    parser.add_argument('--password', dest='password', help='Password for login.')
    parser.add_argument('tweets',  metavar='tweets', type=str, nargs='+', help='Tweet URLs separated by spaces.')
    parser.add_argument('--rt', dest='rt', action='store_true', help='RT Tweet. Used if no instruction is given.')
    parser.add_argument('--like', dest='like', action='store_true', help='Like Tweet.')
    args = parser.parse_args()
    if not args.password:
        password = getpass.getpass('Account password: ')
    else:
        password = args.password
    if args.browser:
        driver = chrome(args.mode)
    else:
        driver = firefox(args.mode)
    bot = XAccount(driver, args.username, password)
    bot.login()
    for tweet in args.tweets:
        if args.like:
            if args.rt:
                bot.rt_like(tweet)
            else:
                bot.like(tweet)
        else:
            bot.rt(tweet)
    driver.close()


if __name__ == '__main__':
    main()