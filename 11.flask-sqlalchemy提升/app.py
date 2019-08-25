from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    # addresses = db.relationship('Address', backref='user_info')


class Address(db.Model):
    __tablename__ = 't_address'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))

    user_info = db.relationship('User', backref='addresses')

    def __repr__(self):
        return '<%s, %s>' % (self.user_id, self.detail)


@app.route('/')
def index():
    db.drop_all()
    db.create_all()
    user1 = User(name='zs')
    db.session.add(user1)
    db.session.flush()
    db.session.rollback()
    addr1 = Address(detail='中关村3号', user_id=user1.id)
    addr2 = Address(detail='中关村2号', user_id=user1.id)
    db.session.add_all([addr1, addr2])
    db.session.commit()

    user_obj = User.query.filter_by(name='zs').first()
    print(user_obj.addresses)
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
