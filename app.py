from flask import Flask, render_template, request, redirect
import sqlite3

from models.Product import Product

app = Flask(__name__)

db_connection = sqlite3.connect("database/products.db", check_same_thread=False)
# check_same_thread=False solves this problem
# sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.

db_cursor = db_connection.cursor()


def __create_product_table():
    """
    This method should be only called once
    :return:
    """
    db_connection.execute('''
    CREATE TABLE PRODUCT
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        PRICE NUMBER,
        DISCOUNT NUMBER);
    ''')
    db_connection.commit()


def __add_product(name, price, discount):
    db_connection.execute(f"""INSERT INTO PRODUCT(NAME, PRICE, DISCOUNT)
                        VALUES('{name}', '{int(price)}', '{float(discount)}')""")
    db_connection.commit()


def __get_all_products():
    return list(db_connection.execute("""SELECT * FROM PRODUCT"""))


@app.route('/')
@app.route('/index')
def default_route():
    list_prod = __get_all_products()
    print(list_prod)
    return render_template('index.html', result=list_prod)


@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        if db_connection is not None:
            try:
                __add_product(request.form['name'], request.form['price'], request.form['discount'])
                list_prod = __get_all_products()
                return render_template('index.html', result=list_prod)
            except Exception as e:
                print(e)
                print("Error while inserting product")
        else:
            return redirect('/')
    else:
        list_prod = __get_all_products()
        return render_template('index.html', result=list_prod)
    return redirect('/')


@app.route("/edit")
def edit_product():
    print("Hello we are here to edit")
    print(request.args.get('id'))
    product = db_connection.execute(f"SELECT * FROM PRODUCT WHERE ID={request.args.get('id')}")
    for x in product:
        product = Product(*x)
        print(product)
    return render_template("add_product.html", product=product)


if __name__ == '__main__':
    try:
        __create_product_table()
    except Exception:
        print("Table already exists")
    app.run(debug=True)
