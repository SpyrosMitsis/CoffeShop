import csv
import os
from datetime import datetime
from uuid import uuid4


def place_order(user):
    """
    takes inputs from the user for details about the order and stores them
    in a dictionary

    :param user: employee at the coffee shop to identify who placed the
    order 
    :return: a dictionary with all the values enter with a unique id
    in the form of xxxx-xxxxxxxx where the first four character identify the
    employee and the rest the customer
    """

    user_id = user.get("uuid")

    dictionary = {"customer_name": input("Enter customer name\n> "),
                  "customer_address": input("Enter customer address\n> "),
                  "date": get_date(),
                  "total": get_total()
                  }

    dictionary["UUID"] = user_id + "-" + customer_id(
        dictionary["customer_name"], dictionary["customer_address"])

    return dictionary


def get_total():
    """
    prompts user for the amount in the order, checks if the input was left
    empty and checks if the value entered is a float type :return: the total
    cast as a float
    """

    total = input("Enter total amount of order\n> ")
    if not total:
        print("total field cannot be empty!")
        return get_total()

    try:
        total = float(total)
    except ValueError:
        print("total field should be a numeric value!")
        return get_total()

    return total


def get_date():
    """
    Prompts the user for a date in DDMMYY format and if left empty enter the
    current date taken from the date library :return: the date in a DDMMYY
    format
    """
    date = input("Enter date (leave blank for today's date)\n> ")
    if not date:
        date = datetime.now().strftime("%d%m%y")

    if (not date.isnumeric()) | (len(date) != 6):
        print("Date should follow the DDMMYY format!")
        return get_date()

    return date


def number_of_orders_by_customer(cust_id, dic_list):
    """
    Prints the sum of the orders from a specific customer

    :param cust_id: is the customer id used to filter the orders
    :param dic_list: is the list of dictionaries which is how the application
    handles orders. :return: The sum of orders made by a specific customer
    """
    count = 0
    customer_name = ""

    for i in dic_list:
        if i.get("UUID")[5:] == cust_id:
            if customer_name == "":
                customer_name = i.get("customer_name")
            count += 1

    return count


def number_of_orders_by_date(date, dic_list):
    """
    Prints the sum of the orders from a specific date

    :param date: is the parameter used to filter the orders
    :param dic_list: is the list of dictionaries which is how the
    application handles orders.
    :return: The sum of orders made by a specific customer
    """
    count = 0

    for i in dic_list:
        if i.get("date") == date:
            count += 1
    return count


# the order_printer function is not used in the main()
def order_printer(dic_list):
    """
    prints orders.

    :param dic_list: is the list of dictionaries which is how the
    application handles orders.
    """

    if not dic_list:
        print("no order placed")
        return
    else:
        name_key, addr_key, date_key, total_key, uuid_key = dic_list[0].keys()

        print("{:<20} {:<20} {:<20} {:<20} {:<20}".format(name_key, addr_key,
                                                          date_key, total_key,
                                                          uuid_key))

        for i in dic_list:
            customer_name, customer_address, date, total, uuid_value = i.values()
            print("{:<20} {:<20} {:<20} {:<20} {:<20}".format(customer_name,
                                                              customer_address,
                                                              date, total,
                                                              uuid_value))
            # print(list(i.values()))


def customer_id(customer_name, address):
    """
    Creates a unique identifier for a customer, To ensure that this
    identifier is unique it stores all customer data inside a
    customer_list.csv file anc checks if the customer has already placed an
    order. If so the customer id gets retrieved from the customer_list.csv
    file instead of generating a brand new one.

    :param customer_name: this parameter is passed to ensure that the
    customer name is inside the csv file
    :param address: this parameter is
    passed to ensure that the customer name is inside the csv file
    :return: a unique customer id
    """

    customer = {"customer_name": customer_name,
                "address": address
                }

    keys = ["customer_name", "address", "UUID"]

    if os.path.isfile("./data/customer_list.csv"):
        with open("data/customer_list.csv", "r+", newline="",
                  encoding="utf-8") as csv_file:
            dict_reader = csv.DictReader(csv_file, keys)
            customer_list = list(dict_reader)

            for i in customer_list:
                if customer_name == i.get("customer_name") \
                        and address == i.get("address"):
                    return i.get("UUID")
                else:
                    continue

            customer["UUID"] = uuid4().hex[:8]
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writerow(customer)
        return customer.get("UUID")

    with open("data/customer_list.csv", "w", newline="",
              encoding="utf-8") as csv_file:
        customer["UUID"] = uuid4().hex[:8]
        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        dict_writer.writerow(customer)
    return customer.get("UUID")


