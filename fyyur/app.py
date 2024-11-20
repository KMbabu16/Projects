#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import (Flask, 
                  jsonify, 
                  render_template, 
                  request, 
                  flash, 
                  redirect, 
                  url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,update
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from collections import defaultdict
from datetime import datetime
from models import db, Venue, Show, Artist
#--------------------------------------------------cls--------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
with app.app_context():

    # Add initial data only if the table is empty
    if Venue.query.count() == 0:
        # Venue 1
        venue1 = Venue(
            name="The Musical Hop",
            genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            address="1015 Folsom Street",
            city="San Francisco",
            state="CA",
            phone="123-123-1234",
            website_link="https://www.themusicalhop.com",
            facebook_link="https://www.facebook.com/TheMusicalHop",
            seeking_talent=True,
            seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
            image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        )

        # Venue 2
        venue2 = Venue(
            name="The Dueling Pianos Bar",
            genres=["Classical", "R&B", "Hip-Hop"],
            address="335 Delancey Street",
            city="New York",
            state="NY",
            phone="914-003-1132",
            website_link="https://www.theduelingpianos.com",
            facebook_link="https://www.facebook.com/theduelingpianos",
            seeking_talent=False,
            image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
        )

        # Venue 3
        venue3 = Venue(
            name="Park Square Live Music & Coffee",
            genres=["Rock n Roll", "Jazz", "Classical", "Folk"],
            address="34 Whiskey Moore Ave",
            city="San Francisco",
            state="CA",
            phone="415-000-1234",
            website_link="https://www.parksquarelivemusicandcoffee.com",
            facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            seeking_talent=False,
            image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
        )

        # Add the venues to the session
        db.session.add_all([venue1, venue2, venue3])
        db.session.commit()
    if Artist.query.count() == 0:
      artist1 = Artist(
      name="Guns N Petals",
        genres=["Rock n Roll"],  # Ensure the column supports array types if using Postgres.
        city="San Francisco",
        state="CA",
        phone="326-123-5000",
        website_link="https://www.gunsnpetalsband.com",
        facebook_link="https://www.facebook.com/GunsNPetals",
        seeking_venue=True,
        seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
        image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        )

      artist2 = Artist(
        name="Matt Quevedo",
        genres=["Jazz"],  # Ensure your database supports array/list types for genres if needed.
        city="New York",
        state="NY",
        phone="300-400-5000",
        facebook_link="https://www.facebook.com/mattquevedo923251523",
        seeking_venue=False,
        image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
        )
      artist3 = Artist(
        name="The Wild Sax Band",
        genres=["Jazz", "Classical"],  # Make sure your database supports array types if needed
        city="San Francisco",
        state="CA",
        phone="432-325-5432",
        seeking_venue=False,
        image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
        )
      db.session.add_all([artist1, artist2, artist3])
      db.session.commit()
    if Show.query.count() == 0:
        show1=Show(
          venue_id= 1,
          artist_id= 2,
          start_time=datetime.strptime( "2025-05-21T21:30:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        show2=Show(
          venue_id= 1,
          artist_id= 1,
          start_time=datetime.strptime( "2025-06-15T23:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        show3=Show(
          venue_id= 2,
          artist_id= 3,
          start_time=datetime.strptime( "2035-04-01T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        show4=Show(
          venue_id= 2,
          artist_id= 2,
          start_time=datetime.strptime("2035-04-01T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        )
        db.session.add_all([show1, show2, show3,show4])
        db.session.commit()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues') 
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    venue_data = defaultdict(lambda: {"city": None, "state": None, "venues": []})
    venues = Venue.query.all()
    
    for venue in venues:
        city = venue.city
        state = venue.state

        # Count upcoming shows for each venue by querying the Show model
        upcoming_shows = db.session.query(Show).filter(
            Show.venue_id == venue.id,
            func.to_timestamp(Show.start_time, 'YYYY-MM-DD"T"HH24:MI:SS.MSZ') > datetime.now()
            ).count()
        venue_data[(city, state)]["city"] = city
        venue_data[(city, state)]["state"] = state
        venue_data[(city, state)]["venues"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": upcoming_shows
        })

    data = list(venue_data.values())
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST']) 
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')

  search_results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()


  response = {
      "count": len(search_results),  
      "data": []  
  }

  for venue in search_results:

      upcoming_shows_count = db.session.query(Show).filter(
          Show.venue_id == venue.id,
          Show.start_time > datetime.now().isoformat()
      ).count()

      response["data"].append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": upcoming_shows_count
      })

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
    venue = db.session.get(Venue,venue_id)    
    shows=db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id).all()
    upcoming_shows = []
    past_shows = []

    for show in shows:
        start_time_str = show.start_time
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

        show_info={
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": start_time
            }
        if start_time <= datetime.now():
          past_shows.append(show_info)
        else:
          upcoming_shows.append(show_info)
    venue=Venue.query.get_or_404(venue_id)
    data=venue.__dict__
    data['past_shows']=past_shows
    data['upcoming_shows']=upcoming_shows
    data['past_shows_count']=len(past_shows)
    data['upcoming_shows_count']=len(upcoming_shows)
    print(data)
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST']) 
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form, meta={'csrf':False})
  if form.validate():
    try:
      genres=form.genres.data
      genres = [genres] if genres else []
      venue = Venue(
          name=form.name.data,
          genres=genres,
          address=form.address.data,
          city=form.city.data,
          state=form.state.data,
          phone=form.phone.data,
          website_link=form.website_link.data,
          facebook_link=form.facebook_link.data,
          seeking_talent=form.seeking_talent.data,
          image_link=form.image_link.data
      )

      # Add the venues to the session
      db.session.add(venue)
      db.session.commit()
      flash(f"Venue form {form.name.data}submitted successfully")
    except Exception as e:
        error = True
        db.session.rollback()
        print(f"Error occurred in venue creation: {e}")
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE']) 
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)

        if venue is None:
            return jsonify({"error": "Venue not found"}), 404        
        shows = Show.query.filter_by(venue_id=venue_id).all()
        for show in shows:
            db.session.delete(show)
        db.session.delete(venue)
        db.session.commit()
        return render_template('pages/home.html')
    except :
        db.session.rollback()
        print(f"Error while deleting venue")
        return jsonify({"error": "An error occurred while deleting the venue"}), 500

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists') 
def artists():
  # TODO: replace with real data returned from querying the database
  artist_data = []
  artists=Artist.query.all()
  for artist in artists:
    artist_entry={
       "id":artist.id,
       "name":artist.name
    }
    artist_data.append(artist_entry)

  return render_template('pages/artists.html', artists=artist_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_artist = request.form.get('search_term', '')

  search_results = Artist.query.filter(Artist.name.ilike(f'%{search_artist}%')).all()

  response = {
      "count": len(search_results),  
      "data": []  
  }

  for artist in search_results:
      results_count = db.session.query(Artist).filter(
          Show.artist_id == artist.id,
          Show.start_time > datetime.now().isoformat()
      ).count()
      response["data"].append({
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": results_count
      })

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>') 

def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    artist = db.session.get(Artist, artist_id)    
    now = datetime.now()
    shows = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).all()
    print(shows)
    upcoming_shows = []
    past_shows = []

    for show in shows:
        print(show)
        start_time_str = show.start_time
        start_time = datetime.strptime(start_time_str,"%Y-%m-%d %H:%M:%S")
        show_info={
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": start_time
            }
        if start_time <= datetime.now():
           past_shows.append(show_info)
        else:
           upcoming_shows.append(show_info)    
    artist=Artist.query.get_or_404(artist_id)   
    data=artist.__dict__
    artist_genres=data['genres']
    print(artist_genres)
    data['upcoming_shows_count']=len(upcoming_shows)
    data['past_shows_count']=len(past_shows)
    data['upcoming_shows']=upcoming_shows
    data['past_shows']=past_shows
    print(data)
    return render_template('pages/show_artist.html', artist=data)
