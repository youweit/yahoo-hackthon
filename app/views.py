from app import app, db
from flask import Flask, flash, jsonify, make_response, redirect, url_for, request, abort, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask.ext.httpauth import HTTPBasicAuth
from models import User,Movie,Day
from werkzeug import secure_filename
import json
from random import choice
import os
import datetime
import math
import datetime


@app.route('/api/register', methods = ['POST'])
def create_user():
    if not request.form or not 'name' in request.form:
        abort(400)
        
    u = User(
        name = request.form['name'],
        uid = request.form['uid'],
        timestamp = datetime.datetime.utcnow(),
        longtitude = request.form['longtitude'],
        latitude = request.form['latitude']
    )

    if(User.query.filter_by(uid = request.form['uid']).first() == None):
        db.session.add(u)
        db.session.commit()
        return jsonify( { 'status': 'successful'} ), 200
    else:
        return jsonify( { 'status': 'duplicate'} ), 200
    
@app.route('/api/set_prefer_time', methods = ['POST'])
def set_prefer_time():
    if(User.query.filter_by(uid = request.form['uid']).first() != None):
        u = User.query.filter(User.uid == request.form['uid'])
        u.update({
            'hour': request.form['hour'],
            'weekday': request.form['weekday'],
            'longtitude': request.form['longtitude'],
            'latitude' : request.form['latitude']
        })

        m = Movie.query.filter(Movie.week == request.form['weekday']).first()
        day = Day.query.filter(Day.hour == request.form['hour'],Day.movie_id == m.id).first()

        day.people += 1 #TODO -1

        db.session.commit()

        return jsonify( { 'status': 'successful'} ), 200
    else:
        return jsonify( { 'status': 'user not in database'} ), 200

@app.route('/api/get_buddy', methods = ['POST'])
def get_buddy():
    mUid = request.form['uid']
    u = User.query.filter_by(uid = mUid).first()
    
    if(u != None):
        return random_buddy(u)
    else:
        return jsonify( { 'buddy_uid': 'none'} ), 200

@app.route('/api/get_people', methods = ['GET'])
def get_movie():

    weekday = datetime.datetime.today().weekday()-1
    people_data = []
    density_data = []
    day_max = 0.0
    for i in range(7):

        m = Movie.query.filter(Movie.week == (i + weekday)%7).first()
        days = Day.query.filter(Day.movie_id == m.id).all()
        
        for day in days:
            day_max = max(day_max,day.people)
            data = day.people
            people_data.append(data)
        
        for day in days:
            if(day_max == 0):
                density_data.append(0)
            else:
                multipler = 9.0/day_max
                den = round(day.people * multipler)
                density_data.append(den)



    return jsonify( {'people': people_data,'density':density_data} ), 200

@app.route('/api/check_notitfication', methods = ['POST'])
def check_notitfication():
    u = User.query.filter(User.uid == request.form['uid'])
    follow = followers.query.filter(followers.follower_id == u.id or followers.followed_id == u.id)
    if(follow != None):
        return jsonify( {'people': "test"} ), 200
    else:
        pass

@app.route('/api/populate', methods = ['GET'])
def populate():
    for i in range(7):
        m = Movie(
            week = i
        )
        
        for i in range(0,24,3):
            m.day.append(Day(
                hour = i,
                people = 0
            ))
        db.session.add(m)
        pass
            
    db.session.commit()
    return jsonify( { 'status': 'successful'} ), 200

def random_buddy(mUser):
    user_list = []
    if(mUser.ordered == 0):
        users = User.query.filter(User.ordered == 0,User.id != mUser.id).all()
        for user in users:
            if(distance_on_unit_sphere(float(mUser.latitude), float(mUser.longtitude), float(user.latitude), float(user.longtitude)) < 15 and mUser.weekday == user.weekday and mUser.hour == user.hour):
                user_list.append(user)
                print user.name
        if not user_list:
            print "is empty"
        else:
            luckyguy = choice(user_list)

            mUser.follow(luckyguy)
            luckyguy.follow(mUser)

            mUser.ordered = luckyguy.ordered = 1

            m = Movie.query.filter(Movie.week == mUser.weekday).first()
            print m
            day = Day.query.filter(Day.hour == mUser.hour,Day.movie_id == m.id).first()
            print mUser.hour
            #day.people -= 2

            db.session.flush()
            db.session.commit()

            return jsonify( luckyguy.serialize ), 200
        return jsonify( { 'error': 'nobody' } ), 200
    else:
        return jsonify( { 'error': 'you are ordered' } ), 200

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad Request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify( { 'error': 'Method Not Allowed' } ), 405)

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    return arc*6373
