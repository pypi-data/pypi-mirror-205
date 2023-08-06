from miniagent.executer import ExecuterInterface
from example.adapter.payment_adapters import PaymentAdapter
from example.adapter.printer_adapters import PrinterAdapter
from example.adapter.restserver_adapters import RESTServerAdapter
from example.dbquery.purchase_card_queries import insert_purchase

class PurchaseCard(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            printer: PrinterAdapter,
                            payment: PaymentAdapter,
                            restserver: RESTServerAdapter,
                        ) -> tuple[int, dict]:
        
        print('initial_param : ', initial_param)

        # 1. Print Image
        rtn, message = printer.print_image_file(initial_param['product_code']+'.jpg')
        print('printer.print_image_file : ', rtn, message)

        # 2. Payment
        rtn, message = payment.approve_credit(
                            initial_param['card_no'],
                            initial_param['payment_amount'])
        
        message['product_code'] = initial_param['product_code']

        # 3. Db
        insert_purchase(message)

        # 4. Restserver 
        restserver.post_purchase(
                      product_code  = message['product_code'],
                      card_no       = message['card_no'],
                      payment_amount = message['payment_amount'],
                      approved_no   = message['approved_no'],
                      approved_date = message['approved_date'],
                    )
        
        return 1, dict(message="Well Done!!!!")
