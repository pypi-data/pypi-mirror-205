import logging
import os

basedir = os.path.dirname(__file__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)


class Config:
    RUM_SEED = "rum://seed?v=1&e=0&n=0&c=qOh_wTyuoKDoXmqGrP7Tfi1EAEFwTe81wZDbhEN4UKo&g=_NnW5VeXSgagNFD1VBE0tQ&k=A07OxsxC3apkq9mGTFeBGQK1aLDQ552hIjbIRZgjxaiN&s=nECW9-MqxEEmQ3sHu4_8F5boGkTsMBu8iYHf6IwweA5pUzQzT76KeQ6UT4fRLnspUnOehWxLmhB0fUvtHTqXdwA&t=F1bBbub7xqE&a=test_telegram_bot&y=group_timeline&u=http%3A%2F%2F158.69.15.98%3A8004%3Fjwt%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwIjoiZmNkOWQ2ZTUtNTc5Ny00YTA2LWEwMzQtNTBmNTU0MTEzNGI1IiwiZXhwIjoxODM5NDI0MTk1LCJuYW1lIjoiYWxsb3ctZmNkOWQ2ZTUtNTc5Ny00YTA2LWEwMzQtNTBmNTU0MTEzNGI1Iiwicm9sZSI6Im5vZGUifQ.fFyuVzMomMKEtJ_1RijpNhIaH5sa9TCLPkHCnpnROM8"
    ETH_PVTKEY = "0x5ee77ca3c261cddd6baaaa94be76f19d2a5997f2ca9921f68557e2266adeffaf"
    FEED_URL_BASE = "https://test.feed.base.one"
    FEED_TITLE = "My Feed"
    TG_USER_ID = 417326505
    TG_CHANNEL_NAME = "@hi_my_test_channel"
    TG_CHANNEL_URL = "https://t.me/hi_my_test_channel"
    TG_CHANNEL_ID = -1001869927577
    TG_BOT_TOKEN = "5847114777:AAEPNthtoyYxLUa4ywqWclMwD29vJbPcS4I"  # bot token
    TG_BOT_NAME = "@MyRumTestBot"
    # TG_GROUP_NAME = "@hi_my_test_channel_group"
    TG_GROUP_ID = -1001854966591
    DB_URL = f"sqlite:///{basedir}/test_db.sqlite"
    DB_ECHO = False
    RUM_DELAY_HOURS = -10
    RUM_POST_FOOTER = "#什么不值得买 "
    TG_REPLY_POSTURL = True
    BLACK_LIST_PUBKEYS = []
    BLACK_LIST_TGIDS = []


config = Config()
