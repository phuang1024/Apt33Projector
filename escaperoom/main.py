import argparse
from threading import Thread

from display import Display


def main():
    #parser = argparse.ArgumentParser()
    #args = parser.parse_args()

    display = Display()

    threads = []

    for thread in threads:
        thread.start()
    display.start()


if __name__ == "__main__":
    main()
