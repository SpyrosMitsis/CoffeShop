"""
Student : Mitsis Spyridon
Course: SWE4001 Introduction to Software Development
Professor:  Dr. Sotirios Ntouskas
Year : 1
Assessment: 001
"""
import login
import order


def export_menu(dic_list):
    """
    Menu used for exporting orders in txt or csv format

    :param dic_list: is the list of dictionaries which is how the
    application handles orders.

    :return: nothing
    """
    while True:
        print("************* Export System *************")
        print("1    | Names of customers(txt)")
        print("2    | Orders entered per user(txt)")
        print("3    | All data entered(csv)")
        print("4    | Total amount of orders per day(csv)")
        print("5    | Quit")
        print("*****************************************")

        line = input("> ")
        if line == "q" or line == "quit" or line == "5":
            break
        elif line == "1":
            order.customer_txt(dic_list)
        elif line == "2":
            order.user_txt(dic_list)
        elif line == "3":
            order.order_exporter_csv(dic_list)
        elif line == "4":
            order.total_amount_orders_per_day_csv(dic_list)
        else:
            print('command "{}" is not recognised'.format(line))
            continue


def order_menu(user, orders):
    """
    Menu used for placing orders and retriving specific data.

    :param user: Is the username of the user that is loged in at the moment
    :param orders: is the list of dictionaries which is how the
    application handles orders.
    :return: nothing
    """
    print("Welcome {} !".format(user["username"]))

    while True:
        print("************* Order System *************")
        print("1    | Place order")
        print("2    | Number of orders by customer")
        print("3    | Number of orders by specific date")
        print("4    | Total amount of orders by customer")
        print("5    | Total amount of orders by specific date")
        print("6    | Total amount of all orders delivered")
        print("7    | Enter export menu")
        print("8    | Logout")
        print("****************************************")
        line = input("> ")
        if line == "1":
            orders.append(order.place_order(user))
        elif line == "2":
            order.unique_customer_printer(orders)
            customer = input("Enter customer id\n> ")
            print("{} has ordered {} time(s)".format(customer,
                                                     order.number_of_orders_by_customer(
                                                         customer, orders)))
        elif line == "3":
            order.unique_dates_printer(orders)
            date = input("Enter date in format DDMMYY\n> ")
            print("On {} there were placed {} order(s)".format(date,
                                                               order.number_of_orders_by_date(
                                                                   date,
                                                                   orders)))
        elif line == "4":
            order.unique_customer_printer(orders)
            customer_id = input("Enter customer id\n> ")
            print("The total amount of the orders for {} is {:.2f} €".format(customer_id,
                order.total_amount_of_orders_printer(orders, customer_id)))
        elif line == "5":
            order.unique_dates_printer(orders)
            date = input("Enter date in format DDMMYY\n> ")
            print("The total amount of orders on {} is {:.2f} €".format(date,
                                                                        order.total_amount_of_orders_printer(
                                                                            orders,
                                                                            date)))
        elif line == "6":
            print("The total amount for all the orders is {:.2f} €".format(
                order.total_amount_of_orders_printer(orders)))
        elif line == "7":
            export_menu(orders)
        elif line == "8" or line == "q" or line == "quit":
            print("bye", user["username"] + "!")
            break

        else:
            print('command "{}" is not recognised'.format(line))
            continue


def login_menu(orders):
    """
    Log in menu used for the user to login sign-up or change password
    :param orders: is the list of dictionaries which is how the
    application handles orders.
    :return: nothing

    """
    while True:
        print("************* Login System *************")
        print("1    | Log In")
        print("2    | Forgot password")
        print("3    | Sign up")
        print("4    | Quit")
        print("****************************************")

        line = input("> ")
        if line == "q" or line == "quit" or line == "4":
            break
        elif line == "1":
            username = login.login()
            if username:
                order_menu(username, orders)
        elif line == "2":
            login.forgot_password()
        elif line == "3":
            login.sign_up()
        else:
            print('command "{}" is not recognised'.format(line))
            continue


def main():
    # list_of_orders = [
    #     {'customer_name': 'mario', 'customer_address': 'W1', 'date': '270612',
    #      'total': '13.2',
    #      'UUID': 'bede-06cea4cs'},
    #     {'customer_name': 'luigi', 'customer_address': 'W2', 'date': '100300',
    #      'total': '15.6',
    #      'UUID': '4677-3b2f5a12'},
    #     {'customer_name': 'luigi', 'customer_address': 'W2', 'date': '100300',
    #      'total': '43.1',
    #      'UUID': '4677-3b2f5aca'},
    #     {'customer_name': 'luigi', 'customer_address': 'W2', 'date': '270612',
    #      'total': '10.8',
    #      'UUID': '4677-3b2f5aee'},
    #     {'customer_name': 'peach', 'customer_address': 'W3', 'date': '151205',
    #      'total': '66',
    #      'UUID': 'bede-1e9e5018'},
    #     {'customer_name': 'toad', 'customer_address': 'W4', 'date': '270612',
    #      'total': '0.60',
    #      'UUID': '4677-aa8d0842'},
    #     {'customer_name': 'toad', 'customer_address': 'W4', 'date': '272612',
    #      'total': '4.60',
    #      'UUID': 'f345-aa8d0842'},
    #     {'customer_name': 'toadette', 'customer_address': 'W8',
    #      'date': '272622', 'total': '14.60',
    #      'UUID': 'f345-aa8d0812'},
    #     {'customer_name': 'toadette', 'customer_address': 'W1',
    #      'date': '271612', 'total': '4.60',
    #      'UUID': 'f345-aa8d0813'}
    # ]
    list_of_orders = []
    login_menu(list_of_orders)


if __name__ == "__main__":
    main()
