import requests
from stem import Signal
from stem.control import Controller


def renew_connection():
    hashed_pwd = "XXXX"
    with Controller.from_port(port=9151) as controller:
        controller.authenticate(password=hashed_pwd)
        controller.signal(Signal.NEWNYM)


def new_session() -> requests.session:
    s = requests.session()
    s.proxies = {
        'http': 'socks5h://localhost:9150',
        'https': 'socks5h://localhost:9150'
    }
    return s
