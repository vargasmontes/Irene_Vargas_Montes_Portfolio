from datetime import datetime
stock = {"BPCM": {"Category": "Phone",
                    "Item code": "BPCM",
                    "Description": "Compact",
                    "Price": 29.99},
        "BPSH": {"Category": "Phone",
                    "Item code": "BPSH",
                    "Description": "Clam shell",
                    "Price": 49.99},
        "RPSS": {"Category": "Phone",
                    "Item code": "RPSS",
                    "Description": "Robo phone - 5inch 64GB memory",
                    "Price": 199.99},
        "RPLL": {"Category": "Phone",
                    "Item code": "RPLL",
                    "Description": "Robo phone - 6inch 256GB memory",
                    "Price": 499.99},
        "YPLS": {"Category": "Phone",
                    "Item code": "YPLS",
                    "Description": "Y-phone standard 6 inch 64GB memory",
                    "Price": 549.99},
        "YPLL": {"Category": "Phone",
                    "Item code": "YPLL",
                    "Description": "Y-phone deluxe 6 inch 256GB memory",
                    "Price": 649.99},
        "RTMS": {"Category": "Tablet",
                    "Item code": "RTMS",
                    "Description": "RoboTab - 8 inch screen 64GB memory",
                    "Price": 149.99},
        "RTML": {"Category": "Tablet",
                    "Item code": "RTML",
                    "Description": "RoboTab - 10 inch screen 64GB memory",
                    "Price": 299.99},
        "YTLM": {"Category": "Tablet",
                    "Item code": "YTLM",
                    "Description": "Y-tab standard - 10 inch screen 128GB memory",
                    "Price": 499.99},
        "YTLL": {"Category": "Tablet",
                    "Item code": "YTLL",
                    "Description": "Y-tab deluxe - 10 inch screen 128GB memory",
                    "Price": 599.99},
        "SMNO": {"Category": "SIM Card",
                    "Item code": "SMNO",
                    "Description": "Sim free (no SIM card)",
                    "Price": 0},
        "SMPG": {"Category": "SIM Card",
                    "Item code": "SMPG",
                    "Description": "Pay as you go (with SIM card)",
                    "Price": 9.99},
        "CSST": {"Category": "Case",
                    "Item code": "CSST",
                    "Description": "Standard",
                    "Price": 0},
        "CSLX": {"Category": "Case",
                    "Item code": "CSLX",
                    "Description": "Luxury",
                    "Price": 50},
        "CGCR": {"Category": "Charger",
                    "Item code": "CGCR",
                    "Description": "Car",
                    "Price": 19.99},
        "CGHM": {"Category": "Charger",
                    "Item code": "CGHM",
                    "Description": "Home",
                    "Price": 15.99}}
global basket
basket = []

def Finish():
    print("That is a shame. Please come back to our shop if you wish to buy anything in the future!\n\n")
    return

def AssistCustomer():
    shopping_finished = False
    while shopping_finished == False:
        device = ""
        while device == "":
            interest = input("Are you interested in looking at phones, tablets or both? ").lower().strip()
            interest = "phone" if interest == "phones" else interest
            interest = "tablet" if interest == "tablet" else interest

            if interest == "phone" or interest == "tablet":
                print(f"We have in stock the following {interest}s:")
                for item in stock:
                    if stock[item]["Category"] == interest.capitalize():
                        print(f"- [{stock[item]['Item code']}] {stock[item]['Description']}, for {stock[item]['Price']}$;")

            elif interest == "both":
                print("We have in stock the following devices:")
                for item in stock:
                    if stock[item]["Category"] == "Tablet" or stock[item]["Category"] == "Phone":
                        print(f"- [{stock[item]['Item code']}] {stock[item]['Description']}, for {stock[item]['Price']}$;")

            else:
                print("Sorry, I did not understand that. Here are all of our devices for sale:")
                for item in stock:
                    if stock[item]["Category"] == "Tablet" or stock[item]["Category"] == "Phone":
                        print(f"- [{stock[item]['Item code']}] {stock[item]['Description']}, for {stock[item]['Price']}$;")

            print("\n")
            device_choice = input("If you are interested in any of these products, please let me know what the item code of it is: ").upper().strip()
            if device_choice in stock:
                print("Item code " + device_choice + " is the " + stock[device_choice]["Description"] + ". It is on sale for " + str(stock[device_choice]["Price"]) + "$.")
                proceed = input("Would you like to proceed with the item? ").lower().strip()
                if proceed == "no":
                    check_again = input("I am sorry to hear that. Would you like to look at other options? Or would you like to select another item code from the ones I presented to you? ").lower().strip()
                    if check_again == "yes":
                        continue
                    elif check_again == "no":
                        Finish()
                    elif check_again.upper() in stock:
                        device = check_again.upper().strip()
                    else:
                        print("Sorry, I did not understand that. Please try again.")
                        continue
                elif proceed == "yes":
                    device = device_choice
                else: proceed = input("Please decide between yes or no: ")

        basket.append(device)
        print("\n")

        # Task 1.3: Allow phone customers to choose whether the phone will be SIM Free or Pay As You Go:
        if stock[device]["Category"] == "Phone":
            sim = ""
            print("Since you have chosen a phone, here is the SIM options we offer:")
            for options in stock:
                item = stock[options]
                if item["Category"] == "SIM Card": print("- " + item["Description"])

            sim_choice = input("Which option would you like to proceed with? 'With SIM' or 'without SIM'? ").lower().strip()
            while sim == "":
                if sim_choice == "with sim":
                    print("The " + stock["SMPG"]["Description"] + " option is " + str(stock["SMPG"]["Price"]) + "$.")
                    sim = "SMPG"
                elif sim_choice == "without sim":
                    print("The " + stock["SMNO"]["Description"] + " option is free of cost.")
                    sim = "SMNO"
                else:
                    sim_choice = input("Please select one option: 'With SIM' or 'without SIM'. ")

            proceed = input("Would you like to proceed with the item? ").lower().strip()
            while proceed != "yes":
                other_sim = "SMPG" if sim == "SMNO" else "SMNO"
                print("I understand. The other option, the " + stock[other_sim]["Description"] + " option is " + str(stock[other_sim]["Price"]) + "$.")

                if input("Would you like to choose this option? ").lower().strip() == "yes":
                    proceed = "yes"
                    sim = other_sim
                else:
                    print("No problem, we will go with you original choice.")
                    proceed = "yes"

            basket.append(sim)
            print("\n")

        # Task 1.4: Allow the customer to choose a standard or luxury case:
        print(f"Included with your purchase is a standard case. For {stock['CSLX']['Price']}$ you can upgrade to the {stock['CSLX']['Description']} case.")
        device_case = "CSLX" if input("Are you interested in this offer? ").lower().strip() == "yes" else "CSST"

        basket.append(device_case)
        print("\n")

        # Task 1.5: Allow the customer to choose the chargers required
        chargers = []
        chargers_need = input("Do you need to buy any chargers? ").lower().strip()
        if chargers_need == "yes":
            print("We can offer the following charger types:")
            for item in stock:
                if stock[item]["Category"] == "Charger":
                    if input(f"- {stock[item]['Description']} charger, for {stock[item]['Price']}$. Would you like to purchase it? ").lower().strip() == "yes":
                        chargers.append(stock[item]["Item code"])

        basket.extend(chargers)
        print("\n")

        # Task 1.6:Calculate the total price of this transaction:
        global total_price
        total_price = 0
        for item in basket: total_price += stock[item]["Price"]

        print(f"Your current total is {total_price}$.")
        print("We have an active promotion for 10% off of every additional phone or tablet purchased.")
        choice = input("Would you like to purchase any other mobile devices? ").lower().strip()
        if choice == "no":
            shopping_finished = True

