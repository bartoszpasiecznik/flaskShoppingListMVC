from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskShoppingListMVC'

mysql = MySQL(app)
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

    return render_template('index.html', shoppingList = data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        itemName = request.form['itemName'] #nazwy z index.html
        quantity = request.form['quantity']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO shoppingList (itemName, quantity, bought) VALUES (%s, %s, %s)", (itemName, quantity, False))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/update', methods = ['POST', 'GET'])
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

@app.route('/delete/<string:id_data>', methods = ['POST', 'GET'])
def delete(id_data):

    flash("Data Deleted Successfully")

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM shoppingList WHERE id = %s", (id_data))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/bought/<string:id_data>', methods = ['POST', 'GET'])
def bought(id_data):

    cur = mysql.connection.cursor()
    cur.execute("""
                    SELECT bought
                    FROM shoppingList
                    WHERE id=%s
    """, id_data)
    bought = cur.fetchone()  # nazwy z index.html
    cur.close()
    print(bought[0])

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

if __name__ == "__main__":
    app.run(debug=True)
