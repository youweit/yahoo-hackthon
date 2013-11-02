from app import db
import re

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.String(40), primary_key = True)
    count = db.Column(db.Integer)
    prefer_time = db.Column(db.String(14))
    longtitude = db.Column(db.String(15))
    latitude  = db.Column(db.String(15))
    ordered = db.Column(db.Integer, default=0)

    followed = db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = db.backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')
   
    def __repr__(self):
        return '<User %r>' % (self.name)


    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
            
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
     
    @property
    def serialize(self):
       return {
           'name' : self.name,
           'uid' : self.uid,
           'prefer_time' : self.prefer_time
       }

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sun = db.Column(db.String(14))
    mon = db.Column(db.String(14))
    tue = db.Column(db.String(14))
    wed = db.Column(db.String(14))
    thu = db.Column(db.String(14))
    fri = db.Column(db.String(14))
    sat = db.Column(db.String(14))


# class Company(db.Model):
    
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(120), unique = True)
#     phone = db.Column(db.String(20), unique = True)
#     name = db.Column(db.String(120), unique = True)
#     description = db.Column(db.String(140))
    
    
#     def __repr__(self):
#         return '<Company %r>' % (self.name)

#     @staticmethod
#     def make_valid_name(name):
#         return re.sub('[^a-zA-Z0-9_\.]', '', name)
    
#     @property
#     def serialize(self):
#        return {
#            'id' : self.id,
#            'name' : self.name,
#            'email' : self.email,
#            'phone' : self.phone,
#            'description' : self.description        
#        }
    
#     @property
#     def serialize_many2many(self):
#        return [ item.serialize for item in self.many2many]


