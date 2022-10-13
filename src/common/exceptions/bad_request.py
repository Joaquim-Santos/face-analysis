from common.exceptions.abstract_exception import AbstractException


class BadRequest(AbstractException):

    def __init__(self, message: str = 'Requisição inválida.', status_code: int = 400,
                 payload: dict = None) -> None:
        """
            O servidor não entendeu a requisição, pois está com uma sintaxe inválida.

            Parameters
            ----------
            message: str
                Messagem a ser exibida quando a exceção é lançada.
                Default: Campo não pode ser branco.

            status_code: int
                Código de status HTTP.
                Default: 400

            payload: dict
                Dados de payload para envio na resposta da exceção.
        """
        super().__init__(message, status_code, payload)
