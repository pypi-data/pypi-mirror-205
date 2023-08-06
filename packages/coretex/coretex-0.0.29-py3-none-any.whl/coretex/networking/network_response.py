from typing import Optional, Final
from typing_extensions import Self
from enum import IntEnum

import logging

from requests import Response


class HttpCode(IntEnum):

    """
        A enum class which represents code for specific http errors
    """

    unauthorized        = 401

    internalServerError = 500
    serviceUnavailable  = 503


class ErrorHandling:

    """
        A class which represents NetworkResponse error
    """

    def __init__(self, response: Response, endpoint: str):
        self.__statusCode: int = response.status_code
        self.__message: str = response.text
        self.__endpoint: str = endpoint
        self.__result: bool = response.ok

    def returnIfError(self) -> Optional[Self]:
        """
            Returns
            -------
            Optional[Self] -> ErrorHandling object if there is client/server error, None if not
        """

        return None if self.__result else self

    def toString(self) -> str:
        """
            Converts ErrorHandling object to string representation

            Returns
            -------
            str -> string describing the ErrorHandling object
        """

        return f"Endpoint: {self.__endpoint}, Code: {self.__statusCode}, Message: {self.__message}"


class NetworkResponse:

    """
        Represents Coretex backend response to network request

        Properties
        ----------
        response : Response
            API response
        endpoint : endpoint
            name of API endpoint
        json : Any
            response in json format

    """

    def __init__(self, response: Response, endpoint: str):
        self.raw: Final = response
        self.headers: Final = response.headers

        try:
            self.json = response.json()
        except ValueError:
            self.json = {}

        self.__error = ErrorHandling(response, endpoint).returnIfError()
        if self.__error is not None:
            logging.getLogger("coretexpylib").debug(f">> [Coretex] Request failed -- {self.__error.toString()}")

        logging.getLogger("coretexpylib").debug(f">> [Coretex] Request response: {self.json}")

    @property
    def statusCode(self) -> int:
        return self.raw.status_code

    def hasFailed(self) -> bool:
        """
            Checks if request has failed

            Returns
            -------
            bool -> True if request has failed, False if request has not failed
        """

        return self.__error is not None

    def isUnauthorized(self) -> bool:
        """
            Checks if request was unauthorized

            Returns
            -------
            bool -> True if status code is 401 and request has failed, False if not
        """

        return self.statusCode == HttpCode.unauthorized and self.hasFailed()
