import sys

from src.exception.exception import (
    CustomException
)


def divide():

    try:

        number = 10 / 0

        return number

    except Exception as error:

        raise CustomException(
            error,
            sys
        )


if __name__ == "__main__":

    divide()