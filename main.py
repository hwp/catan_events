"""
main.py

Copyright (c) Weipeng He <weipeng.he@idiap.ch>
"""

import random
import secrets

from flask import Flask, render_template, redirect, url_for, session
app = Flask(__name__, static_folder='.')
with open('secret_key', 'rb') as f:
    app.secret_key = f.read()

_EVENT_LIST = [
    'Robber Attack',
    'None',
    'Epidemic',
    'Earthquake',
    'Good Neighbors',
    'Trade Advantage',
    'Tournament',
    'Robber Flees',
    'Conflict',
    'Calm Seas',
    'Neighborly Assistance',
    'Plentiful Year',
]

_EVENT_CHANCE = [
    0,
    16,
    2,
    1,
    1,
    1,
    1,
    2,
    1,
    2,
    2,
    1,
]

_EVENT_CHOICES = [x for e, c in enumerate(_EVENT_CHANCE) for x in [e] * c]


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/roll')
def roll():
    # roll dice
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2

    if 'dice_count' in session:
        dice_count = session['dice_count']
    else:
        dice_count = {str(i): 0 for i in range(2, 13)}
    dice_count[str(dice_sum)] += 1
    session['dice_count'] = dice_count

    dice_count_list = sorted(dice_count.items(), key=lambda x: int(x[0]))

    # sample event
    if dice_sum == 7:
        event = 0
    else:
        event = random.choice(_EVENT_CHOICES)

    if 'event_count' in session:
        event_count = session['event_count']
    else:
        event_count = {str(i): 0 for i in range(len(_EVENT_LIST))}
    event_count[str(event)] += 1
    session['event_count'] = event_count

    event_count_list = sorted(
        (_EVENT_LIST[int(e)], c) for e, c in event_count.items())

    return render_template(
        'roll.html',
        dice1=dice1,
        dice2=dice2,
        dice_sum=dice_sum,
        dice_count=dice_count_list,
        event=_EVENT_LIST[event],
        event_count=event_count_list,
    )


@app.route('/reset')
def reset(name=None):
    if 'dice_count' in session:
        session['dice_count'] = {i: 0 for i in range(2, 13)}
    if 'event_count' in session:
        session['event_count'] = {str(i): 0 for i in range(len(_EVENT_LIST))}
    return redirect(url_for('index'))
