from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

DB.init_app(app)

def create_app():
        
    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title="Home", users=users)

    @app.route('/reset')
    def reset():
        #reseting the batabase
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')

    @app.route('/populate')
    def populate():
        #create some fake users in the DB
        add_or_update_user('austen')
        add_or_update_user('nasa')
        add_or_update_user('ryanallred')
      

        DB.session.commit()

        return render_template('base.html', title='Populate Database')

    @app.route('/update')
    def update():
        '''get list of usernames of all users'''
        users = User.query.all()
        # usernames = []
        # for user in users:
        #     usernames.append(user.username)
        # for username in usernames:
        #     add_or_update_user(username)
        for username in [user.username for user in users]:
            add_or_update_user(username)

    return render_template('base.html', title='Users Updated') 

    return app
