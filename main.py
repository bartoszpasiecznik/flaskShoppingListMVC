from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app import app
from config import mysql
import pymysql
from pymysql import cursors

@app.route('/init_db')
def init_db():
    cur = mysql.connection.cursor()
    cur.execute("CREATE  DATABASE IF NOT EXISTS flaskShoppingListMVC")
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS shoppingList (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    itemName VARCHAR(256),
                    quantity VARCHAR(256),
                    bought BOOL NULL

                    )
    """)

    mysql.connection.commit()
    cur.close()
    return redirect(url_for('Index'))


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shoppingList")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', shoppingList=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        itemName = request.form['itemName']  # nazwy z index.html
        quantity = request.form['quantity']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO shoppingList (itemName, quantity, bought) VALUES (%s, %s, %s)",
                    (itemName, quantity, False))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        itemName = request.form['itemName']  # nazwy z index.html
        quantity = request.form['quantity']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE shoppingList
            SET itemName=%s, quantity=%s
            WHERE id=%s
        """, (itemName, quantity, id_data))

        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    flash("Data Deleted Successfully")

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM shoppingList WHERE id = %s", (id_data))
    mysql.connection.commit()
    return redirect(url_for('Index'))


@app.route('/bought/<string:id_data>', methods=['POST', 'GET'])
def bought(id_data):
    cur = mysql.connection.cursor()
    cur.execute("""
                    SELECT bought
                    FROM shoppingList
                    WHERE id=%s
    """, id_data)
    bought = cur.fetchone()  # nazwy z index.html
    cur.close()

    if bought[0] == 0:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE shoppingList
            SET bought=%s
            WHERE id=%s
        """, (1, id_data))
        mysql.connection.commit()
    else:
        cur = mysql.connection.cursor()
        cur.execute("""
                        UPDATE shoppingList
                        SET bought=%s
                        WHERE id=%s
                    """, (0, id_data))

        flash("Item Status Changed")
        mysql.connection.commit()

    return redirect(url_for('Index'))


@app.route('/api/additem', methods=['POST'])
def add_item():
    try:
        _json = request.json
        _itemName = _json['itemName']
        _quantity = _json['quantity']

        if _itemName and _quantity and request.method == 'POST':
            cur = mysql.connection.cursor()
            query = "INSERT INTO shoppingList (itemName, quantity, bought) VALUES (%s, %s, %s)"
            queryData = (_itemName, _quantity, False)
            cur.execute(query,queryData)
            mysql.connection.commit()
            response = jsonify("Shopping Item added successfully")
            response.status_code = 200
            cur.close()
            return response
        else:
            return showMessage()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/item')
def show_items():
    try:
        cur = mysql.connect.cursor()
        cur.execute("SELECT id, itemName, quantity, bought FROM shoppingList")
        itemList = cur.fetchall()
        response = jsonify(itemList)
        response.status_code = 200
        cur.close()
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/item/<string:item_id>')
def show_select_item(item_id):
    try:
        cur = mysql.connect.cursor()
        cur.execute("SELECT id, itemName, quantity, bought FROM shoppingList WHERE ID =%s", item_id)
        itemList = cur.fetchone()
        response = jsonify(itemList)
        response.status_code = 200
        cur.close()
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/update', methods=['PUT'])
def update_item():
    try:
        _json = request.json
        _id_data = _json['id']
        _itemName = _json['itemName']
        _quantity = _json['quantity']

        if _itemName and _quantity and _id_data and request.method == 'PUT':
            cur = mysql.connection.cursor()
            query = """
                UPDATE shoppingList
                SET itemName=%s, quantity=%s
                WHERE id=%s
            """
            queryData = (_itemName, _quantity, _id_data)
            cur.execute(query,queryData)
            mysql.connection.commit()
            response = jsonify("Shopping Item updated successfully")
            response.status_code = 200
            cur.close()
            return response
        else:
            return showMessage()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/buyitem/<string:item_id>', methods=['PUT'])
def change_item_bought_status(item_id):
    try:
        _json = request.json
        _bought_data = _json['bought']

        if request.method == 'PUT':
            cur = mysql.connection.cursor()
            query = """
                UPDATE shoppingList
                SET bought=%s
                WHERE id=%s
            """
            queryData = (_bought_data, item_id)
            cur.execute(query,queryData)
            mysql.connection.commit()
            if _bought_data:
                response = jsonify("Shopping Item bought successfully")
            else:
                response = jsonify("Shopping Item set to not bought successfully")
            response.status_code = 200
            cur.close()
            return response
        else:
            return showMessage()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/delete/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:

        if request.method == 'DELETE':
            cur = mysql.connection.cursor()
            query = """
                DELETE FROM shoppingList
                WHERE id =%s
            """
            queryData = (item_id)
            cur.execute(query,queryData)
            mysql.connection.commit()
            response = jsonify("Shopping Item deleted successfully")
            response.status_code = 200
            cur.close()
            return response
        else:
            return showMessage()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run(debug=True)