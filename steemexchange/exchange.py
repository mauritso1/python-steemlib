from steemapi.steemclient import SteemClient
from datetime import datetime
import time
from random import randint

#from grapheneextra.proposal import Proposal
#from steembase.account import PrivateKey

class NoWalletException(Exception):
    pass


class InvalidWifKey(Exception):
    pass


class WifNotActive(Exception):
    pass


class ExampleConfig() :
    #: Wallet connection parameters
    wallet_host           = "127.0.0.1"
    wallet_port           = 8091
    wallet_user           = ""
    wallet_password       = ""

    #: Witness connection parameter
    witness_url           = ""
    witness_user          = ""
    witness_password      = ""

    #: The account used here
    account               = ""
    wif                   = None


class SteemExchange(SteemClient) :
    wallet = None
    precision = {
        "STEEM" : 3,
        "VESTS" : 6,
        "SBD" : 3,
        "STMD" : 3,
    }

    def __init__(self, config, **kwargs) :
        # Defaults:
        self.safe_mode = True

        if "safe_mode" in kwargs:
            self.safe_mode = kwargs["safe_mode"]


        if "prefix" in kwargs:
            self.prefix = kwargs["prefix"]
        else:
            self.prefix = "STM"

        super().__init__(config)

    def formatTimeFromNow(self, secs=0):
        """ Properly Format Time that is `x` seconds in the future

            :param int secs: Seconds to go in the future (`x>0`) or the
                             past (`x<0`)
            :return: Properly formated time for Graphene (`%Y-%m-%dT%H:%M:%S`)
            :rtype: str

        """
        return datetime.utcfromtimestamp(time.time() + int(secs)).strftime('%Y-%m-%dT%H:%M:%S')

    def returnBalances(self):
        account = self.ws.get_account(self.config.account)
        balances = {
            "STEEM": account["balance"],
            "SBD": account["sbd_balance"],
            "VESTS": account["vesting_shares"]
        }
        return balances

    def sell(self, currencyPair, rate, amount, expiration=7 * 24 * 60 * 60, killfill=False, order_id=None):
        if self.safe_mode :
            print("Safe Mode enabled!")
            print("Please do SteemExchange(config, safe_mode=False) to remove this and execute the transaction below")
        quote_symbol, base_symbol = currencyPair.split(self.market_separator)
        if not order_id:
            order_id = randint(0, 4294967295)
        if self.rpc:
            transaction = self.rpc.create_order(
                self.config.account,
                order_id,
                '{:.{prec}f}'.format(amount * rate, prec=self.precision[base_symbol]) + " " + base_symbol,
                '{:.{prec}f}'.format(amount, prec=self.precision[quote_symbol]) + " " + quote_symbol,
                killfill,
                expiration,
                not (self.safe_mode)
            )
        return transaction

    def buy(self, currencyPair, rate, amount, expiration=7 * 24 * 60 * 60, killfill=False, order_id=None):
        if self.safe_mode :
            print("Safe Mode enabled!")
            print("Please do SteemExchange(config, safe_mode=False) to remove this and execute the transaction below")
        quote_symbol, base_symbol = currencyPair.split(self.market_separator)
        if not order_id:
            order_id = randint(0, 4294967295)
        if self.rpc:
            transaction = self.rpc.create_order(
                self.config.account,
                order_id,
                '{:.{prec}f}'.format(amount * rate, prec=self.precision[quote_symbol]) + " " + quote_symbol,
                '{:.{prec}f}'.format(amount, prec=self.precision[base_symbol]) + " " + base_symbol,
                killfill,
                expiration,
                not (self.safe_mode)
            )
        return transaction

    def cancel_order(self, oid):
        if self.safe_mode :
            print("Safe Mode enabled!")
            print("Please do SteemExchange(config, safe_mode=False) to remove this and execute the transaction below")
        if self.rpc:
            transaction = self.rpc.cancel_order(self.config.account, oid, not self.safe_mode)
        return transaction

