from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Meal, Tag
from . import db
import json
import random

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        meal = request.form.get('meal')
        tags = request.form.get('tags').split()

        if len(meal) < 1:
            flash('Meal is too short!', category='error')
        else:
            new_meal = Meal(data=meal, user_id=current_user.id)
            if len(tags) < 1:
                flash('At least one tag is needed', category='error')
            else:
                for tag in tags:
                    new_meal.tags.append(Tag(value=tag))
            db.session.add(new_meal)
            db.session.commit()
            flash('Meal added', category='success')

    return render_template('home.html', user=current_user)


@views.route('/week', methods=['GET', 'POST'])
@login_required
def week():
    if request.method == 'POST':
        dej = []
        din = []
        nbdej = int(request.form.get('nbdej'))
        nbdin = int(request.form.get('nbdin'))
        meals = Meal.query.all()

        for meal in meals:
            for tag in meal.tags:
                if tag.value == 'dejeuner':
                    dej.append(meal)
                if tag.value == 'diner':
                    din.append(meal)

        dej_list = random.sample(dej, nbdej)
        din_list = random.sample(din, nbdin)

        return render_template('week.html', user=current_user, dej_list=dej_list, din_list=din_list)

    return render_template('week.html', user=current_user)


@views.route('/delete-meal', methods=['POST'])
def delete_meal():
    meal = json.loads(request.data)
    mealId = meal['mealId']
    meal = Meal.query.get(mealId)
    if meal:
        if meal.user_id == current_user.id:
            db.session.delete(meal)
            db.session.commit()

    return jsonify({})

@views.route('/delete-tag', methods=['POST'])
def delete_tag():
    tag = json.loads(request.data)
    tagId = tag['tagId']
    tag = Tag.query.get(tagId)
    if tag:
        db.session.delete(tag)
        db.session.commit()

    return jsonify({})
