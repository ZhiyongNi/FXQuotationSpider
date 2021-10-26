# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ABCI import ABCI
from BCHO import BCHO
from BCOH import BCOH
from CCBH import CCBH
from FXQuotationSpider import FXQuotationSpider
from ICBC import ICBC

from NBCB import NBCB


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
    FXQuotationSpider().QuotationSpiderCommand('start')

# ABCIInstance = ABCI()
# ABCIInstance.setSleepTime(5)
# ABCIInstance.getQuotation()
