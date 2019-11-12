import logging
from configparser import ConfigParser

from bastion import init_bastion


def main():
    logging.basicConfig(level=logging.WARN)
    config = ConfigParser()
    config.read('config.ini')

    bastion = init_bastion(config)

    bastion.run()

if __name__ == '__main__':
    main()