def total_amount_of_orders_printer(dic_list, customer_day="all"):
    """
    Prints total amount of orders depending on the customer_day parameter

    :param dic_list: is the list of dictionaries which is how the
    application handles orders.
    :param customer_day: this parameter is used
    as a filter when calculating the total amount of orders. The default
    state is "all" that means that if left blank it is not going to filter
    the dictionary list and is going to print the sum of all the orders
    regardless of date or customer. If the length of the parameter is 6 that
    means that the program is dealing with a date, so It's going to filter
    the orders by date. If the parameter length is 8 that means that the
    program is dealing with a customer_id which is always 8 character long
    :return: The sum of the orders depending on the customer_day parameter
    """
    sum_of_amounts = 0.0

    if customer_day == "all":
        sum_of_amounts = sum(
            (list(map(lambda amount: float(amount.get('total')), dic_list))))
        return sum_of_amounts

    elif len(customer_day) == 6:
        if not customer_day.isnumeric():
            print(
                'The Date "{}" must be a numeric value!'.format(customer_day))
            return ValueError
        for i in dic_list:
            if customer_day == i.get("date"):
                sum_of_amounts += float(i.get("total"))
        return sum_of_amounts

    elif len(customer_day) == 8:
        for i in dic_list:
            if customer_day == i.get("UUID")[5:]:
                sum_of_amounts += float(i.get("total"))
        return sum_of_amounts
    else:
        print("something went wrong, please try again!")
        return -999999


def unique_customer_printer(dic_list):
    """
    Prints a list of unique customers by utilizing the unique customer_id

    :param dic_list: is the list of dictionaries which is how the
    application handles orders.
    :return: nothing
    """
    unique_customers_id = []

    unique_customer = {}

    print("{:<20} {:<20} {:<20}".format("Customer Name", "Customer Address",
                                        "Customer UUID"))
    for i in dic_list:
        if i.get("UUID")[5:] not in unique_customers_id:
            unique_customers_id.append(i.get("UUID")[5:])
            unique_customer['name'] = i.get("customer_name")
            unique_customer['customer_address'] = i.get("customer_address")
            unique_customer['UUID'] = i.get("UUID")[5:]
            print("{:<20} {:<20} {:<20}".format(unique_customer['name'],
                                                unique_customer[
                                                    'customer_address'],
                                                unique_customer['UUID']))

    return


def unique_dates_finder(dic_list):
    """
    Makes a unique list of dates inside the dictionary
    :param dic_list: is the list of dictionaries which is how the application
    handles orders.
    :return: the list of unique dates
    """
    unique_dates = list(set(map(lambda date: date.get('date'), dic_list)))

    return unique_dates


def unique_dates_printer(dic_list):
    """
    Prints a list of dates line by line

    :param dic_list: is the list of dictionaries which is how the application
    handles orders.
    :return: nothing
    """
    unique_dates = unique_dates_finder(dic_list)
    print("Dates")

    print("\n".join(unique_dates))
    print()
    return


def txt_exporter(lst, dic_list, customer_or_user):
    """
    Makes a txt file of the list of orders filtered by the lst parameter.

    :param lst:  takes as input the list of customer names or a list
    of the users
    :param dic_list:  takes the list of orders which is a list of dictionaries
    :param customer_or_user: expects a string that indicates in which way
    the function should operate either customer mode or user mode
    :return: nothing
    """

    export = get_csv_output("txt")

    with open("export/" + export, "w", newline="", encoding="utf-8") as file:

        if customer_or_user == "customer":
            for i in lst:
                file.write(str("Name: {}\n".format(i)))

        if customer_or_user == "user":

            for i in lst:
                file.write(
                    str('orders made by "{}" \n'.format(i.get("username"))))
                name_key, addr_key, date_key, total_key, uuid_key = dic_list[
                    0].keys()
                file.write(
                    str("{:<20} {:<20} {:<20} {:<20} {:<20}\n".format(name_key,
                                                                      addr_key,
                                                                      date_key,
                                                                      total_key,
                                                                      uuid_key)))

                for j in dic_list:
                    if j.get("UUID")[:4] == i.get("uuid"):
                        customer_name, customer_address, date, total, uid = j.values()
                        file.write(
                            str("{:<20} {:<20} {:<20} {:<20} {:<20}\n".format(
                                customer_name, customer_address, date,
                                total, uid)))
                file.write("\n")
            return
        else:
            print("The customer_or_user parameter can only be 'customer' or 'user'")
            return ValueError


def order_exporter_csv(dic_list):
    """
    Exports list of dictionaries in a csv file


    :param dic_list:  takes the list of orders which is a list of dictionaries
    :return: nothing
    """
    export = get_csv_output()

    order_keys = list(dic_list[0].keys())

    with open("export/" + export, "a", newline="",
              encoding="utf-8") as csv_file:
        dict_writer = csv.DictWriter(csv_file, order_keys)
        if os.stat("export/" + export).st_size == 0:
            dict_writer.writeheader()
        dict_writer.writerows(dic_list)

    return


