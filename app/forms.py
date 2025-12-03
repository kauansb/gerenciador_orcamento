from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from app.models import Categoria


class CategoryForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    limite = DecimalField('Limite', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Salvar')

    def __init__(self, original_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_id = original_id

    def validate_nome(self, field):
        nome = field.data.strip()
        existing = Categoria.query.filter_by(nome=nome).first()
        if existing and (self.original_id is None or existing.id != self.original_id):
            raise ValidationError('Categoria com esse nome já existe.')


class TransactionForm(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired(), Length(max=255)])
    valor = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

    # choices must be set by the route before rendering/validation
