from flask import Flask, render_template, request, redirect, url_for

from utils.db import db

from models.rankings import *

# Initialize Flask app
flask_app = Flask(__name__)
rankings_data = []
next_id = 1


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/categories')
def categories():
    return render_template('categories.html')


@flask_app.route('/articles')
def articles():
    return render_template('articles.html')


@flask_app.route('/about')
def about():
    return render_template('about.html')


@flask_app.route('/get_ranked')
def get_ranked():
    return render_template('get_ranked.html')


@flask_app.route('/submit', methods=['POST'])
def submit_university():
    global next_id
    name = request.form['name']
    region = request.form['region']
    discipline = request.form['discipline']
    specialized_rankings = int(request.form['specialized_rankings'])
    alumni = int(request.form['alumni'])
    award = int(request.form['award'])
    hici = int(request.form['hici'])
    n_s = int(request.form['n_s'])
    pub = int(request.form['pub'])
    pcp = int(request.form['pcp'])

    # Check if editing or adding new
    if 'id' in request.form and request.form['id']:
        university_id = int(request.form['id'])
        for record in rankings_data:
            if record['id'] == university_id:
                record.update({
                    'name': name, 'region': region, 'discipline': discipline,
                    'specialized_rankings': specialized_rankings,
                    'alumni': alumni, 'award': award,
                    'hici': hici, 'n_s': n_s, 'pub': pub, 'pcp': pcp,
                    'total': alumni + award + hici + n_s + pub + pcp + specialized_rankings
                })
                break
    else:
        rankings_data.append({
            'id': next_id,
            'name': name,
            'region': region,
            'discipline': discipline,
            'specialized_rankings': specialized_rankings,
            'alumni': alumni,
            'award': award,
            'hici': hici,
            'n_s': n_s,
            'pub': pub,
            'pcp': pcp,
            'total': alumni + award + hici + n_s + pub + pcp + specialized_rankings
        })
        next_id += 1



    return redirect(url_for('rankings'))


@flask_app.route('/rankings')
def rankings():
    search_query = request.args.get('search', '')
    sorted_data = sorted(rankings_data, key=lambda x: x['total'], reverse=True)
    if search_query:
        sorted_data = [item for item in sorted_data if search_query.lower() in item['name'].lower()]
    return render_template('rankings.html', data=sorted_data, search_query=search_query)


@flask_app.route('/edit/<int:id>')
def edit_university(id):
    record = next((item for item in rankings_data if item['id'] == id), None)
    if not record:
        return "Record not found", 404
    return render_template('get_ranked.html', record=record)


@flask_app.route('/delete/<int:id>')
def delete_university(id):
    global rankings_data
    rankings_data = [item for item in rankings_data if item['id'] != id]
    return redirect(url_for('rankings'))
if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=8004,
        debug=True
    )
