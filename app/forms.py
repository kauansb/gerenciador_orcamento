from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class CategoryForm(FlaskForm):
    """Formulário para criar/editar categoria."""
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    limite = DecimalField('Limite', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Salvar')
    
    def validate_nome(self, field):
        """Validar que nome não é vazio após strip."""
        if not field.data or not field.data.strip():
            raise ValidationError('Nome não pode ser vazio.')


class TransactionForm(FlaskForm):
    """Formulário para criar/editar transação."""
    descricao = StringField('Descrição', validators=[DataRequired(), Length(max=255)])
    valor = DecimalField('Valor', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')


class DeleteForm(FlaskForm):
    """Formulário para deletar (apenas token CSRF)."""
    submit = SubmitField('Deletar')
