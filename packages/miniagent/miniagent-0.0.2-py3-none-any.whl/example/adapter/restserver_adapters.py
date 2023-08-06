from datetime import datetime
from miniagent.adapter import Adapter

class RESTServerAdapter(Adapter):

    def post_purchase(self, 
                      product_code: str,
                      card_no: str, 
                      payment_amount: int,
                      approved_no: str,
                      approved_date: datetime, 
                      ) -> tuple[int, dict]:
        
        return self._adaptee.postPurchase(
                        product_code,
                        card_no, 
                        payment_amount,
                        approved_no,
                        approved_date 
                        )
    
    def put_refund(self, 
                      approved_no: str,
                      refund_no: str,
                      refund_date: datetime, 
                      ) -> tuple[int, dict]:
        
        return self._adaptee.putPurchase(
                        approved_no,
                        refund_no,
                        refund_date 
                        )
    
    def get_status(self) -> int:
        return 1