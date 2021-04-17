import logging

import RequestsStampede.horde


# logging.basicConfig(level=logging.DEBUG)


def main():
    horde = RequestsStampede.horde.RetryRequest()

    response = horde.get("https://stat.us/500")

    print(response)


if __name__ == "__main__":
    main()