@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:        
      shows = db.session.query(Show).filter(Show.artist_id == artist_id).all()      
      print(shows)
      if shows:
        for show in shows:
            db.session.delete(show)
            db.session.commit()
      artist = db.session.get(Artist,artist_id)
      print(artist)
      if artist:
          db.session.delete(artist)
          db.session.commit()
          return render_template('pages/home.html')
      else:    
          return jsonify({"error": "artist not found"}), 404
    except:
        db.session.rollback()        
        print(f"Error while deleting artist")
        return jsonify({"error": "An error occurred while deleting the artist"}), 500  
    finally:
        db.session.close()
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist=db.session.get(Artist,artist_id)
  form = ArtistForm(obj=artist)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    form = request.form
    genres=form.genres.data
    print(genres)
    if not isinstance(genres, list):
      genres = [genres]

    print(genres)
    result=db.session.execute( update(Artist).where(Artist.id == artist_id).values({            
              "name":form.name.data,
              "city":form.city.data,
              "state":form.state.data,
              "phone":form.phone.data,
              "genres":genres,
              "website_link":form.website_link.data,
              "image_link":form.image_link.data,
              "facebook_link":form.facebook_link.data,                      
              "seeking_venue":form.seeking_venue.data,
              "seeking_description":form.seeking_description.data
            }))
    db.session.commit()
    print(result)
    # TODO: populate form with fields from artist with ID <artist_id>
    return  redirect(url_for('show_artist', artist_id=artist_id))




