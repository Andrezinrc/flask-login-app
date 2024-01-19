from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class FormLogin(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class FormCadastro(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    csenha = PasswordField('csenha', validators=[DataRequired()])
