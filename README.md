# Team45: CSC301 Assignment 2
In this assignment, we are developing the cli of restaurant ordering system as front end and with Flask as backend server.


## Getting Started
The following instructions will get you a copy of the assignement and running on your local machine for development and testing purposes.


### Installing
Clone this repository to local machine. 
```
https://github.com/csc301-fall-2020/assignment-2-45-yingkewang2018-sherryw99.git
```
Install all the dependencies. (or use pip3)
```
pip install -r requirements.txt
```


## Running the app
You can run the app by opening two terminals and use one following command in each. (or use python3)

```
python client.py
python pizza_parlour.py
```
## Testing the app
Run unit tests with coverage by running 
```
pytest --cov-report term --cov=. tests/*.py
```


## Pair Programming feature
#### create order feature
In our plan, we roughly split the first feature into 3 segments: Build get Keywords file, Build Create Mediator class, and Update the usage in client.py.

Checkpoint 1: 
- Driver: Yingke, Navigator: Sherry
- Yingke works on building the data_keywords_loader.py. Yingke creates the function prototype and its implementation while Sherry going through the client file and search all the needed keywords in CLI.

Checkpoint 2:
- Driver: Sherry, Navigator: Yingke
- Sherry works on building class CreateOrderMediator and its attributes and methods, while Yingke is trying to locate all the logical code inside client.py front end file and navigate Sherry through what the logical code that she needs to implement inside CreateOrderMediator class.

Checkpoint 3:
- Driver: Yingke, Navigator: Sherry
- Discuss whether we should let CreateOrderMediator class handle all the logic or we should let CreateOrderMediator class handle all the input behaviour, or we should let CreateOrderMediator class return an order and directly edit that order.
- We finalize it into letting CreateOrderMediator class return the order, let order do the operation, and CreateOrderMediator handles the Server Dao sending functionality.
- Yingke does the create order client-side implementation, and Sherry navigates on when to use order class to handle input and when to use CreateOrderMediator to handle input.
    
#### update order feature
Our plan for the second feature is similar to the first one. Since we already have the get Keywords file built, we are left with two major things: Build Order Mediator class and Update the usage in client.py.

Checkpoint 1:
- Driver: Sherry, Navigator: Yingke
- Sherry works on building class UpdateOrderMediator and its attributes and methods, while Yingke is trying to locate all the logic of update order from client.py front end file and navigate Sherry through what the logical code that she needs to implement inside UpdateOrderMediator class.

Checkpoint 2:
- Driver: Yingke, Navigator: Sherry
- Discuss whether we should directly edit the dictionary object or turn it into an order object first and then manipulate that instead.
- We finalize it into letting UpdateOrderMediator class return the order object, let order do the operation, and UpdateOrderMediator handles the Server Dao getting and sending functionalities.
- Yingke does the update order client-side implementation, and Sherry navigates on when to use order class to handle input and when to use UpdateOrderMediator to handle input.


### Paired Programming PROS
- Navigator helped search the usage in files and give code suggestions. 
- We have someone to reach out to whenever we need help, for example we can ask the other person to search for some code usage online
- we both have a full understanding of the feature we implemented together and it also help us to use this feature in further code implementation
- we have really good design pattern and clean code, since the navigator can point out the problem that driver usually don't notice


### Paired Programming CONS
- it's kind of stressful. Having another person watching driver when he/she is typing need time to get adapted to, at the beginning. We both feel the uneasy atmosphere around us.
- We spend a lot of time discussing the design logic. Before we start doing the pair programming feature, we spends hours on choosing the design pattern we will use. We both have our own preference and need to
spend lots of time to explain to each other. However, we also think the time is valuable, because we do get a chance to know the other person's design logic and broaden the scope of looking at the same task in different perspective. 


## Code Craftsmanship
- PyCharm lets you reformat your code according to the requirements you have specified in the Code Style settings. Every time we use the reformat feature, PyCharm removes unused imports, adds missing ones, organizes import statements, and runs the code cleanup inspections. We reformat our code regularly to help us create clean and nice formatted code.


# Design Patterns
We used five design patterns: the Builder design pattern, Factory design pattern, Facade Design Pattern,  Data Access Object design pattern， Mediator design pattern.
## Mediator Design Pattern
We have five Mediator objects: CreateOrderMediator, DeliveryMediator, DeleteOrderMediator, UpdateOrderMediator, MenuMediator.

Each Mediator correspond to one functionality of our restaurant app
These Mediator objects act as a mediator between our CLI (client.py), the front end, and the 
backend server and object connection (DAO objects, order object, orderBuilder object,and item object).
As a result, CLI (client.py) do purely get input and print output. All the input and output handling get delegate to the backend operation.
In such design, we both preserver Single Responsibility Principle and hide the internal logic from the client.

## Data Access Object Design Pattern
We have concrete DAO object: ClientDaoJson and DAO interface ClientDaoInterface in client_dao.py
Our DAO objects access the server; they manage how their respective data is stored/updated/fetched from server.

Since we have DAO interface defined, which makes our app easy to load from different kinds of source. Right now, we load from JSON. In the
feature, we can also load from xml, csv, etc; as long as it follows ClientDaoInterface. In addition, creating such DAO encapsulate our server
Hence client cannot directly call request on to our server, which also increase the security level of our application.

## Builder & Facade Design Pattern
we use builder design pattern to build order_detail object (OrderDetailBuilderFacade) as well as Facade design pattern
to handle the order_detail build to PizzaOrderBuild class and DrinkOrderBuild class in order_builder.py.

In this way, we can build order_detail step by step just as the workflow of user enter each component line by line in CLI
and do orderDetailBuilderFacade.build_order_detail() only once when everything get entered.

By using Facade Design Pattern, we can separate create-order into create-drink-order and create-pizza-drink, since they actually don't interfere with each other a lot.
We also use OrderBuilder supper class to catch anything in common between these two. We use Facade to hold Single Responsibility and hide actually implementation from client.

## Factory Design Pattern
We use Factory (SerializerFactory) in order.py to convert our order object to either csv format or Json format
using Factory design pattern also encapsulate the actually serialization part and we can extend it in the future to produce xml format etc.
It also provide a easy understanding interface to serialize data.

## Server Design
On the server end, we also separate the load_and_save_files (model) from the route that handle requests (server). 
In such way, we can easily change the database we are using without doing any modification to our server.

