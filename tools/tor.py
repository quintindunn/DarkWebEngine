import requests
from stem import Signal
from stem.control import Controller


def renew_connection():
    hashed_pwd = "HashedControlPassword 16:4885259C4E594EF260E9232AD3EBC19FFED5A7F0DF1E17E60DEA6C19D4"
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
