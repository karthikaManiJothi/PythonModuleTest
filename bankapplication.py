# By using rest api,developing banking application
# importing flask module
from flask import Flask,jsonify,render_template

# using Flask constructor , takes argument as module-name
app = Flask(__name__)

# creating database for customer
customer_details =[{'customer_name':'karthika',
                    'customer_id':'0',
                    'account_no':'234567891',
                    'account_type':'savings',
                    'balance_available':'1000'},
                   {'customer_name': 'kavin',
                    'customer_id': '1',
                    'account_no': '1457567891',
                    'account_type': 'savings',
                    'balance_available':'50000'},
                   {'customer_name':'Mani',
                    'customer_id':'2',
                    'account_no':'324567999',
                    'account_type':'CASA',
                    'balance_available':'20000'},
                  {'customer_name':'Jothi',
                    'customer_id':'3',
                    'account_no':'543261978',
                    'account_type':'CASA',
                    'balance_available':'60000'}]

# @app.route(rule,options)
# rule - binds the url with specific function
# @app.route('/) return the html page of bank application
@app.route('/')
def html():
    return render_template('bank.html')

# performing CRUD operation using http methods
# C - Create - using POST method
# R - Read   - using GET method
# U - Update - using PUT method
# D - Delete - using DELETE method

# performing reading operation in two ways:
# 1. reading all details of the customers
@app.route('/details/',methods=['GET'])
def get_customer_details():
    return jsonify({"customer_details":customer_details})

# 2.reading particular customer details using customer-id
@app.route('/details/<int:customer_id>',methods=['GET'])
def get_single_customer_details(customer_id):
    return jsonify({"customer_details":customer_details[customer_id]})

# performing create operation using post method
# creating new customer details
@app.route('/details/add',methods=['POST'])
def add_customer_details():
    # getting input to add new customer
    name =input("Enter name:")
    cus_id =input("Enter customer_id:")
    account_no=input("Enter account number:")
    account_type=input("Enter account type (savings/CASA):")
    balance_available=input("enter the available balance:")

    new_customer ={'customer_name': name,
                    'customer_id': cus_id,
                    'account_no': account_no,
                    'account_type': account_type,
                    'balance_available': balance_available}
    customer_details.append(new_customer)
    return jsonify({'new_customer':customer_details})

# performing update operation using http put method
# updating only the name and account_type of the customer
@app.route('/details/update/<int:customer_id>',methods=['PUT'])
def update_customer_details(customer_id):
    # updating details based on input
    print("what do you want to update ?")
    update =int(input("1.name\n2.account_type"))
    if update ==1:
        name =input("enter updated name:")
        customer_details[customer_id]['customer_name'] = name
    elif update==2:
        type =input("enter updated savings type")
        customer_details[customer_id]['account_type'] = type
    else:
        print("enter valid input")
    return jsonify({'customer_details': customer_details[customer_id]})


# performing deletion operation using delete method
@app.route('/details/remove/<int:customer_id>',methods=['DELETE'])
def delete_customer_details(customer_id):
    customer_details.remove(customer_details[customer_id])
    return "customer details of customerId : {} is deleted successfully".format(customer_id)

# withdraw operation
@app.route('/withdraw/<int:customer_id>',methods=['PUT'])
def withdraw(customer_id):
    withdraw_amount =int(input("amount need to be withdraw from your account :"))
    balance =int(customer_details[customer_id]['balance_available'])
    # checking the available balance
    if balance < withdraw_amount:
        return "available balance is low"
    else:
       final_balance = balance - withdraw_amount
       # updating the account balance
       customer_details[customer_id]['balance_available'] = final_balance
       return jsonify({"Balance":customer_details[customer_id]['balance_available']})

# deposit operation
@app.route('/deposit/<int:customer_id>', methods=['PUT'])
def deposit(customer_id):
    # getting amount from the user
    amount = int(input("amount depositing to your account :"))
    balance = int(customer_details[customer_id]['balance_available'])
    available_balance = balance + amount
    # updating the account balance
    customer_details[customer_id]['balance_available'] = available_balance
    return jsonify({"Current Balance": customer_details[customer_id]['balance_available']})


if __name__ == '__main__':
    # app.run(host,port,debug,options)
    # run the application on local server
    app.run(debug=True)


# commands:
# to create : curl -i -H "Content-Type: Application/json" -X POST http://localhost:5000/details/add
# to update : curl -i -H "Content-Type: Application/json" -X PUT http://localhost:5000/details/update/2
# to delete : curl -i -H "Content-Type: Application/json" -X DELETE http://localhost:5000/details/remove/1
# to withdraw : curl -i -H "Content-Type: Application/json" -X PUT http://localhost:5000/withdraw/1
# to deposit : curl -i -H "Content-Type: Application/json" -X PUT http://localhost:5000/deposit/2