class User():
    def __init__(self, name, branch,type, accno):
        self.name = name
        self.branch = branch
        self.type = type
        self.accno = accno

    def show_user_details(self):
        print("PERSONAL DETAILS")
        print("")
        print("Name: ", self.name)
        print("Branch: ", self.branch)
        print("Acc/Type: ", self.type)
        print("Acc/No:", self.accno)
# User1 = User("MAXWEL OCHIENG OKEYO",20,"MALE")


class Bank(User):
    def __init__(self, name, branch,type, accno):
        super().__init__(name, branch,type, accno)
        self.balance = 0
        self.savingsBal =0

    def deposit(self, amount):
        self.amount = amount
        self.balance = self.balance + self.amount
        print(
            f"Account Updated Succesfully. The Balance Is {self.balance} Ksh.")

    # save
    def saveAmount(self, amount):
        self.amount = amount
        self.savingsBal = self.savingsBal + self.amount
        print(f"\nSaved Well Bal Ksh. {self.savingsBal} ")

    def checkSaveBal(self):
        print(f"\nSavings Account Bal is  {self.savingsBal}")


    def withdraw(self, amount):
        self.amount = amount
        if (self.balance >= amount):
            self.balance = self.balance - amount
            print(f"Withdrawal Succesfully Made. Your Outstanding balance is: {self.balance} Ksh.")
            return True
        else:
            print(f"Ballance Insufficient,  Your Balance Available is:  {self.balance} Ksh.")
            return False

    def view_balance_(self):
        self.show_user_details()
        print(f"The Balance Is: {self.balance}")


    def Controller(self):
        print("""
    Please Select your Choice below
    1. Do you wanna Deposit
    2. Do you wanna Withdraw
    3. Access Your Savings Account
    4. Do you wanna Exit?

        """)

        choice = input("Choice:  ")



        if choice == "1":
            amount = input("Enter Amount to Deposit:   ")
            # all inputs are strings convert them
            amount = int(amount)
            self.deposit(amount)
            print("\n\n")
            self.Controller()
        elif choice == "2":
            amount = input("Enter Amount to Withdraw:  ")
            amount = int(amount)
            # ask until got amout is entered
            while not self.withdraw(amount):
                amount = input("Insufficient Funds     ")
                amount = int(amount)
            print("\n\n")
            self.show_user_details()
            self.view_balance_()
            self.Controller()
        elif choice == "3":
            print(
            """
    choose what to do in savingas account:
    1. deposit
    2. view balance
    3. exit
            """)
            choice = input("choice : ")

            # for saving .. deposited amount savingsBal
            if choice == "1":
                amount = input("Enter Amount to Deposit:   ")
                # all inputs are strings convert them
                amount = int(amount)
                self.saveAmount(amount)
                print("\n\n")
                self.Controller()

            elif choice ==  "2":
                self.checkSaveBal()
                self.Controller()
            else:
                print("Leaving the Program ...........\n")
                exit(1)
        else:
            print()
            print()
            self.show_user_details()
            self.view_balance_()
            print("\n Leaving the program......")
            exit(1)



# create object for back since it contains users data
bank = Bank("MAXWEL OCHIENG OKEYO",
            "KCB BANK - THIKA ROAD MALL", "CURRENT ACCOUNT", 1273577450)

#create object for savings account
# savings = Bank("MAXWEL OCHIENG OKEYO",
#             "KCB BANK - THIKA ROAD MALL", "SAVINGS  ACCOUNT", 1273576078)


print("\n")
bank.Controller()
