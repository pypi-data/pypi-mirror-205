from miniagent.adapter import Adapter

class PaymentAdapter(Adapter):

    def approve_credit(self, card_no: str, payment_amount: int) -> tuple[int, dict]:
        rtn, message = self._adaptee.approveCredit(card_no, payment_amount)
        return rtn, message
    
    def refund_credit(self, card_no: str, approved_no: str) -> tuple[int, dict]:
        rtn, message = self._adaptee.refundCredit(card_no, approved_no)
        return rtn, message

    def get_status(self) -> int:
        return 1