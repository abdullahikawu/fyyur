from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  city = db.Column(db.String(50), nullable=False)
  state = db.Column(db.String(50), nullable=False)
  address = db.Column(db.String(500), nullable=False)
  phone = db.Column(db.String(15), nullable=False)
  image_link = db.Column(db.String(255))
  facebook_link = db.Column(db.String(255))
  genres = db.Column(db.String(120), nullable=False)
  website_link = db.Column(db.String(255))
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='venue', lazy=True)
  
  def __repr__(self):
    return f"{self.id} {self.name} {self.state}"
  # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  city = db.Column(db.String(50), nullable=False)
  state = db.Column(db.String(50), nullable=False)
  phone = db.Column(db.String(15), nullable=False)
  genres = db.Column(db.String(120), nullable=False)
  image_link = db.Column(db.String(255))
  facebook_link = db.Column(db.String(255))
  website_link = db.Column(db.String(255))
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='artist', lazy=True)

  def __repr__(self):
    return f"{self.id} {self.name} {self.state}"
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime)
  
  def __repr__(self):
    return f"{self.id} {self.name} {self.state}"