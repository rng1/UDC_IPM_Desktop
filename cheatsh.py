from model import Model
from view import View
from controller import Controller


if __name__ == '__main__':
    controller = Controller(Model(), View())
    controller.main()