# flaskShoppingListMVC
Shopping List MVC made in Flask using MySQL Database

Shopping list is able to:
- Add items to the database
- Edit items
- Delete items
- Change item bought status

# REST API
There is an implemented REST API with following requests:
 - POST: '127.0.0.1:5000/api/additem': Adds new item to the shopping list, requires json body with two arguments called "itemName" and "quantity"
 - GET: '127.0.0.1:5000/api/item': Shows all items in the database
 - GET: '127.0.0.1:5000/api/item/<item_id>': Returns specific item from the database
 - PUT: '127.0.0.1:5000/api/update': Updates a record. Requires json body with three arguments: "id", "itemName", "quantity"
 - PUT: '127.0.0.1:5000/api/buyitem/<item_id>': Updates bought status
 - DELETE: '127.0.0.1:5000/api/delete/<item_id>': Deletes a record with selected ID

# Instructions
1. Create a MySQL Database with port 3306 and add a database called flaskShoppingListMVC
2. Run app.py
3. Enter 127.0.0.1:5000/init_db in your browser - this will initialize a database and table in your MySQL Database
4. Click "Add Item" button to add an item
5. Now you can click Change Item Status to change item bough status, Edit button to edit the record or Delete button to delete the record
