from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# In-memory data storage
expense_list = []

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Add expense
@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']

    expense = {
        'id': str(uuid.uuid4()),
        'title': title,
        'amount': amount,
        'category': category,
        'description': description
    }

    expense_list.append(expense)
    return redirect(url_for('show_expenses'))

# Expense list with optional category filter
@app.route('/expenses')
def show_expenses():
    selected_category = request.args.get('category')
    if selected_category:
        filtered_expenses = [e for e in expense_list if e['category'] == selected_category]
    else:
        filtered_expenses = expense_list

    categories = sorted(set(e['category'] for e in expense_list))

    return render_template(
        'expenses.html',
        expenses=filtered_expenses,
        categories=categories,
        selected_category=selected_category
    )

# Expense detail
@app.route('/expense/<expense_id>')
def expense_detail(expense_id):
    expense = next((e for e in expense_list if e['id'] == expense_id), None)
    if not expense:
        return "Expense not found", 404
    return render_template('expense_detail.html', expense=expense)

if __name__ == '__main__':
    app.run(debug=True)
