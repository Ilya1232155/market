from flask import Flask, request, jsonify
from models import db, Product


app = Flask(__name__)


app.config['SECRET_KEY'] = "this_badass_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
	db.drop_all()
	db.create_all()
	
	product1 = Product(123000, "Меховые наручники")
	product2 = Product(123001, "Удлинитель электрический, 3м")
	db.session.add(product1)
	db.session.add(product2)
	
	user1 = User("user1.mail.ru", "password123")
	user2 = User("user2.mail.ru", "password321")
	db.session.add(user1)
	db.session.add(user2)
	user2.admin=True
	
	card1=Card(1, 1, 1)
	card2=Card(2, 2, 2)
	db.session.add(card1)
	db.session.add(card2)
	
	db.session.commit()

@app.route("/api/products", methods = ["POST", "GET"])
def products():
	if request.method == "GET":
		products_list = {"products": []}
		products_data = Product.query.all()
		for p in products_data:
			print(p.articul, p.name, p.description, p.id)
			product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
			products_list["products"].append(product)
		return jsonify(products_list)
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
def cards():
	if request.method == "GET":
		products_list = {"products": []}
		products_data = Product.query.all()
		for p in products_data:
			print(p.articul, p.name, p.description, p.id)
			product = {"id":p.id,"articul":p.articul,"name":p.name,"description":p.description}
			products_list["products"].append(product)
		return jsonify(products_list)

app.run()
