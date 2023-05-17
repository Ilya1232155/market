from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Product(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	articul = db.Column(db.Integer, unique=True, nullable=False)
	name = db.Column(db.String(150), nullable=False, unique=True)
	description = db.Column(db.String(2000))
	cost=db.Column(db.Integer)

	def __init__(self, articul, name, cost):
		self.articul = articul
		self.name = name
		self.description = ""
		self.cost=cost

class User(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String(1000), unique=True, nullable=False)
	admin=False
	password=db.Column(db.String(150), nullable=False)
	def __init__(self, email, password):
		self.email=email
		self.password=password

class Cart(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	user_id=db.Column(db.Integer)
	product_id=db.Column(db.Integer)
	count=db.Column(db.Integer)

	def __init__(self, product_id, user_id, count):
		self.product_id=product_id
		self.user_id=user_id
		self.count=count
