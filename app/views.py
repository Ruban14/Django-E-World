import hashlib
import sqlite3
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import EmployeeForm
from .models import Products, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def getLoginDetails(request):
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    if 'email' not in request.session:
        loggedIn = False
        firstName = ''
        noOfItems = 0
    else:
        loggedIn = True
        cursor.execute("SELECT userId, firstName FROM app_users WHERE email = '" + request.session['email'] + "'")
        userId, firstName = cursor.fetchone()
        cursor.execute('SELECT count(productId_id) FROM app_cart WHERE userId_id = ' + str(userId))
        noOfItems = cursor.fetchone()[0]
    db.commit()
    return loggedIn, firstName, noOfItems


# @app.route("/registerationForm")
def registrationForm(request):
    return render(request, 'register.html')


# @app.route("/register", methods=['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute('SELECT email FROM app_users')
        data = cursor.fetchall()
        for row in data:
            if row[0] == email:
                print("exit")
                return HttpResponse('<h1>Email ID already exists</h1>')
        password = request.POST.get("password", False)
        firstName = request.POST.get("firstName", False)
        try:
            cursor.execute('INSERT INTO app_users (password, email, firstName) VALUES (?, ?, ?)',
                           (hashlib.md5(password.encode()).hexdigest(), email, firstName))
            db.commit()
        except:
            db.rollback()
        db.close()
        return render(request, 'login.html')


# @app.route("/loginForm")
def loginForm(request):
    if 'email' in request.session:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')


# @app.route("/login", methods = ['POST', 'GET'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        password = request.POST.get("password", False)
        if is_valid(email, password):
            request.session['email'] = email
            return HttpResponseRedirect('/app/')
        else:
            return "invalid ok va"
    return render(request, 'login.html')


def index(request):
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT productId, name, price, description, image  FROM app_products')
    itemData = cursor.fetchall()
    cursor.execute('SELECT categoryId, name FROM app_category')
    categoryData = cursor.fetchall()
    itemData = parse(itemData)
    return render(request, 'home.html',
                  {'itemData': itemData, 'loggedIn': loggedIn, 'firstName': firstName, 'noOfItems': noOfItems,
                   'categoryData': categoryData})


def add(request):
    if request.method == "POST":
        name = request.POST.get("name", False)
        price = float(request.POST.get("price", False))
        description = request.POST.get("description", False)
        category_id = int(request.POST.get("category", False))
        image = request.FILES.get("image", False)
        # obj = Products(name=name, price=price, description=description, category_id=category_id,image=image).save()
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        try:
            cursor = Products(name=name, price=price, description=description, category_id=category_id,
                              image=image).save()
            cursor.execute(
                '''INSERT INTO app_products (name, description, image, category_id, price) VALUES (?, ?, ?, ?, ?)''',
                (name, description, image, category_id, price,))
            db.commit()
            msg = "added successfully"
        except:
            msg = "error occurred"
            db.rollback()
        db.close()
        print(msg)
        return HttpResponseRedirect('/app/edit/')


# @app.route("/add")
def admin(request):
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT categoryId,name FROM app_category")
    categories = cursor.fetchall()
    db.close()
    return render(request, 'add.html', {'categories': categories})


# @app.route("/remove")
def remove(request):
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT productId, name, price, description FROM app_products')
    data = cursor.fetchall()
    db.close()
    return render(request, 'remove.html', {'data': data, 'range': range(5)})


# @app.route("/removeItem")
def removeItem(request):
    productId = request.GET.get('productId')
    categoryId = request.GET.get('categoryId')
    db = sqlite3.connect('db.sqlite3')
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM app_products WHERE productId = ' + productId)
        db.commit()
        msg = "Deleted successfully"
    except:
        cursor = db.cursor()
        cursor.execute('DELETE FROM app_category WHERE categoryId = ' + categoryId)
        db.commit()
        msg = "Error occurred"
    db.close()
    print(msg)
    return HttpResponseRedirect('/app/edit/')


# @app.route("/displayCategory")
def displayCategory(request):
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    categoryId = request.GET.get("categoryId")
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute(
        "SELECT app_products.productId, app_products.name, app_products.price, app_products.image, app_category.name FROM app_products, app_category WHERE app_products.category_Id = app_category.categoryId AND app_category.categoryId = " + categoryId)
    data = cursor.fetchall()
    db.close()
    categoryName = data[0][4]
    data = parse(data)
    return render(request, 'displayCategory.html',
                  {'data': data, 'loggedIn': loggedIn, 'firstName': firstName, 'noOfItems': noOfItems,
                   'categoryName': categoryName})


# @app.route("/productDescription")
def productDescription(request):
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    productId = request.GET.get('productId')
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT productId, name, price, description, image FROM app_products WHERE productId = ' + productId)
    productData = cursor.fetchone()
    db.close()
    return render(request, 'item.html',
                  {'data': productData, 'loggedIn': loggedIn, 'firstName': firstName, 'noOfItems': noOfItems})


