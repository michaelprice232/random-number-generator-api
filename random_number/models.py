from random_number import db


# Table to store generated random number data in
class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    max_range = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Number %r>' % self.number
