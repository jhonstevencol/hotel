from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/hotelcoutyardDB.db"
db = SQLAlchemy(app)

class Habitacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('habitacion.idhotel.id'))
    piso = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    descripcion = db.Column(db.String)
    estado = db.Column(db.String)
    numero = db.Column(db.Integer)
    capacidad = db.Column(db.Integer)
    id_tarjeta_llave = db.Column(db.Integer)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    condado = db.Column(db.String, nullable=False)
    township = db.Column(db.String, nullable=False)
    estrellas = db.Column(db.String, nullable=False)
    pisos = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    codigopostal = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer)

class Reserva(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fechaRegistro=db.Column(db.DateTime, default=datetime.datetime.now())
    fechaInicio=db.Column(db.DateTime, default=datetime.datetime.now())
    cantidadDias=db.Column(db.Integer)
    usuario_id=db.Column(db.Integer)
    habitacion_id=db.Column(db.Integer, ForeignKey('habitacion.id'))
    habitacion = relationship(Habitacion, backref=backref('reserva', uselist=True))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    loginUserName = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fecharegistro = db.Column(db.DateTime, default=datetime.datetime.now())
    loginstatus = db.Column(db.Integer)
    lastaccess = db.Column(db.DateTime, default=datetime.datetime.now())
    role_id = db.Column(db.Integer)

    def verif_clave(self, password):
        return checkph(self.password, password)

@app.route("/index", methods=["GET"])
@app.route('/')
def home():    
    return render_template('index.html')

@app.route("/acerca/")
def acerca():
    return render_template("acerca.html", methods=["GET"])

@app.route("/contacto/")
def contacto():
    return render_template("contacto.html", methods=["GET"])

@app.route("/servicios/")
def servicios():
    return render_template("servicios.html", methods=["GET"])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        if not request.form['name'] or not request.form['lastname'] or not request.form['username'] or not request.form['password']:
            flash('Hay campos vacios!!', 'error')
            return redirect(url_for('register'))
        else:
            user = Usuario(name=request.form['name'], lastname=request.form['lastname'], loginUserName=request.form['username'], password=genph(request.form['password']), loginstatus=0 , role_id=3)
            db.session.add(user) 
            db.session.commit()
            session["username"] = user.loginUserName
            session["role"] = user.role_id
            session["usuario_id"] = user.id
            return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(loginUserName=username).first()
        if user is not None and user.verif_clave(password):
            #user.loginstatus = 1
            db.session.commit()
            session["username"] = username
            session["role"] = user.role_id
            session["usuario_id"] = user.id
            return render_template('index.html')
        else:
            flash('Las credenciales no existen, verifique', 'error')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():    
    session.clear()
    return render_template('index.html')

#admin
@app.route('/admin')
def createroom():
    hoteles = Hotel.query.all()
    return render_template('createroom.html', hoteles=hoteles)

@app.route('/rooms')
def getrooms():
    rooms = Habitacion.query.filter_by(estado='disponible').all()
    # rooms = Habitacion.query.join(Hotel, Habitacion.hotel_id == Hotel.id).all()
    return render_template('rooms.html', rooms=rooms)

@app.route('/create-room', methods=['POST'])
def saveroom():
    if not request.form['hotel_id'] or not request.form['piso'] or not request.form['numero'] or not request.form['capacidad'] or not request.form['precio'] or not request.form['descripcion'] or not request.form['estado'] or not request.form['id_tarjeta_llave']:
        flash('Hay campos vacios!!', 'error')
        return redirect(url_for('createroom'))
    else:
        room = Habitacion(hotel_id=request.form['hotel_id'], piso=request.form['piso'], numero=request.form['numero'], capacidad=request.form['capacidad'], precio=request.form['precio'], descripcion=request.form['descripcion'], estado=request.form['estado'], id_tarjeta_llave=request.form['id_tarjeta_llave'] )
        db.session.add(room) 
        db.session.commit()
        flash('Room save success!!', 'success')
        return redirect(url_for('createroom'))

@app.route('/edit-room')
def editroom():
    rooms = Habitacion.query.all()
    return render_template('editroom.html', rooms=rooms)

@app.route('/find-hotel/<id>')
def findhotel(id):
    hotel = Hotel.query.get(id)
    
    return jsonify(
        pisos=hotel.pisos
    )
@app.route('/find-room/<id>')
def findroom(id):
    room = Habitacion.query.get(id)
    return jsonify(
        id=room.id,
        piso=room.piso,
        precio=room.precio,
        estado=room.estado,
        descripcion=room.descripcion,
        numero=room.numero,
        capacidad=room.capacidad,
        id_tarjeta_llave=room.id_tarjeta_llave
    )

@app.route('/update-room', methods=['POST'])
def updateroom():
    room = Habitacion.query.get(int(request.form['id']))
    room.piso = request.form['piso']
    room.numero = request.form['numero']
    room.capacidad = request.form['capacidad']
    room.precio = request.form['precio']
    room.descripcion = request.form['descripcion']
    room.estado = request.form['estado']
    room.id_tarjeta_llave = request.form['id_tarjeta_llave']
    db.session.add(room) 
    db.session.commit()

    flash('Room update success!!', 'success')
    return redirect(url_for('editroom'))

@app.route('/delete-rooms')
def deleterooms():
    rooms = Habitacion.query.all()
    return render_template('deleteroom.html', rooms=rooms)

@app.route('/delete-room', methods=['POST'])
def deleteroom():
    room = Habitacion.query.get(request.form['room_id'])
    db.session.delete(room)
    db.session.commit()
    flash('Room delete success!!', 'success')
    return redirect(url_for('deleterooms'))

@app.route('/reserve', methods=['POST'])
def reservar():
    if not request.form['fecha'] or not request.form['dias']:
        flash('Hay campos vacios!!', 'error')
        return redirect(url_for('getrooms'))
    else:
        reserve = Reserva(cantidadDias=request.form['dias'], usuario_id=session['usuario_id'], habitacion_id=request.form['habitacion_id'])
        db.session.add(reserve) 
        habitacion = Habitacion.query.get(reserve.habitacion_id)
        habitacion.estado = 'ocupada'
        db.session.add(habitacion) 
        db.session.commit()
        flash('Reserve save success!!', 'success')
        return redirect(url_for('getrooms'))

@app.route('/reserves')
def reserves():
    # rooms = Habitacion.query.join(Hotel, Habitacion.hotel_id == Hotel.id).all()
    reserves = Reserva.query.filter_by(usuario_id=session['usuario_id']).all()
    # reserves = Reserva.query.join(Habitacion, Reserva.habitacion_id == Habitacion.id).all()
    
    return render_template('reserves.html', reserves=reserves)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)