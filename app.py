from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scrape_gju import scrape_gju_staff

app = Flask(__name__, static_url_path='', static_folder='public')
CORS(app)

# Serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Handle the search route
@app.route('/search', methods=['POST'])
def search_staff():
    try:
        staff_name = request.json['staffName'].lower()  # Convert to lowercase for case-insensitive search
        page = 0

        # Call the scraping function from scrape_gju.py
        result = scrape_gju_staff(staff_name, page)
        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
