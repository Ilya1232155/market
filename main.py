from flask import Flask, request, jsonify
from models import db, Product, User, Cart
#здесь был вася

app = Flask(__name__)


app.config['SECRET_KEY'] = "this_badass_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
	db.drop_all()
	db.create_all()
	
	product1 = Product(123000, "Меховые наручники", 2000)
	product2 = Product(123001, "Удлинитель электрический, 3м",520)
	db.session.add(product1)
	db.session.add(product2)
	
	user1 = User("user1.mail.ru", "password123")
	user2 = User("user2.mail.ru", "password321")
	db.session.add(user1)
	db.session.add(user2)
	user2.admin=True
	
	cart1=Cart(1, 1, 1)
	cart2=Cart(2, 2, 2)
	db.session.add(cart1)
	db.session.add(cart2)
	
	db.session.commit()

@app.route("/api/products", methods = ["POST", "GET"])
def products():
	if request.method == "GET":
		products_list = {"products": []}
		products_data = Product.query.all()
		for p in products_data:
			product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
			products_list["products"].append(product)
		return jsonify(products_list)
	if request.method == "POST":
		data = request.json
		articul = data['articul']
		name = data['name']
		cost = data['cost']

		product = Product.query.filter_by(articul=articul).first()
		if product:
			return {"error":"Articul already registered"}
		product = Product.query.filter_by(name=name).first()
		if product:
			return {"error": "Name already registered"}
		product = Product(articul,name,cost)
		try:
			description = data.get('description')
			product.description = description
		except:
			pass
		db.session.add(product)
		db.session.commit()
		return {"message":"Product was add in database"}

@app.route("/api/products/<p_id>", methods = ["GET", "PUT", "DELETE"])
def product_page(p_id):
	if request.method == "GET":
		products_list = {"products": []}
		p = Product.query.filter_by(id=p_id).first_or_404()
		product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
		products_list["products"].append(product)
		return jsonify(products_list)
	if request.method == "PUT":
		data = request.json
		articul = data['articul']
		name = data['name']
		cost = data['cost']
		description = data['description']
		product = Product.query.filter_by(articul=articul).first()
		if product:
			return {"error": "Articul already registered"}
		product = Product.query.filter_by(name=name).first()
		if product:
			return {"error": "Name already registered"}
		product = Product.query.filter_by(id=p_id).first_or_404()
		product.articul = articul
		product.name = name
		product.cost = cost
		product.description = description
		db.session.add(product)
		db.session.commit()
		return {"message": "Product was updated in database"}
	if request.method == "DELETE":
		product = Product.query.filter_by(id=p_id).first_or_404()
		db.session.delete(product)
		return {"message": "Product was deleted from database"}
	
@app.route("/api/users", methods = ["POST", "GET"])
def users():
	if request.method == "GET":
		users_list = {"users": []}
		users_data = User.query.all()
		for u in users_data:
			user = {"id":u.id,"email":u.email}
			users_list["users"].append(user)
		return jsonify(users_list)
	if request.method == "POST":
		data = request.json
		email = data["email"]
		password = data["password"]
		pass_confirm = data["pass_confirm"]
		admin = data["admin"]
		user = User.query.filter_by(email=email).first()
		if user:
			return {"error": "email already registered"}
		if password != pass_confirm:
			return {"error": "Password not confirmed"}
		user = User(email, password)
		user.admin = admin
		db.session.add(user)
		db.session.commit()
		return {"message": f"User {email} was registered"}

#Добавить обработчик для конкретного пользователя - получить, изменить, удалить
#@app.route("/api/users/<p_id>", methods = ["GET", "PUT", "DELETE"])
			


@app.route("/api/cards", methods = ["POST", "GET"])
def carts():
	#Исправить обработчик, чтоб выдавал записи в корзине, а не товары
	if request.method == "GET":
		products_list = {"products": []}
		products_data = Product.query.all()
		for p in products_data:
			print(p.articul, p.name, p.description, p.id)
			product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
			products_list["products"].append(product)
		return jsonify(products_list)

	if request.method == "POST":
		data=request.json
		user_id=data["user_id"]
		product_id=["product_id"]
		count=["count"]
		cart = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
		if cart:
			cart.count=count
		else:
			cart=Cart(user_id, product_id, count)
		
		db.session.add(cart)
		db.session.commit()
		return {"message":"Cart was add in database"}
#Добавить обработчик для записи в корзине - получить, изменить, удалить
#@app.route("/api/carts/<p_id>", methods = ["GET", "PUT", "DELETE"])

app.run()