def customer_txt(dic_list):
    """
    Prints a unique list of un customer names in a txt file with the format
    Name: (customer_name) A set of customer ids is made from the dict list
    parameter. A dictionary of customer ids as keys and customer names as
    values is made. The values(names) are passed to the txt_exporter
    function to get exported into a txt file

    :param dic_list:  takes the list of orders which is a list of dictionaries
    :return: nothing
    """

    unique_customer_id = set(
        map(lambda customer_ident: customer_ident.get("UUID")[5:], dic_list))
    unique_names = {i["UUID"][5:]: i["customer_name"] for i in dic_list if
                    i.get("UUID")[5:] in unique_customer_id}
    txt_exporter(list(unique_names.values()), dic_list, "customer")

    return


def user_txt(dic_list):
    """
    Makes a txt file of  a list of orders by users that placed them. Reads
    the login.csv to take the uuid of each user and passes it to the
    txt_exporter() function

    :param dic_list: is the list of orders stored in a list of dictionaries
    :return: nothing
    """

    with open("data/login.csv", "r", encoding="utf-8") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        user_lst = list(dict_reader)

    user_lst = [{k: v for k, v in i.items() if k != 'password'} for i in
                user_lst]

    txt_exporter(user_lst, dic_list, "user")

    return


def total_amount_per_day_dictionary(dic_list, date):
    """
    Calculates the total amount of orders made in a specific date and pairs
    them in a dictionary

    :param dic_list:  takes the list of orders which is a list of dictionaries
    :param date: specified date to calculate the total
    :return: a dictionary with the date and the total amount of the date
    """
    total_per_day = {"date": date,
                     "total": "{}€".format(
                         str(total_amount_of_orders_printer(dic_list, date)))
                     }

    return total_per_day


def total_amount_orders_per_day_csv(dic_list):
    """
    Export a csv file with every date and the total amount of the orders in
    that date

    :param dic_list:  takes the list of orders which is a list of dictionaries
    :return: nothing
    """

    export = get_csv_output()

    unique_dates = unique_dates_finder(dic_list)

    list_of_dict = [total_amount_per_day_dictionary(dic_list, i) for i in
                    unique_dates]

    keys = list(list_of_dict[0].keys())

    with open("export/" + export, "w", newline="",
              encoding="utf-8") as csv_file:
        dict_writer = csv.DictWriter(csv_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dict)


def get_csv_output(csv_or_txt="csv"):
    """
    Prompts the user for file name and adds the appropriate extension
    if necessary

    :param csv_or_txt: the default values is "csv", to append .csv
    at the end of the string,
    but it can be anything. Ex. "txt", "png"
    :return: the string with the extension if not included
    """
    export = input("Enter output file name\n> ")
    if not export:
        print("Field cannot be empty!")
        return get_csv_output(csv_or_txt)

    if export[-4:] != "." + csv_or_txt:
        export = export + "." + csv_or_txt

    return export


if __name__ == "__main__":
    dict_list = [
        {'customer_name': 'mario', 'customer_address': 'W1', 'date': '270612',
         'total': '13.2',
         'UUID': 'bede-71683700'},
        {'customer_name': 'luigi', 'customer_address': 'W2', 'date': '100300',
         'total': '15.6',
         'UUID': '4677-27765000'},
        {'customer_name': 'luigi', 'customer_address': 'W2', 'date': '100300',
         'total': '43.1',
         'UUID': '4677-27765000'},
        {'customer_name': 'luigi', 'customer_address': 'W2', 'date': '270612',
         'total': '10.8',
         'UUID': '4677-27765000'},
        {'customer_name': 'peach', 'customer_address': 'W3', 'date': '151205',
         'total': '66', 'UUID': 'bede-73659850'},
        {'customer_name': 'peach', 'customer_address': 'W3', 'date': '151205',
         'total': '66', 'UUID': 'bede-73659850'},
        {'customer_name': 'peach', 'customer_address': 'W3', 'date': '151205',
         'total': '66', 'UUID': 'bede-73459850'},
        {'customer_name': 'toad', 'customer_address': 'W4', 'date': '270612',
         'total': '0.60', 'UUID': '4677-29807000'},
        {'customer_name': 'toad', 'customer_address': 'W4', 'date': '272612',
         'total': '4.60', 'UUID': '4677-29807000'}
    ]

    # number_of_orders_by_customer("27765000", dict_list)
    # print(customer_id("Jean-Paul Sartre ", "Café de Flore"))
    # print(customer_id("Jean-Paul Sartre ", "Café de Flors"))
    # print(customer_id.__doc__)
    # customer_txt(dict_list)
    # user_txt(dict_list)
    # order_exporter_csv(dict_list)
    # print(total_amount_of_orders_printer(dict_list, "100300"))
    # unique_customer_printer(dict_list)
    # print(get_date())
    # print(get_total())
    # order_printer(dict_list)
    print(total_amount_of_orders_printer(dict_list, "29807000"))
    # print(total_amount_of_orders_printer(dict_list, "100300"))
    # unique_dates_finder(dict_list)
    # unique_dates_printer(dict_list)
