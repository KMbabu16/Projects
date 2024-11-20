from datetime import datetime
from enum import Enum
import re
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired,URL,Regexp


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class state(Enum):
            AL='AL'
            AK='AK'
            AZ='AZ'
            AR='AR'
            CA='CA'
            CO='CO'
            CT='CT'
            DE='DE'
            DC='DC'
            FL='FL'
            GA='GA'
            HI='HI'
            ID='ID'
            IL='IL'
            IN='IN'
            IA='IA'
            KS='KS'
            KY='KY'
            LA='LA'
            ME='ME'
            MT='MT'
            NE='NE'
            NV='NV'
            NH='NH'
            NJ='NJ'
            NM='NM'
            NY='NY'
            NC='NC'
            ND='ND'
            OH='OH'
            OK='OK'
            OR='OR'
            MD='MD'
            MA='MA'
            MI='MI'
            MN='MN'
            MS='MS'
            MO='MO'
            PA='PA'
            RI='RI'
            SC='SC'
            SD='SD'
            TN='TN'
            TX='TX'
            UT='UT'
            VT='VT'
            VA='VA'
            WA='WA'
            WV='WV'
            WI='WI'
            WY='WY'
class genres(Enum):
    ALTERNATIVE='Alternative'
    BLUES='Blues'
    CLASSICAL='Classical'
    COUNTRY='Country'
    ELECTRONIC='Electronic'
    FOLK='Folk'
    FUNK='Funk'
    HIP_HOP='Hip-Hop'
    HEAVY_METAL='Heavy Metal'
    INSTRUMENTAL='Instrumental'
    JAZZ='Jazz'
    MUSICAL_THEATRE='Musical Theatre'
    POP='Pop'
    PUNK='Punk'
    R_B='R&B'
    REGGAE='Reggae'
    ROCK_N_ROLL='Rock n Roll'
    SOUL='Soul'
    OTHER='Other'
def is_valid_phone(Form, field):
    phone = field.data 
    regex=re.compile(r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    if not regex.match(phone):
        raise ValidationError("Invalid phone number format. Please use XXX-XXX-XXXX or similar.")

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(state.name,state.value) for state in state])
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
            Regexp(r'^\d{10}$', message="Phone number must be exactly 10 digits."),
            is_valid_phone 
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[(genres.name,genres.value) for genres in genres])
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(),URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(state.name,state.value) for state in state])
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
            Regexp(r'^\d{10}$', message="Phone number must be exactly 10 digits."),
            is_valid_phone 
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[(genres.name,genres.value) for genres in genres])
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(),URL()]
    )
    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

