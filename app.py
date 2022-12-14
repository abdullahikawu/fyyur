#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import db, Venue, Artist, Show
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
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
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  
  data2 = []
  # fetch distinct records of Venue city and state fields
  categs = db.session.query(Venue.city, Venue.state).distinct().all()
  
  # create a group ( dictionary ) for records with the same state and city
  for categ in categs:
    group = {
      "city": categ[0],
      "state": categ[1],
      "venues": []
    }
    
    # left join Venue and Show, retrive records of venues that fall under current city and state group
    venues = db.session.query(Venue).join(Show, isouter=True).filter(Venue.city==group["city"], Venue.state==group["state"])
    for venue in venues.all():
      group["venues"].append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': venues.filter(Show.venue_id==venue.id, Show.start_time > datetime.now()).count()
      })
    # data current group to return
    data2.append(group)
  
  return render_template('pages/venues.html', areas=data2);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  
  
  response2 = {
      'count': 0,
      'data': []
    }
  
  search = request.form.get('search_term', None)
  if search:
    # left join Venue and Show table, retrieve records from Venue where venue name is like search term
    venues = db.session.query(Venue).join(Show, isouter=True).filter(Venue.name.ilike('%' + search + '%'))
    response2['count'] = venues.count()
    
    if response2['count'] > 0:
      # insert each records found
      for venue in venues.all():
        response2['data'].append({
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': venues.filter(Show.venue_id==venue.id, Show.start_time > datetime.now()).count()
        })
    else:
      flash("Venue '" + search + "' not found")
    print(response2)
  else:
    flash("No search input provided")
  return render_template('pages/search_venues.html', results=response2, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  venue = Venue.query.get_or_404(venue_id)
  
  data2 = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres.split(', '),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0
  }
  print(data2['genres'])
  # find upcoming shows with venue id form Show table 
  upcoming_shows = Show.query.filter(Show.venue_id==venue.id, Show.start_time > datetime.now())
  for show in upcoming_shows.all():
    data2['upcoming_shows'].append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    })
  data2['upcoming_shows_count'] = upcoming_shows.count()
  
  # find past shows with venue id form Show table 
  past_shows = Show.query.filter(Show.venue_id==venue.id, Show.start_time < datetime.now())
  for show in past_shows.all():
    data2['past_shows'].append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    })
  data2['past_shows_count'] =past_shows.count()
  return render_template('pages/show_venue.html', venue=data2)

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
  error = False
  data = {}
  fields = [
    'name',
    'city',
    'state',
    'address',
    'phone',
    'genres',
    'image_link',
    'facebook_link',
    'website_link',
    'seeking_talent',
    'seeking_description',
  ]
  form = VenueForm()
  
  # insert form data into data dict
  for key in fields:
    data[key] = getattr(form, key).data 
  data['genres'] = ', '.join(data['genres'])    # replace string value to boolean
  
  if form.validate_on_submit():
    if data['seeking_talent'] == 'y':
      data['seeking_talent'] = True
    else:
      data['seeking_talent'] = False
    
    # insert new venue to database
    try:
      new_venue = Venue(**data)
      db.session.add(new_venue)
      db.session.commit()
    except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
    finally:
      db.session.close()
  
  if error  or not form.validate_on_submit():
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + data['name'] + ' could not be created. ' + ' and '.join(form.errors))
    return render_template('forms/new_venue.html', form=form)
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.get(venue_id)
  except:
    flash('An error occurred. Venue id ' + str(venue_id) + ' does not exist.')
    return redirect(url_for('venues'))
  
  try:
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue id ' + str(venue_id) + ' could not be removed.')
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    # on successful db insert, flash success
    flash('Venue ' + str(venue_id) + ' was successfully removed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  data2 = []
  artists = db.session.query(Artist).all()
  for artist in artists:
    data2.append({
      'id': artist.id,
      'name': artist.name
    })
  return render_template('pages/artists.html', artists=data2)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  
  response2 = {
      'count': 0,
      'data': []
    }
  
  search = request.form.get('search_term', None)
  # 
  if search:
    # left join Artist and Show table, retrieve records from Artist where Artist name is like the search term
    artists = db.session.query(Artist).join(Show, isouter=True).filter(Artist.name.ilike('%' + search + '%'))
    response2['count'] = artists.count()
    
    # append each records found
    if response2['count'] > 0:
      for artist in artists.all():
        response2['data'].append({
          'id': artist.id,
          'name': artist.name,
          'num_upcoming_shows': artists.filter(Show.artist_id==artist.id, Show.start_time > datetime.now()).count()
        })
    else:
      flash("Artist '" + search + "' not found")
    print(response2)
  else:
    flash("No search input provided")
  return render_template('pages/search_artists.html', results=response2, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  
  artist = Artist.query.get_or_404(artist_id)
  data2 = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(', '),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "image_link": artist.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0
  }
  
  # find upcoming shows with artist id form Show table 
  upcoming_shows = Show.query.filter(Show.artist_id==artist.id, Show.start_time > datetime.now())
  for show in upcoming_shows.all():
    data2['upcoming_shows'].append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    })
  data2['upcoming_shows_count'] =upcoming_shows.count()
  
  # find past shows with artist id form Show table 
  past_shows = Show.query.filter(Show.artist_id==artist.id, Show.start_time < datetime.now())
  for show in past_shows.all():
    data2['past_shows'].append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    })
  data2['past_shows_count'] =past_shows.count()
  return render_template('pages/show_artist.html', artist=data2)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm()
  
  # insert data from db into form fields
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres.split(', ')
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm()
  error = False
  try:
    artist = Artist.query.get(artist_id)
  except:
    flash('An error occurred. Artist id ' + str(artist_id) + ' does not exist.')
    return redirect(url_for('artists'))
  
  
  
  if form.validate_on_submit():
    # update artist  wiith data from form fields 
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = ', '.join(form.genres.data)
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    
    # get record from venue table in database
    try:
      db.session.commit()
    except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
    finally:
      db.session.close()
  
  if error  or not form.validate_on_submit():
    flash('Failed to update Artist id ' + str(artist_id) + '.')
    return render_template('forms/edit_artist.html', form=form, artist=artist)
  flash('Artist id ' + str(artist_id) + ' was updated successfully.')
  return redirect(url_for('edit_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()
  
  # insert form fields wiith data from db
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres.split(', ')
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
    
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  
  try:
    venue = Venue.query.get(venue_id)
  except:
    flash('An error occurred. Venue id ' + str(venue_id) + ' does not exist.')
    return redirect(url_for('venues'))
  
  form = VenueForm()
  if form.validate_on_submit():
    # update table fields wiith data from form fields 
    
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = ', '.join(form.genres.data)
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    
    
    # get record from venue table in database
    try:
      db.session.commit()
    except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
    finally:
      db.session.close()
  
  if error  or not form.validate_on_submit():
    # TODO: populate form with values from venue with ID <venue_id>
    flash('An error occurred. Failed to update Venue id ' + str(venue_id) + '.' + ' and '.join(form.errors))
    return render_template('forms/edit_venue.html', form=form, venue=venue)
  flash('Venue id ' + str(venue_id) + ' was successfully updated.')
  return redirect(url_for('edit_venue', venue_id=venue_id))

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
  
  error = False
  data = {}
  fields = [
    'name',
    'city',
    'state',
    'phone',
    'genres',
    'image_link',
    'facebook_link',
    'website_link',
    'seeking_venue',
    'seeking_description',
  ]
  form = ArtistForm()
  for key in fields:  
    data[key] = getattr(form, key).data # insert form data in data object
  data['genres'] = ', '.join(data['genres'])    # return string value to boolean
  
  if form.validate_on_submit():
    if data['seeking_venue'] == 'y':
      data['seeking_venue'] = True
    else:
      data['seeking_venue'] = False
    
    # insert new artist to database
    try:
      new_artist = Artist(**data)
      db.session.add(new_artist)
      db.session.commit()
    except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
    finally:
      db.session.close()
  print("validate on submit", form.is_submitted())
  if error  or not form.validate_on_submit():
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + data['name'] + ' could not be created.' + ' and '.join(form.errors))
    return render_template('forms/new_artist.html', form=form)
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))
  

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  shows = db.session.query(Show)
  data2 = []
  for show in shows.all():
    data2.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime("%Y-%m-%dT%H:%M:%S")
    })
  print(data2)
  return render_template('pages/shows.html', shows=data2)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  data = {}
  fields = ['artist_id', 'venue_id', 'start_time']
  
  form = ShowForm()
  for key in fields:  
    data[key] = getattr(form, key).data # insert form data object into dict data
  
  if form.validate_on_submit():
    datePattern = str(data["start_time"].date()) + "%" # convert date object to string
    
    # check if show artist is already shedculed for a particular date and return count
    result = db.engine.execute('select COUNT(*) from "Show" where artist_id = %s and start_time::text like %s', (data["artist_id"], datePattern))
    
    if result.fetchone()[0]:
      flash('Artist not available on this date')
      return render_template('forms/new_show.html', form=form)
    # try to insert new show to database
    try:
      new_show = Show(**data)
      db.session.add(new_show)
      db.session.commit()
    except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
    finally:
      db.session.close()
  print("validate on submit", form.is_submitted())
  if error  or not form.validate_on_submit():
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be created.' + ' and '.join(form.errors))
    return render_template('forms/new_show.html', form=form)
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))
  
  
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

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
