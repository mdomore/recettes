from . import db

tags_association = db.Table('association', db.Model.metadata,
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(30))
    meals = db.relationship('Meal', secondary=tags_association, back_populates='tags')

    def __repr__(self):
        return self.value


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100000))
    tags = db.relationship('Tag', secondary=tags_association, back_populates='meals')

    def __repr__(self):
        return self.name
