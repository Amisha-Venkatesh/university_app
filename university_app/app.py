from flask import Flask, render_template, request, redirect, url_for
from utils.db import db
from models.rankings import Rankings

flask_app = Flask(__name__)

flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rankings.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(flask_app)

def seed_database():
    if not Rankings.query.first():  
        mock_data = [
            Rankings(name=f"University {i}", region="Region A", discipline="Discipline X",
                     specialized_rankings=10 + i, alumni=50 + i, award=20 + i,
                     hici=30 + i, n_s=40 + i, pub=100 + i, pcp=5 + i,
                     total=(10 + i + 50 + i + 20 + i + 30 + i + 40 + i + 100 + i + 5 + i))
            for i in range(1, 21)
        ]
        db.session.bulk_save_objects(mock_data)
        db.session.commit()

with flask_app.app_context():
    db.create_all()
    seed_database()

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
    total = specialized_rankings + alumni + award + hici + n_s + pub + pcp

    university_id = request.form.get('id')
    if university_id:  # Update existing record
        record = Rankings.query.get(int(university_id))
        if record:
            record.name = name
            record.region = region
            record.discipline = discipline
            record.specialized_rankings = specialized_rankings
            record.alumni = alumni
            record.award = award
            record.hici = hici
            record.n_s = n_s
            record.pub = pub
            record.pcp = pcp
            record.total = total
    else:  # Add new record
        new_record = Rankings(name=name, region=region, discipline=discipline,
                              specialized_rankings=specialized_rankings, alumni=alumni,
                              award=award, hici=hici, n_s=n_s, pub=pub, pcp=pcp,
                              total=total)
        db.session.add(new_record)

    db.session.commit()
    return redirect(url_for('rankings'))


@flask_app.route('/rankings')
def rankings():
    search_query = request.args.get('search', '').strip()
    if search_query:
        sorted_data = Rankings.query.filter(
            Rankings.name.ilike(f"%{search_query}%")
        ).order_by(Rankings.total.asc()).all()
    else:
        sorted_data = Rankings.query.order_by(Rankings.total.asc()).all()
    return render_template('rankings.html', data=sorted_data, search_query=search_query)



@flask_app.route('/edit/<int:id>')
def edit_university(id):
    record = Rankings.query.get(id)
    if not record:
        return "Record not found", 404
    return render_template('get_ranked.html', record=record)


@flask_app.route('/delete/<int:id>')
def delete_university(id):
    record = Rankings.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect(url_for('rankings'))


if __name__ == '__main__':
    flask_app.run(host='127.0.0.1', port=8004, debug=True)