def product(request):
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT productId, name, price, description, image FROM app_products')
    itemData = cursor.fetchall()
    cursor.execute('SELECT categoryId, name, image FROM app_category')
    catData = cursor.fetchall()

    return render(request, 'product.html',
                  {'loggedIn': loggedIn, 'catData': catData, 'firstName': firstName, 'noOfItems': noOfItems,
                   'itemData': itemData})


# @app.route("/addToCart")
def addToCart(request):
    if 'email' not in request.session:
        return render(request, 'login.html')
    else:
        productId = request.GET.get('productId')
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute("SELECT userId FROM app_users WHERE email = '" + request.session['email'] + "'")
        userId = cursor.fetchone()[0]
        try:
            cursor.execute("INSERT INTO app_cart (userId_id, productId_id) VALUES (?, ?)", (userId, productId))
            db.commit()
        except:
            db.rollback()
    db.close()
    return HttpResponseRedirect('/app/')


# @app.route("/cart")
def cart(request):
    if 'email' not in request.session:
        return render(request, 'login.html')
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    email = request.session['email']
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT userId FROM app_users WHERE email = '" + email + "'")
    userId = cursor.fetchone()[0]
    cursor.execute(
        "SELECT app_products.productId, app_products.name, app_products.price, app_products.image FROM app_products, app_cart WHERE app_products.productId = app_cart.productId_id AND app_cart.userId_id = " + str(
            userId))
    products = cursor.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render(request, "cart.html",
                  {'products': products, 'totalPrice': totalPrice, 'loggedIn': loggedIn, 'firstName': firstName,
                   'noOfItems': noOfItems})


# @app.route("/removeFromCart")
def removeFromCart(request):
    if 'email' not in request.session:
        return render(request, 'login.html')
    email = request.session['email']
    productId = int(request.GET.get('productId'))
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT userId FROM app_users WHERE email = '" + email + "'")
    userId = cursor.fetchone()[0]
    try:
        cursor.execute(
            "DELETE FROM app_cart WHERE userId_id = " + str(userId) + " AND productId_id = " + str(productId))
        db.commit()
    except:
        db.rollback()
    db.close()
    return HttpResponseRedirect('/app/')


def end2(request):
    return render(request, 'end.html')


def end(request):
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    email = request.session['email']
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT userId FROM app_users WHERE email = '" + email + "'")
    userId = cursor.fetchone()[0]
    if noOfItems == 0:
        return HttpResponseRedirect('/app/')
    else:
        cursor.execute(
            "SELECT app_products.productId, app_products.name, app_products.price, app_products.image FROM app_products, app_cart WHERE app_products.productId = app_cart.productId_id AND app_cart.userId_id = " + str(
                userId))
        products = cursor.fetchall()
        mail = get_template('mail.html')
        subject, from_email, to = 'Product Confirm', 'harirooban43@gmail.com', email
        text_content = 'This is an important message.'
        html_content = mail.render({'products': products, 'firstName': firstName})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        cursor.execute(
            "INSERT into app_order SELECT NULL, app_products.name, app_products.price, app_products.description, app_products.image, app_cart.userId_id, app_products.productId FROM app_products, app_cart WHERE app_products.productId = app_cart.productId_id AND app_cart.userId_id = " + str(
                userId))
        cursor.execute("DELETE FROM app_cart WHERE userId_id = " + str(userId))
    db.commit()
    return HttpResponseRedirect('/app/end2/', {'loggedIn': loggedIn, 'firstName': firstName, 'noOfItems': noOfItems})



# @app.route("/logout")
def logout(request):
    request.session.pop('email', None)
    return HttpResponseRedirect('/app/')


def is_valid(email, password, ):
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT email, password FROM app_users')
    data = cursor.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


# @app.route("/loginForm")


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


# admin
def aregistrationForm(request):
    return render(request, 'adminregister.html')


