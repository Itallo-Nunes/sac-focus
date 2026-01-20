from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Cliente') # Papéis: Cliente, Atendente
    
    # Relações que serão "anonimizadas" na exclusão
    tickets = db.relationship('Ticket', backref='requester', lazy=True, foreign_keys='Ticket.user_id')
    comments = db.relationship('Comment', backref='author', lazy=True, foreign_keys='Comment.user_id')
    evaluations = db.relationship('Evaluation', backref='evaluator', lazy=True, foreign_keys='Evaluation.user_id')

    @property
    def is_attendant(self):
        return self.role == 'Atendente'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Aberto') # Aberto, Em andamento, Resolvido, Fechado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    evaluation = db.relationship('Evaluation', backref='ticket', uselist=False, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='ticket_comment', lazy=True, cascade="all, delete-orphan")

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # Nota de 1 a 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # CORRIGIDO: Adicionado nullable=True para permitir anonimização
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
