

class Voter(db.Model):
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    id_number = db.Column(db.Integer, nullable=False, primary_key=True)
    province = db.Column(db.String(20), nullable=True)
    voted = db.Column(db.Integer(1), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    vote_time = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.Integer(1), nullable=True)
    email = db.Column(db.String(30), nullable=True)

    def __repr__(self):
    return f'<Student {self.id_number}>'
