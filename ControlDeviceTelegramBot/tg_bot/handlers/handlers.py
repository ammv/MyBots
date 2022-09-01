from .menu import register_menu
from .add_device import register_add_device
from .devices import register_device
from .control_device import register_control_device

def register_handlers(dp):
    register_menu(dp)
    register_add_device(dp)
    register_device(dp)
    register_control_device(dp)
    
