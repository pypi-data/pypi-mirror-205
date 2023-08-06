from datetime import datetime
from miniagent.executer import ExecuterInterface
from example.adapter.payment_adapters import PaymentAdapter
from example.adapter.printer_adapters import PrinterAdapter
from example.adapter.restserver_adapters import RESTServerAdapter
from example.dbquery.scheduler_check_queries import add_all_device_health

class DeviceHealth(ExecuterInterface):

    def execute_command(self,
                            initial_param: dict,
                            printer: PrinterAdapter,
                            payment: PaymentAdapter,
                            restserver: RESTServerAdapter,
                        ) -> tuple[int, dict]:
        
        checked_date = datetime.now()

        val_list = []
        for obj in [printer, payment, restserver]:
            val_dict = \
                dict(
                    adapter_name = obj.get_adapter_name(),
                    adaptee_name = obj.get_adaptee_name(),            
                    is_healthy = 'YES' if obj.get_status() else 'NO',
                    checked_date = checked_date
                )
            val_list.append(val_dict)

        add_all_device_health(val_list)

        return 1, dict(message="Well Done!!!!")
