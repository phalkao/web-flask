from flask import Blueprint, render_template, jsonify

mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod.route('/')
def index():
    return render_template('dashboard/home.html')


@mod.route('/irc/')
def irc():
    return render_template('dashboard/irc.html')


@mod.route('/badges/')
def badges():
    return render_template('dashboard/badges.html')



@mod.route('/logos/')
def logos():
    return render_template('dashboard/logos.html')