from .resources.token import Token
from .resources.invoices import InvoiceClient
from .resources.shipments import ShipmentClient
from .resources.orders import OrderClient
from .resources.returns import ReturnClient


class Client(Token):

    def __init__(self, redis_hostname, redis_password=None, redis_port=None, redis_database=None,
                 redis_connection_method=None):
        super().__init__(redis_hostname, redis_password, redis_port, redis_database, redis_connection_method)

    @property
    def invoices(self):
        return InvoiceClient(self.access_token)

    @property
    def shipments(self):
        return ShipmentClient(self.access_token)

    @property
    def orders(self):
        return OrderClient(self.access_token)

    @property
    def returns(self):
        return ReturnClient(self.access_token)
