from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import or_
from sqlalchemy import inspect

# New Code 
# from models import sqldb

# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# from sqlalchemy.engine import reflection
# from sqlalchemy import MetaData
# from sqlalchemy import Table
# end new code


queries=[
    {
        'name':'/query_1',
        'query':'Display All Players:'
    },
    {
        'name':'/query_2',
        'query':'Display Players in PSG:'
    },
    {
        'name':'/query_3',
        'query':'Display All Matches with PSG:'
    },
    {
        'name':'/query_4',
        'query':'List of players and their stats'
    }
]


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CACHE_TYPE'] = "null"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/four2three1'
db = SQLAlchemy(app)


# player = db.Table('player',db.metadata,autoload = True, autoload_with = db.engine)
# stats = db.Table('stats',db.metadata,autoload = True, autoload_with = db.engine)
# agent = db.Table('agent',db.metadata,autoload = True, autoload_with = db.engine)
# national_team = db.Table('national_team',db.metadata,autoload = True, autoload_with = db.engine)
# manager = db.Table('manager',db.metadata,autoload = True, autoload_with = db.engine)
# clubs = db.Table('clubs',db.metadata,autoload = True, autoload_with = db.engine)
# match = db.Table('match',db.metadata,autoload = True, autoload_with = db.engine)
# journalist = db.Table('journalist',db.metadata,autoload = True, autoload_with = db.engine)
# journalist = db.Table('journalist',db.metadata,autoload = True, autoload_with = db.engine)
# articles = db.Table('articles',db.metadata,autoload = True, autoload_with = db.engine)
# player_transfer = db.Table('player_transfer',db.metadata,autoload = True, autoload_with = db.engine)

Base = automap_base()
Base.prepare(db.engine, reflect = True)
player = Base.classes.player
stats = Base.classes.stats
match = Base.classes.match
our_user = Base.classes.our_user


global_admin = False
global_login = False


# INDEX 
@app.route('/')
def index():
    if global_login == False:
        return redirect(url_for('login'))
        # return render_template('login.html')
    return render_template('home.html', admin = global_admin, login = global_login)



# QUERY 
@app.route('/query')
def query():
    # queries = {"query_1":"Display All Players:",
    #             "query_2":"Display Players in PSG:",
    #             "query_3":"Display All Matches with PSG:"}
    return render_template('query.html', title="Query", queries = queries, admin = global_admin, login = global_login)


@app.route('/query_1')
def query_1():
    players = db.session.query(player).all()
    # headers = [ 'Player Name' , 'Position', 'National Team', 'Club Name', 'Salary($)', 'Term', 'Join Date']
    inspection = inspect(player)
    headers = [attr.key for attr in inspection.mapper.column_attrs]
    query_1 = [ player for player in players ]
    return render_template('query_submit.html', title="Query", headers = headers, players = query_1, admin = global_admin, login = global_login)


@app.route('/query_2')
def query_2():
    players = db.session.query(player).filter(player.club_name == 'PSG')
    # headers = [ 'Player Name' , 'Position', 'National Team', 'Club Name', 'Salary($)', 'Term', 'Join Date']
    inspection = inspect(player)
    headers = [attr.key for attr in inspection.mapper.column_attrs]
    query_2 = [ player for player in players ]
    return render_template('query_submit.html', title="Query", headers = headers, players = query_2, admin = global_admin, login = global_login)


@app.route('/query_3')
def query_3():
    matches = db.session.query(match).filter(or_(match.home_team == 'PSG', match.away_team == 'PSG'))
    # headers = [ 'Player Name' , 'Position', 'National Team', 'Club Name', 'Salary($)', 'Term', 'Join Date']
    query_3 = [ game for game in matches ]
    # print(query_3[0], type(query_3))
    inspection = inspect(match)
    headers = [attr.key for attr in inspection.mapper.column_attrs]
    # print(attributes)
    # for query in query_3:
    #     for header in headers:
    #         print(query[0])
    return render_template('query3_submit.html', title="Query", headers = headers, players = query_3, len=len(query_3), admin = global_admin, login = global_login)


