from src.common.exceptions.abstract_exception import AbstractException


class GenericException(AbstractException):
    def __init__(
        self,
        message: str = "Ocorreu um comportamento inesperado.",
        status_code: int = 500,
        payload: dict = None,
    ) -> None:
        """
        Exceção para propósito genérico, quando não há nenhuma específica para uso, acusando um
        erro interno no servidor

        Parameters
        ----------
        message: str
            Messagem a ser exibida quando a exceção é lançada.
            Default: Campo não pode ser branco.

        status_code: int
            Código de status HTTP.
            Default: 500

        payload: dict
            Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)
