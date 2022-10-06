

class AbstractException(Exception):
    """
        Classe abstrata para criar exceções.

        Parameters
        ----------
        message: str
            Messagem a ser exibida quando a exceção é lançada.
            Default: Ocorreu algum problema ao processar a requisição.

        status_code: int
            Código de status HTTP.
            Default: 500

        payload: dict
            Dados de payload para envio na resposta da exceção.
    """
    def __init__(self, message: str = 'Exceção abstrata.', status_code: int = 500,
                 payload: dict = None) -> None:

        super().__init__(message)
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self) -> dict:
        """
            Método para criar um dicionário a partir do objedo da exceção.

            Returns
            ----------
            dict
                {'error_message': self.message,
                 'payload': self.payload}
        """
        return {
            'error_message': self.message,
            'payload': self.payload
        }