@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue=db.session.get(Venue,venue_id)
  form = VenueForm(obj=venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form, meta={'csrf': False})
    data = request.form
    genres=data.get('genres')
    genres = [genres] if genres else []
    db.session.execute(update(Venue).where(Venue.id==venue_id).values({
        "name":form.name.data,
        "genres":genres,
        "address":form.address.data,
        "city":form.city.data,
        "state":form.state.data,
        "phone":form.phone.data,
        "website_link":form.website_link.data,
        "facebook_link":form.facebook_link.data,
        "seeking_talent":form.seeking_talent.data,
        "image_link":form.image_link.data
      }))
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id)) 

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form, meta={'csrf':False})
  if form.validate():
      try:
          genres = form.genres.data
          
          # Create a new Artist instance with form data
          artist = Artist(
              name=form.name.data,
              city=form.city.data,
              state=form.state.data,
              phone=form.phone.data,
              genres=genres,
              website_link=form.website_link.data,
              image_link=form.image_link.data,
              facebook_link=form.facebook_link.data,
              seeking_venue=form.seeking_venue.data,
              seeking_description=form.seeking_description.data
          )

          db.session.add(artist)
          db.session.commit()

          flash(f'Artist {form.name.data} was successfully listed!')
          return render_template('pages/home.html')
      
      except Exception as e:
          db.session.rollback()

          print(f"Error while adding artist: {e}")

          flash(f'An error occurred. Artist {form.name.data} could not be listed.')
          
          return jsonify({"error": "An error occurred while creating the artist"}), 500
      
      finally:

          db.session.close()
  
  else:
      flash('Form validation failed. Please check the data entered.')
      return render_template('forms/new_artist.html', form=form), 400
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')#Working fine
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    show_data = []
    shows_all=Show.query.all()
    for show in shows_all:
      venues=Venue.query.get(show.venue_id)
      artists=Artist.query.get(show.artist_id)

      show_entry={
        "venue_id":show.venue_id,
        "venue_name": venues.name,
        "artist_id":show.artist_id,
        "artist_name": artists.name,
        "artist_image_link": artists.image_link,
        "start_time": show.start_time
      }
      show_data.append(show_entry)
    return render_template('pages/shows.html', shows=show_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form, meta={'csrf':False})
  if form.validate():
    try:
      show=Show(           
                venue_id=form.venue_id.data,
                artist_id=form.artist_id.data,
                start_time=form.start_time.data
              )
      db.session.add(show)
      db.session.commit()
    # on successful db insert, flash success
      flash('Show was successfully listed!')
      return render_template('pages/home.html')
    except:
      flash(f'An error occurred. show {form.artist_id.data} could not be listed.')
      db.session.rollback()        
      return jsonify({"error": "Show could not be listed"}), 500   
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
