from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length
from flask.ext.babel import gettext


class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    phone = TextField('phone', validators = [Length(min = 6, max = 35)])
    email = TextField('Email Address', validators = [Length(min=6, max=35)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        '''if self.nickname.data != Company.make_valid_name(self.nickname.data):
            self.nickname.errors.append('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.')
            return False'''
        
        user = Company.query.filter_by(name = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        
        return True
