from flask import Flask, request, jsonify
try:
    from flask_sqlalchemy import SQLAlchemy
except Exception as e:
    raise ImportError("Missing dependency 'flask_sqlalchemy'. Install with: pip install flask-sqlalchemy") from e

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"{self.name}-{self.description}"


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    
    output = [] 
    for drink in drinks:
        output.append({
            'id': drink.id,
            'name': drink.name,
            'description': drink.description,
        })
        
    return {
        "drinks": output
    }

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {
        'id': drink.id,
        'name': drink.name,
        'description': drink.description,
    }
    
@app.route('/drinks/<id>', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json.get('description'))
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id, 'name': drink.name, 'description': drink.description}, 201

def add_drink(name, description=None):
    with app.app_context():
        drink = Drink(name=name, description=description)
        db.session.add(drink)
        db.session.commit()
        return {
            'id': drink.id,
            'name': drink.name,
            'description': drink.description,
        }


@app.route('/drinks', methods=['POST'])
def create_drink():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'name is required'}), 400

    drink = add_drink(name, description)
    return jsonify(drink), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)