class PrintReceipt():
    def __init__(self):
        #Widths for receipt columns
        self.desc_width = max([len(stock[item]["Description"]) for item in basket])+2
        self.price_width = max([len(str(stock[item]["Price"])) for item in basket])+3

        #Timing
        now = datetime.now()
        self.date = now.strftime("%d %b %Y")
        self.time = now.strftime("%I:%M:%S %p")

    def WithoutDiscount(self):
        # Task 1.7: Output a list of the stock purchased and the total price:
        max_width = self.desc_width + self.price_width + 23
        half_width = int(max_width/2)

        print("\n")
        print(("Receipt").center(max_width, "-"))
        print(self.date.ljust(half_width, " ")+self.time.rjust(half_width, " "))
        print(f"{'Category':10} {'Item code':10} {'Description':{self.desc_width}} {'Price':>{self.price_width}}")

        for item in basket:
            category = stock[item]["Category"]
            code = stock[item]["Item code"]
            description = stock[item]["Description"]
            price = stock[item]["Price"]
            price = f"{price:.2f}$"

            print(f'{category:10} {code:10} {description:{self.desc_width}} {price:>{self.price_width}}')

        print(f"Total: {total_price:.2f}$".rjust(max_width, "-"))

    def WithDiscount(self):
        # Task 3: Allow a discount of 10% off the price of every additional phone or tablet purchased
        max_width = self.desc_width + self.price_width * 2 + 32
        half_width = int(max_width/2)

        discount_active = False

        print("\n")
        print(("Receipt").center(max_width, "-"))
        print(self.date.ljust(half_width, " ")+self.time.rjust(half_width, " "))
        print(f'{'Category':10} {'Item code':10} {'Description':{self.desc_width}} {'Price':{self.price_width}} {'Discount':9} {'Total':>{self.price_width}}')

        to_pay = 0
        for item in basket:
            category = stock[item]["Category"]
            code = stock[item]["Item code"]
            description = stock[item]["Description"]
            price = stock[item]["Price"]
            discount = ""
            total = price
            if discount_active == True and (category == "Phone" or category == "Tablet"):
                discount = "10%"
                total = price * 0.9

            to_pay += total
            total = f"{total:.2f}$"
            price = f"{price:.2f}$"

            if category == "Phone" or category == "Tablet": discount_active = True

            print(f'{category:10} {code:10} {description:{self.desc_width}} {price:{self.price_width}} {discount:9} {total:>{self.price_width}}')

        discount_total = total_price - to_pay
        final_price = total_price - discount_total

        print(f"\nSubtotal: {total_price:.2f}$".rjust(max_width, " "))
        print(f"Discounted: {discount_total:.2f}$".rjust(max_width, " "))
        print(f"Final price to pay: {final_price:.2f}$".rjust(max_width, "-"))

if __name__ == "__main__":
    print("Welcome to the shop.")
    AssistCustomer()

    discount = False
    amount_devices = 0
    for item in basket:
        if stock[item]["Category"] == "Phone" or stock[item]["Category"] == "Tablet":
            amount_devices += 1

    if amount_devices > 1: discount = True

    if discount == False: PrintReceipt().WithoutDiscount()
    else: PrintReceipt().WithDiscount()

    print("\nThank you for choosing to shop with us today!")
