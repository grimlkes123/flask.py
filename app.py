from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    dates = request.json.get('dates', [])
    if not dates:
        return jsonify(error="No dates provided"), 400

    return jsonify(forecast={})

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/dataset-preview')
def dataset_preview():
    dataset_path = os.path.join(os.path.dirname(__file__), 'templates', 'Supermart Grocery Sales - Retail Analytics Dataset.csv')
    df = pd.read_csv(dataset_path)
    categories_data = df.to_html(index=False)
    return render_template('dataset_preview.html', categories_data=categories_data)

@app.route('/dataset-result')
def dataset_result():
    dates = request.args.getlist('date')
    return render_template('dataset_result.html', dates=dates)

@app.route('/user-feedback')
def user_feedback():
    return render_template('user_feedback.html')

feedback_data = []

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('feedback')
    feedback_entry = {
        'id': len(feedback_data) + 1,
        'name': name,
        'email': email,
        'feedback': feedback
    }
    feedback_data.append(feedback_entry)
    return jsonify(success=True)

@app.route('/delete-feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    global feedback_data
    feedback_data = [feedback for feedback in feedback_data if feedback['id'] != feedback_id]
    return jsonify(success=True)

@app.route('/customer-feedback')
def customer_feedback():
    return render_template('customer_feedback.html', feedback_data=feedback_data)

@app.route('/photo/<path:filename>')
def photo(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/real_time_data')
def real_time_data():
    dates = request.args.getlist('date')
    dataset_path = os.path.join(os.path.dirname(__file__), 'templates', 'Supermart Grocery Sales - Retail Analytics Dataset.csv')
    df = pd.read_csv(dataset_path)
    
    # Filter data based on selected dates
    filtered_data = df[df['Order Date'].isin(dates)]
    
    # Prepare data for charts
    charts_data = {
        'Bakery': filtered_data[filtered_data['Category'] == 'Bakery'][['Order Date', 'Sales']].to_dict(orient='records'),
        'Beverages': filtered_data[filtered_data['Category'] == 'Beverages'][['Order Date', 'Sales']].to_dict(orient='records'),
        'EggsMeatFish': filtered_data[filtered_data['Category'] == 'Eggs, Meat & Fish'][['Order Date', 'Sales']].to_dict(orient='records'),
        'FoodGrains': filtered_data[filtered_data['Category'] == 'Food Grains'][['Order Date', 'Sales']].to_dict(orient='records'),
        'FruitsVeggies': filtered_data[filtered_data['Category'] == 'Fruits & Veggies'][['Order Date', 'Sales']].to_dict(orient='records'),
        'OilMasala': filtered_data[filtered_data['Category'] == 'Oil & Masala'][['Order Date', 'Sales']].to_dict(orient='records'),
        'Snacks': filtered_data[filtered_data['Category'] == 'Snacks'][['Order Date', 'Sales']].to_dict(orient='records'),
        'Profits': filtered_data[['Order Date', 'Profit']].to_dict(orient='records'),
        'Sales': filtered_data[['Order Date', 'Sales']].to_dict(orient='records'),
        'Regions': filtered_data['Region'].value_counts().to_dict(),
        'Discounts': filtered_data[['Order Date', 'Discount']].to_dict(orient='records')
    }
    
    return render_template('real_time_data.html', dates=dates, charts_data=charts_data)

if __name__ == '__main__':
    app.run(debug=True)