from flask import Flask, render_template, request 
import pymysql
db_connection = None
tb_cursor = None

app = Flask(__name__)

@app.route('/')
def index():
    booksdata=getallbooks()
    return render_template("index.html",data=booksdata)

@app.route("/add",methods=["GET","POST"])
def addBook():
    if request.method=="POST":
        data = request.form
        isInserted = Insertintotable(data['txtName'],data['txtAuthor'],data['txtPrice'],data['txtPb'],data['txtPbd'])

        if (isInserted):
            message="Insertion Sucess"
        else:
            message='Insertion Error'
            return render_template("add.html",message=message)
    return render_template("add.html")

def dbconnect():
    global db_connection, tb_cursor 
    db_connection=pymysql.connect(host='localhost',
    user='root',passwd='',database='lms',port=3306)
    if(dbconnect):
        print('Connected')
        tb_cursor = db_connection.cursor()

    else:
        print('Not Connected')

def dbdisconnect():
    db_connection.close()
    tb_cursor.close()


def getallbooks():
        dbconnect()
        getquery='select * from books'
        tb_cursor.execute(getquery)
        booksdata = tb_cursor.fetchall()
        dbdisconnect()
        return booksdata

def Insertintotable(Name,Author,Price,Publication,Publication_Date):
    dbconnect()
    Insertquery = "INSERT INTO books(Name, Author, Price, Publication, Publication_Date) Values (%s,%s,%s,%s,%s,);"
    tb_cursor.execute(Insertquery,(Name,Author,Price, Publication, Publication_Date))
    db_connection.commit()
    dbdisconnect()
    return True


if __name__=='__main__':
    app.run(debug=True)
