from flask import Blueprint, render_template, request, jsonify
from .models import Meal, Tag
from . import db
import json
import random

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    meals = Meal.query.all()
    return render_template('home.html', meals=meals)


@views.route('/week', methods=['GET', 'POST'])
def week():
    if request.method == 'POST':
        dej = []
        din = []
        nbdej = int(request.form.get('nbdej'))
        nbdin = int(request.form.get('nbdin'))
        meals = Meal.query.all()

        for meal in meals:
            for tag in meal.tags:
                if tag.value == 'déjeuner':
                    dej.append(meal)
                if tag.value == 'diner':
                    din.append(meal)

        dej_list = random.sample(dej, nbdej)
        din_list = random.sample(din, nbdin)

        return render_template('week.html', dej_list=dej_list, din_list=din_list)

    return render_template('week.html')


@views.route('/delete-meal', methods=['POST'])
def delete_meal():
    meal = json.loads(request.data)
    mealId = meal['mealId']
    meal = Meal.query.get(mealId)
    if meal:
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
