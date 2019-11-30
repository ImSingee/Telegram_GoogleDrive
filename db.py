from configparser import ConfigParser
import redis

config_parser = ConfigParser()
config_parser.read('config.ini')

host = config_parser.get('REDIS', 'host')
port = config_parser.get('REDIS', 'port')
db = config_parser.get('REDIS', 'db')

r = redis.Redis(host='localhost', port=6379, db=0)


def get_key(namespace, key):
    return f'{namespace}:{key}'


def get(namespace, key, *, default=None):
    value = r.get(f'{namespace}:{key}')
    if value is not None:
        return value.decode()
    else:
        return default


def set(namespace, key, value):
    r.set(f'{namespace}:{key}', value)


def delete(namespace, key):
    r.delete(f'{namespace}:{key}')
