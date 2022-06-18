from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

ROWS_PER_PAGE = 5


app = Flask(__name__)
app.config['SECRET_KEY'] = 'torqata'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netflix.db'
db = SQLAlchemy(app)

class netflix_titles(db.Model):
    show_id = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    director = db.Column(db.Text, default=None)
    cast = db.Column(db.Text, default=None)
    country = db.Column(db.Text, default=None)
    date_added = db.Column(db.Text, default=None)
    release_year = db.Column(db.BigInteger, nullable=False)
    rating = db.Column(db.Text, default=None)
    duration = db.Column(db.Text, default=None)
    listed_in = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, default=None)

    def __repr__(self):
        return f'<netflix_titles {self.show_id}>'




@app.route('/')
def index():

    shows = netflix_titles.query.all()
    return render_template('index.html', shows=shows)

@app.route('/<string:id>/')
def search(id):
    show = netflix_titles.query.get_or_404(id)
    return render_template('show.html', show=show)


@app.route('/pagination/<int:page_num>')
def paging(page_num):
    data = netflix_titles.query.paginate(per_page=20, page=page_num, error_out=True)
    shows = data.items
    return render_template('index.html', shows=shows)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        show_id = request.form['show_id']
        type = request.form['type']
        director = request.form['director']
        cast = request.form['cast']
        country = request.form['country']
        date_added = request.form['date_added']
        release_year = int(request.form['release_year'])
        rating = request.form['rating']
        duration = request.form['duration']
        listed_in = request.form['listed_in']
        description = request.form['description']
        show = netflix_titles(title = title, show_id = show_id,
            type = type, director = director, cast = cast, country = country,
            date_added = date_added, release_year = release_year, rating = rating,
            duration = duration, listed_in = listed_in, description = description)
        db.session.add(show)
        db.session.commit()

    return render_template('create.html')


@app.route('/<string:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    show = netflix_titles.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form['title']
        show_id = request.form['show_id']
        type = request.form['type']
        director = request.form['director']
        cast = request.form['cast']
        country = request.form['country']
        date_added = request.form['date_added']
        release_year = int(request.form['release_year'])
        rating = request.form['rating']
        duration = request.form['duration']
        listed_in = request.form['listed_in']
        description = request.form['description']

        show.title = title
        show.show_id = show_id
        show.type = type
        show.director = director
        show.cast = cast
        show.country = country
        show.date_added = date_added
        show.release_year = release_year
        show.rating = rating
        show.duration = duration
        show.listed_in = listed_in
        show.description = description

        db.session.add(show)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', show=show)


@app.route('/<string:id>/delete/')
def delete(id):
    show = netflix_titles.query.get_or_404(id)
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/aggregate')
def aggregate():
    
    return

# Functions under here currently do not work

@app.route('/filter/<string:user_in>')
def filtering(user_in):
    data = netflix_titles.query.items.filter(netflix_titles.listed_in.ilike(user_in)).all()
    shows = data.items
    return render_template('filter.html', shows=shows)

# @app.route('/filter/Documentaries')
# def documentary():
#     documentary = netflix_titles.query.filter(netflix_titles.listed_in.ilike("Documentaries")).all()
#     shows = documentary.items
#     return render_template('filter.html', shows=shows)

@app.route('/sorting')
def sorting():
    sort_shows = netflix_titles.query.order_by(netflix_titles.release_year.desc()).limit(5).all()
    shows = sort_shows.items
    return render_template('index.html', shows=shows)




if __name__ =="__main__":
    app.run(debug=True)