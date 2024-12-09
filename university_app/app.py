from flask import Flask, render_template, request, redirect, url_for
from utils.db import db
from models.rankings import University
from models.contact import Contact

# Initialize Flask app
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rankings.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(flask_app)

# Create database tables within the app context
with flask_app.app_context():
    db.create_all()

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        # Fetch form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Save to the database
        contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to a 'thank you' or home page
    return render_template('contact_us.html')

@flask_app.route('/dashboard')
def dashboard():
    # Data processing for regions
    regions = [uni.region for uni in University.query.all()]
    unique_regions = list(set(regions))
    university_counts = [regions.count(region) for region in unique_regions]
    average_scores = [sum([uni.total for uni in University.query.filter_by(region=region)]) / university_counts[idx]
                      for idx, region in enumerate(unique_regions)]

    # Data processing for disciplines
    disciplines = [uni.discipline for uni in University.query.all()]
    unique_disciplines = list(set(disciplines))
    discipline_university_counts = [disciplines.count(discipline) for discipline in unique_disciplines]

    data = {
        'regions': unique_regions,
        'university_counts': university_counts,
        'average_scores': average_scores,
        'disciplines': unique_disciplines,
        'discipline_university_counts': discipline_university_counts
    }
    return render_template('dashboard.html', data=data)


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
    specialized_rankings = request.form['specialized_rankings']
    alumni = int(request.form['alumni'])
    award = int(request.form['award'])
    hici = int(request.form['hici'])
    n_s = int(request.form['n_s'])
    pub = int(request.form['pub'])
    pcp = int(request.form['pcp'])

    total = alumni + award + hici + n_s + pub + pcp

    # Add or update the university record
    if 'id' in request.form and request.form['id']:
        university_id = int(request.form['id'])
        university = University.query.get(university_id)
        if university:
            university.name = name
            university.region = region
            university.discipline = discipline
            university.specialized_rankings = specialized_rankings
            university.alumni = alumni
            university.award = award
            university.hici = hici
            university.n_s = n_s
            university.pub = pub
            university.pcp = pcp
            university.total = total
    else:
        university = University(
            name=name, region=region, discipline=discipline,
            specialized_rankings=specialized_rankings, alumni=alumni, award=award,
            hici=hici, n_s=n_s, pub=pub, pcp=pcp, total=total
        )
        db.session.add(university)

    db.session.commit()
    return redirect(url_for('rankings'))

@flask_app.route('/rankings')
def rankings():
    search_query = request.args.get('search', '')
    sorted_data = University.query.order_by(University.total.desc()).all()
    if search_query:
        sorted_data = [item for item in sorted_data if search_query.lower() in item.name.lower()]
    return render_template('rankings.html', data=sorted_data, search_query=search_query)

@flask_app.route('/edit/<int:id>')
def edit_university(id):
    university = University.query.get(id)  # Fetch the record from the database
    if not university:
        return "Record not found", 404
    return render_template('get_ranked.html', record=university)

@flask_app.route('/delete/<int:id>')
def delete_university(id):
    university = University.query.get(id)  # Fetch the record from the database
    if university:
        db.session.delete(university)  # Delete the record
        db.session.commit()  # Commit the changes
    return redirect(url_for('rankings'))

if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=8004,
        debug=True
    )
