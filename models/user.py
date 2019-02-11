from db import db


class UserModel(db.Model):
    __tablename__ = 'USERS'
    id_user = db.Column(db.Integer, primary_key=True)x
    password = db.Column(db.String(255), default='')
    email = db.Column(db.String(255), unique=True, default='')
    profile_img_url = db.Column(db.String(500), default='')
    create_timestamp = db.Column(
        TIMESTAMP, default=datetime.utcnow().replace(microsecond=0))
    # TODO: User tier and classification
