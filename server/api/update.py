from controllers.interface import InterfaceController
from controllers.element import ElementController

if __name__ == "__main__":
    print("Loading update ...")
    status = InterfaceController.load_data()
    if status: 
        status = ElementController.load_elements()
        if status: print("Updated database.")
        else: print("Data interfaces have been updated, but the history of changes has not been updated.")
    else: print("Failed to update.")