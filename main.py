from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///batik.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class BatikItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
    
with app.app_context():
    db.create_all()


@app.route('/cms/batik', methods=['GET', 'POST'])
def index_cms_batik_items():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_url = request.form['image_url']
        items = BatikItem(title=title, description=description, image_url=image_url)
        db.session.add(items)
        db.session.commit()
        return redirect(url_for('index_cms_batik_items'))
    else:
        batik = BatikItem.query.all()
        return render_template('index.html', batik=batik)   

@app.route('/cms/batik/<int:id>', methods=['GET', 'POST'])
def edit_cms_batik(id):
    batik = BatikItem.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_url = request.form['image_url']
        items = BatikItem(title=title, description=description, image_url=image_url)
        db.session.delete(batik)
        db.session.add(items)
        db.session.commit()
        return redirect(url_for('index_cms_batik_items'))
    else:
        return render_template('edit_batik.html', batik=batik)

@app.route('/cms/delete/<int:id>')
def delete_cms_batik(id):
    person = BatikItem.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index_cms_batik_items'))

@app.route('/api/batik', methods=['GET'])
def get_batik_items():
        items = BatikItem.query.all()
        return jsonify([{'id': item.id, 'title': item.title, 'description': item.description, 'image_url':item.image_url} for item in items])
    
@app.route('/api/batik/<string:query>', methods=['GET'])
def search_batik_item(query):
        batiks = db.session.query(BatikItem).filter(BatikItem.title.like("%"+query+"%")).all()
        return jsonify([{'id': item.id, 'title': item.title, 'description': item.description, 'image_url':item.image_url} for item in batiks])

@app.route('/api/batik', methods=['POST'])
def create_batik_item():
        data = request.get_json()
        item = BatikItem(title=data['title'], description=data['description'], image_url=data['image_url'])
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'title': item.title, 'description': item.description, 'image_url':item.image_url})

@app.route('/api/batik/<int:item_id>', methods=['PUT'])
def update_batik_item(item_id):
        item = BatikItem.query.get_or_404(item_id)
        data = request.get_json()
        item.title = data['title']
        item.description = data['description']
        item.image_url = data['image_url']
        db.session.commit()
        return jsonify({'id': item.id, 'title': item.title, 'description': item.description, 'image_url':item.image_url})

@app.route('/api/batik/<int:item_id>', methods=['DELETE'])
def delete_batik_item(item_id):
        item = BatikItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return 'delete success', 204


@app.route('/')
def index():
  return 'hello, this api created by beneboba'

if __name__ == '__main__':
  app.run(port=5000)
