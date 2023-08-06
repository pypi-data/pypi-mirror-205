import sys
import inspect
import types
import abc
from importlib import import_module
from typing import TypeVar
from .common import SingletonInstane, split_class_path
from .adapter import AdapterFactory

class ExecuterInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'execute_command') and 
                callable(subclass.execute_command) or 
                NotImplemented)

    @abc.abstractmethod
    def execute_command(self, 
                        command_code: str, 
                        initial_param: dict, 
                        *args, 
                        **kwargs) -> tuple[int, dict]:
        """Execute biz logic with handles of calless and paramters"""
        raise NotImplementedError

class ExecuterFactory:

    @staticmethod
    def create_executer(class_path: str):

        package_name, class_name = split_class_path(class_path)

        print('create_executer {} {}'.format(package_name, class_name))

        package_module = sys.modules[package_name]\
                  if package_name in sys.modules else import_module(package_name)

        """
        try:    
            
            package_module = sys.modules[package_name]\
                  if package_name in sys.modules else import_module(package_name)
        
        except ImportError:
            return None
        """
        class_obj = getattr(package_module, class_name)

        if not issubclass(class_obj, ExecuterInterface):
            return None

        return class_obj()

class ExecuterCaller(SingletonInstane):
  
    def __init__(self, configure=None):
        if configure:
            self.default_adaptees = configure['DEFAULT_ADAPTEES']

    def _create_adapter(self, adapter_name: str, adaptee_name: str) -> TypeVar('T'):

        padapter = AdapterFactory.create_adapter(adapter_name)
        rtn, msg = padapter.set_adaptee(adaptee_name)

        if not rtn:
            return None
        else:    
            return padapter

    def execute_command(self, message: dict) -> dict:
        """
        {
            "command_code":"01",
            "initial_param":{
                "product_code":"00011",
                "payment_amount":50000,
            },
            "executer":"addin.executer.purchase_card.PurchaseCard",
        }
        """
        command_code = message['command_code'] if message.get('command_code') else ''
        initial_params = message['initial_param'] if message.get('initial_param') else {}
        executer_path = message['executer']

        executer = ExecuterFactory.create_executer(executer_path)

        sig = inspect.signature(executer.execute_command)

        adapters = dict()

        for param in sig.parameters.values():

            if param.name not in ['db', 'initial_param']:
                dadapter = param.annotation.__module__ +'.'+param.annotation.__name__
                dadaptee = self.default_adaptees[dadapter]
                adapter_instance = self._create_adapter(dadapter, dadaptee)
                adapters[param.name] = adapter_instance

        print('execute_command adapters :',adapters)

        from . import app

        with app.app_context():
            rtn, message = executer.execute_command(initial_params, **adapters)

        return rtn, message