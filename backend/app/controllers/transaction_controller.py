class TransactionController:
    def __init__(self, service):
        self.service = service

    def create_transaction(self, data):
        return self.service.create_transaction(data)

    def list_transactions(self):
        return self.service.list_transactions()