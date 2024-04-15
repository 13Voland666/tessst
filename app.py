from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///X:/JOB/stas/finans/transactions.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(100))
    amount = db.Column(db.Float)

    def __repr__(self):
        return f'<Transaction {self.id}>'

# Оборачиваем create_all() в контекст приложения
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    transactions = Transaction.query.all()
    total_amount = sum(transaction.amount for transaction in transactions)
    return render_template('index.html', transactions=transactions, total_amount=total_amount)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    info = request.form['info']
    amount = float(request.form['amount'])
    transaction = Transaction(info=info, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return '', 204

@app.route('/add_transaction1', methods=['POST'])
def add_transaction1():
    info = request.form['info']
    amount = float(request.form['amount'])*-1
    transaction = Transaction(info=info, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return '', 204

@app.route('/delete_transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))  # Перенаправляем на главную страницу после удаления

if __name__ == '__main__':
    app.run(debug=True)
