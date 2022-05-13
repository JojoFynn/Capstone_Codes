from flask import Flask, render_template, url_for,  request, redirect, flash
import sqlite3 as sql
app = Flask(__name__)


@app.route("/")
@app.route("/login_authentication", methods=['POST', 'GET'])
def login_authentication():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        connection = sql.connect("RFID_database.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM administrator WHERE admin_email=? AND admin_password=?", (name, password))
        row = cursor.fetchall()
        if row:
            return redirect(url_for('index'))
        else:
            flash('Incorrect information', 'warning')
    return render_template("login_page.html")


@app.route("/index")
def index():
    con = sql.connect("RFID_database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from fertiliser_data ")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


@app.route("/getrfidcode", methods=['POST', 'GET'])
def getrfidcode():
    if request.method == "POST":
        currentUID = request.args.get("UIDresult")
        write_to_file(currentUID)
        return 'success'
    else:
        currentUID = ''
        with open('rfid.txt') as file:
            currentUID = file.read()
        return currentUID


@app.route("/checkoutbag")
def checkoutbag():
    return render_template("checkoutbag.html")


@app.route("/checkrfidcode", methods=['POST', 'GET'])
def checkrfidcode():
    if request.method == "POST":
        currentUID = request.args.get("UIDresult")
        write_to_file(currentUID)
        return 'success'
    else:
        currentUID = ''
        with open('rfid.txt') as file:
            currentUID = file.read()
            con = sql.connect("RFID_database.db")
            cur = con.cursor()
            cur.execute(
                "select rfid_code from fertiliser_data where rfid_code=?", (currentUID,))
            table = cur.fetchone()
            if(table == None):
                return 'Wrong Card'
        return table[0]


@app.route("/fertiliser_information", methods=['POST', 'GET'])
def fertiliser_information():
    if request.method == "POST":
        manufacturer_name = request.form['Name_of_Manufacturer']
        manufac_location_name = request.form['Manufacturer_Location_Name']
        destination_name = request.form['Destination_Location_Name']
        voucher_code = request.form['Unique_Government_Voucher_Code']
        rfid_code = request.form['Unique_Identifier_Tag_Code']
        con = sql.connect("RFID_database.db")
        cur = con.cursor()
        cur.execute("insert into fertiliser_data(manufacturer_name,start_location,destination_location,voucher_code,rfid_code) values (?,?,?,?,?)",
                    (manufacturer_name, manufac_location_name, destination_name, voucher_code, rfid_code))
        con.commit()
        flash('User Added', 'success')
        return redirect(url_for("index"))
    clear_file()
    return render_template("adding_fertiliser_bags.html")


@app.route("/edit_user/<string:rfid_code>", methods=['POST', 'GET'])
def edit_user(rfid_code):
    if request.method == 'POST':
        manufacturer_name = request.form['Name of Manufacturer']
        manufac_location_name = request.form['Manufacturer Location Name']
        destination_name = request.form['Destination Location Name']
        voucher_code = request.form['Unique Government Voucher Code']
        con = sql.connect("RFID_Database.db")
        cur = con.cursor()
        cur.execute("update fertiliser_data set voucher_code=?, manufacturer_name=?, start_location=?, destination_location=? where rfid_code=?",
                    (voucher_code, manufacturer_name, manufac_location_name, destination_name, rfid_code))
        con.commit()
        flash('User Updated', 'success')
        return redirect(url_for('index'))
    con = sql.connect("RFID_Database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from fertiliser_data where rfid_code=?", (rfid_code,))
    data = cur.fetchone()
    return render_template("editing_fertiliser_info.html", datas=data)


@app.route("/delete_user/<string:rfid_code>", methods=['GET'])
def delete_user(rfid_code):
    con = sql.connect("RFID_Database.db")
    cur = con.cursor()
    cur.execute("delete from fertiliser_data where rfid_code=?", (rfid_code,))
    con.commit()
    flash('User Deleted', 'warning')
    return redirect(url_for('index'))


def write_to_file(val):
    with open('rfid.txt', 'w') as file:
        file.write(val)


def clear_file():
    with open('rfid.txt', 'r+') as file:
        file.truncate()


if __name__ == "__main__":
    app.secret_key = 'dffg67789@#$%^&*iuyt@'
    app.run(debug=True, host="0.0.0.0", port=5000)
