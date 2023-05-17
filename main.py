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
		db.session.add(product)
		db.session.commit()
		return {"message":"Product was add in database"}

@app.route("/api/users", methods = ["POST", "GET"])
def users():
	if request.method == "GET":
		products_list = {"products": []}
		products_data = Product.query.all()
		for p in products_data:
			print(p.articul, p.name, p.description, p.id)
			product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
			products_list["products"].append(product)
		return jsonify(products_list)

@app.route("/api/cards", methods = ["POST", "GET"])
def carts():
	if request.method == "GET":
		products_list = {"products": []}
		products_data = Product.query.all()
		for p in products_data:
			print(p.articul, p.name, p.description, p.id)
			product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
			products_list["products"].append(product)
		return jsonify(products_list)

app.run()