# @app.route("/aregister", methods=['GET', 'POST'])
def aregister(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute('SELECT email FROM app_admin')
        data = cursor.fetchall()
        for row in data:
            if row[0] == email:
                print("exit")
                return HttpResponse('<h1>Email ID already exists</h1>')
        password = request.POST.get("password", False)
        firstName = request.POST.get("firstName", False)
        try:
            cursor.execute('INSERT INTO app_admin (password, email, firstName) VALUES (?, ?, ?)',
                           (hashlib.md5(password.encode()).hexdigest(), email, firstName))
            db.commit()
        except:
            db.rollback()
        db.close()
        return render(request, 'adminlogin.html')


# @app.route("/aloginForm")
def aloginForm(request):
    if 'email' in request.session:
        return render(request, 'add.html')
    else:
        return render(request, 'adminlogin.html')


# @app.route("/alogin", methods = ['POST', 'GET'])
def alogin(request):
    if request.method == 'POST':
        email = request.POST.get("email", False)
        password = request.POST.get("password", False)
        if is_valid1(email, password):
            request.session['logged_in'] = email
            request.session.set_expiry(500)
            return HttpResponseRedirect('/app/edit/')
        else:
            return "invalid"
    return render(request, 'adminlogin.html')


def is_valid1(email, password):
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute('SELECT email, password FROM app_admin')
    data = cursor.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


def logout1(request):
    request.session.pop('logged_in', None)
    return HttpResponseRedirect('/app/alogin/')


def edit(request):
    if not request.session.get('logged_in'):
        return render(request, 'adminlogin.html')
    else:
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute('SELECT productId, name, price, description,Category_Id,image FROM app_products')
        data = cursor.fetchall()
        cursor.execute('SELECT categoryId,name,image FROM app_category')
        mata = cursor.fetchall()
        cursor.execute('SELECT email,firstName FROM app_admin')
        gata = cursor.fetchall()
        return render(request, 'edit.html', {'data': data, 'mata': mata, 'gata': gata})


def catadd(request):
    if not request.session.get('logged_in'):
        return render(request, 'adminlogin.html')
    else:
        if request.method == "POST":
            name = request.POST.get("name", False)
            image = request.FILES.get("image", False)
            db = sqlite3.connect('db.sqlite3')
            cursor = db.cursor()
            try:
                cursor = Category(name=name, image=image).save()
                cursor.execute(
                    '''INSERT INTO app_category (name,image) VALUES (?, ?,)''',
                    (name, image,))
                db.commit()
                msg = "added successfully"
            except:
                msg = "error occurred"
                db.rollback()
            db.close()
            print(msg)
            return HttpResponseRedirect('/app/edit')


# @app.route("/add")
def catadmin(request):
    return render(request, 'catadd.html')


def update(request, productId):
    if not request.session.get('logged_in'):
        return render(request, 'adminlogin.html')
    else:
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute('SELECT categoryId,name FROM app_category')
        categories = cursor.fetchall()
        product = Products.objects.get(productId=productId)
        form = EmployeeForm(request.POST or None, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/edit/')
        return render(request, 'update.html', {'form': form, 'product': product, 'categories': categories})


# @app.route("/address", methods=['GET', 'POST'])
def bill(request):
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    if request.method == 'POST':
        email = request.session['email']
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute("DELETE FROM app_address WHERE email_id = '" + email + "'")
        mobile = request.POST.get("mobile", False)
        address = request.POST.get("address", False)
        postcode = request.POST.get("postcode", False)
        try:
            cursor.execute('INSERT INTO app_address (email_id,address, mobile,  postcode) VALUES (?, ?, ?, ?)', (email,address, mobile,  postcode))
            db.commit()
        except:
            db.rollback()
        db.close()
        return HttpResponseRedirect('/app/end/', {'loggedIn': loggedIn, 'firstName': firstName, 'noOfItems': noOfItems})


# @app.route("/bill")
def address(request):
    if 'email' not in request.session:
        return render(request, 'loginForm')
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    if noOfItems == 0:
        return HttpResponseRedirect('/app/')
    email = request.session['email']
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT userId FROM app_users WHERE email = '" + email + "'")
    userId = cursor.fetchone()[0]
    cursor.execute("SELECT app_products.productId, app_products.name, app_products.price, app_products.image FROM app_products, app_cart WHERE app_products.productId = app_cart.productId_id AND app_cart.userId_id = " + str(userId))
    products = cursor.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    cursor.execute("SELECT address,postcode,mobile,email_id FROM app_address WHERE email_id = '" + email + "'")
    addr = cursor.fetchall()
    return render(request, "bill.html",
                  {'loggedIn': loggedIn, 'firstName': firstName, 'noOfItems': noOfItems, 'products': products,
                   'totalPrice': totalPrice, 'addr': addr, 'email': email})


# @app.route("/cart")
def order(request):
    if 'email' not in request.session:
        return render(request, 'login.html')
    loggedIn, firstName, noOfItems = getLoginDetails(request)
    email = request.session['email']
    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()
    cursor.execute("SELECT userId FROM app_users WHERE email = '" + email + "'")
    userId = cursor.fetchone()[0]
    cursor.execute("SELECT productId, name, price, image FROM app_order WHERE  app_order.userId_id = '" + str(userId)+"'")
    products = cursor.fetchall()
    return render(request, "order.html",
                  {'products': products,     'loggedIn': loggedIn, 'firstName': firstName,
                   'noOfItems': noOfItems})

def recover(request):
    if request.method == 'POST':
        email = request.session['email']
        password = request.POST.get("password", False)
        if is_valid(email, password):
            db = sqlite3.connect('db.sqlite3')
            cursor = db.cursor()
            cursor.execute("DELETE FROM app_users WHERE email = '" + email + "'")
            password = request.POST.get("newpassword", False)
            firstName = request.POST.get("firstName", False)
            try:
                cursor.execute('INSERT INTO app_users (password, email, firstName) VALUES (?, ?, ?)',
                               (hashlib.md5(password.encode()).hexdigest(), email, firstName))
                db.commit()
            except:
                db.rollback()
            db.close()
            return render(request, 'login.html')


def recoverForm(request):
    return render(request, 'recover.html')




