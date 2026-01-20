from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email(message='E-mail inválido.')])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, message='A senha deve ter pelo menos 6 caracteres.')])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='As senhas não correspondem.')])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Alterar Senha')

class TicketForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    priority = SelectField('Prioridade', choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')], validators=[DataRequired()])
    submit = SubmitField('Abrir Chamado')

class CommentForm(FlaskForm):
    text = TextAreaField('Comentário', validators=[DataRequired(message="O campo de comentário não pode estar vazio.")])
    submit_comment = SubmitField('Adicionar Comentário')

class UpdateStatusForm(FlaskForm):
    status = SelectField('Novo Status', 
        choices=[
            ('Aberto', 'Aberto'), 
            ('Em andamento', 'Em andamento'), 
            ('Resolvido', 'Resolvido'), 
            ('Fechado', 'Fechado')
        ],
        validators=[DataRequired()]
    )
    submit_status = SubmitField('Atualizar Status')
