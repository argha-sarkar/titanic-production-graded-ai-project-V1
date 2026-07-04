"""
Project-wide custom exception.
"""

import sys
from pathlib import Path


class CustomException(Exception):
    """
    Custom exception that enriches the original exception
    with filename and line number information.
    """

    def __init__(
        self,
        error: Exception,
        error_detail: sys
    ) -> None:

        super().__init__(str(error))

        self.error_message = self._build_message(
            error,
            error_detail
        )

    @staticmethod
    def _build_message(
        error: Exception,
        error_detail: sys
    ) -> str:

        _, _, traceback = error_detail.exc_info()

        file_name = Path(
            traceback.tb_frame.f_code.co_filename
        ).name

        line_number = traceback.tb_lineno

        return (
            f"Error in file '{file_name}' "
            f"at line {line_number}: "
            f"{error}"
        )

    def __str__(self) -> str:

        return self.error_message