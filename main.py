#look learn explore

import csv
from flask import Flask, request, jsonify, render_template

# Load the dataset
data = {}
with open('final_cleaned_11.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        verse_num = row['Verse_Number'].replace('Verse ', '')
        data[verse_num] = row

def search_by_verse(verse_num):
    """Search for a verse by its number (e.g., '1.1')"""
    if verse_num in data:
        return data[verse_num]
    else:
        return None

def search_by_text(query):
    """Search for verses containing the query in Verse or Meaning"""
    results = []
    for verse_num, row in data.items():
        if query.lower() in row['Verse'].lower() or query.lower() in row['Verse_Meaning'].lower():
            results.append(row)
    return results

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    search_type = request.args.get('type')
    query = request.args.get('query')
    if not search_type or not query:
        return jsonify({"error": "Missing 'type' or 'query' parameter"}), 400
    if search_type == 'verse':
        result = search_by_verse(query)
        if result:
            return jsonify([result])
        else:
            return jsonify([])
    elif search_type == 'text':
        results = search_by_text(query)
        return jsonify(results)
    else:
        return jsonify({"error": "Invalid type. Use 'verse' or 'text'"}), 400

if __name__ == "__main__":
    app.run(debug=True)