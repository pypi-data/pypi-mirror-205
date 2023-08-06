from miniagent.adapter import Adapter

class PrinterAdapter(Adapter):

    def print_image_file(self, param):        
        return 1, self._adaptee.printImageFile(param)

    def get_printer_info(self):
        return self._adaptee.getPrinterInfo()
    
    def release_printer(self):
        return self._adaptee.releasePrinter()
    
    def get_status(self) -> int:
        return self._adaptee.getPrinterStatus()