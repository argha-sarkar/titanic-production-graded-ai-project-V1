import sys

import pytest

from src.exception.exception import (
    CustomException
)


def test_custom_exception():

    with pytest.raises(CustomException):

        try:

            10 / 0

        except Exception as error:

            raise CustomException(
                error,
                sys
            )