@app.route('/query_4')
def query_4():
    # players = db.session.query(stats).join(player).filter(player.player_id == stats.player_id)
    players = db.session.query(player,stats).filter(player.player_id == stats.player_id)
    headers = [ 'Player Name' , 'Club Name', 'Goals', 'Assists', 'Tackles']
    query_4 = [ player for player in players ]
    # query_4 = db.execute('SELECT * FROM stats')
    # for query in query_4:
    #     print(query)
    return render_template('query4_submit.html', title="Query", headers = headers, players = query_4, len=len(query_4), admin = global_admin, login = global_login)



@app.route('/insert')
def insert():
    return render_template('insert.html', title="Insert", admin = global_admin)

@app.route('/insert_player', methods=['GET', 'POST'])
def insert_record():
    new_player = player(player_id = request.form.get('player_id'),
    p_name=request.form.get('p_name'),
    position = request.form.get('position'),
    agent_id = request.form.get('agent_id'),
    nat_team = request.form.get('nat_team'),
    club_name = request.form.get('club_name'),
    salary = request.form.get('salary'),
    term = request.form.get('term'),
    join_date = request.form.get('join_date'))
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('insert'))



@app.route('/update')
def update():
    return render_template('update.html', title="Update",admin = global_admin)

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    # updated_rows = our_user.query.filter_by(username=request.form.get('username').update(dict(username = request.form.get('new_username'))))
    db.session.query(our_user).filter(our_user.username == request.form.get('username')).update(dict(username = request.form.get('new_username')))
    db.session.commit()
    return redirect(url_for('update'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_validate', methods = ['GET', 'POST'])
def login_validate():
    global global_login
    global global_admin
    if request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
        print('admin found')
        global_admin = True
        global_login = True
        return redirect(url_for('index'))
    if request.form.get('username') == 'user' and request.form.get('password') == 'user':
        print('user found')
        global_login = True
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    global global_login
    global global_admin
    global_login = False
    global_admin = False
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True) 





# class Player(db.Model):
#     player_id = db.Column(db.Integer, primary = True)
#     p_name = db.Column(db.String(20), nullable = False)
#     position = db.Column(db.String(20), nullable = False)
#     agent_id = db.Column(db.Integer, unique = True)
#     nat_team = db.Column(db.String(20))
#     club_name = db.Column(db.String(20))
#     salary = db.Column(db.Integer, nullable = False)
#     term = db.Column(db.Integer, nullable = False)
#     join_date = db.Column(db.Date)

#     def __init__(self, player_id, position, agent_id, nat_team, club_name, salary, term, join_date):
#         self.player_id = player_id
#         self.position = position
#         self.agent_id = agent_id
#         self.nat_team = nat_team
#         self.club_name = club_name
#         self.salary = salary
#         self.term = term
#         self.join_date = join_date
    
#     def __repr__(self):
#         return '<Player %r>' % self.player_id

# class Player(db.Model):
#     player_id = db.Column(db.Integer, primary = True)
#     p_name = db.Column(db.String(20), nullable = False)
#     position = db.Column(db.String(20), nullable = False)
#     agent_id = db.Column(db.Integer, unique = True)
#     nat_team = db.Column(db.String(20))
#     club_name = db.Column(db.String(20))
#     salary = db.Column(db.Integer, nullable = False)
#     term = db.Column(db.Integer, nullable = False)
#     join_date = db.Column(db.Date)

#     def __init__(self, player_id, position, agent_id, nat_team, club_name, salary, term, join_date):
#         self.player_id = player_id
#         self.position = position
#         self.agent_id = agent_id
#         self.nat_team = nat_team
#         self.club_name = club_name
#         self.salary = salary
#         self.term = term
#         self.join_date = join_date
    
#     def __repr__(self):
#         return '<Player %r>' % self.player_idmatch.home_team == 'PSG' or match.away_team == 'PSG'