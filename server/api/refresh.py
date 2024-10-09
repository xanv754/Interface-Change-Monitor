from controllers.element import ElementController

if __name__ == "__main__":
    print("Refresh ...")
    status = ElementController.load_elements()
    if status: print("Updated database.")
    else: print("Failed to update.")