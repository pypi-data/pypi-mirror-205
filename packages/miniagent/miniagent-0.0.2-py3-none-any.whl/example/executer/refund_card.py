from miniagent.executer import ExecuterInterface
from example.adapter.payment_adapters import PaymentAdapter
from example.adapter.restserver_adapters import RESTServerAdapter
from example.dbquery.purchase_card_queries import update_purchase

class RefundCard(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            payment: PaymentAdapter,
                            restserver: RESTServerAdapter,
                        ) -> tuple[int, dict]:
        
        print('initial_param : ', initial_param)

        # 1. Refund
        rtn, message = payment.refund_credit(
                            initial_param['card_no'],
                            initial_param['approved_no'])
        
        condition = dict(approved_no = initial_param['approved_no'])

        # 3. Db
        update_purchase(message, condition)

        # 4. Restserver 
        restserver.put_refund(
                      approved_no = initial_param['approved_no'],
                      refund_no   = message['refund_no'],
                      refund_date = message['refund_date'],
                    )
        
        return 1, dict(message="Well Done!!!!")
