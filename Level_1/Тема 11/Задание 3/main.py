"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import os.path
import sys

from customer_list import CustomerList

if __name__ == "__main__":

    app_path = os.path.abspath(os.path.dirname(sys.argv[0]))


    filename = os.path.join(app_path, "data.txt")

    customers_list = CustomerList()
    try:
        customers_list.open(filename)
        print("Файл \"{}\" успешно загружен. Ошибок при чтении: {}. \n".
              format(os.path.basename(customers_list.filename),
                     len(customers_list.errors)))

        print(customers_list)

        customers_list.print_report()
    except Exception as err:
        print("Ошибка программы:", err)
