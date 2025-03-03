from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète_ici'  # À remplacer par une vraie clé secrète
csrf = CSRFProtect(app)

class InscriptionForm(FlaskForm):
    nom_complet = StringField('Nom complet', validators=[DataRequired(message='Le nom complet est obligatoire')])
    ville = StringField('Ville', validators=[DataRequired(message='La ville est obligatoire')])
    email = StringField('Email', validators=[DataRequired(message='L\'email est obligatoire'), 
                                           Email(message='Format d\'email invalide')])
    submit = SubmitField('Enregistrer')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    form = InscriptionForm()
    
    if form.validate_on_submit():
        # Stocker les données dans la session
        session['inscription_data'] = {
            'nom_complet': form.nom_complet.data,
            'ville': form.ville.data,
            'email': form.email.data
        }
        return redirect(url_for('confirmation'))
    
    return render_template('formulaire.html', form=form)

@app.route('/confirmation')
def confirmation():
    # Récupérer les données depuis la session
    inscription_data = session.get('inscription_data', None)
    
    if not inscription_data:
        flash("Aucune donnée d'inscription trouvée, veuillez remplir le formulaire.", 'warning')
        return redirect(url_for('formulaire'))
    
    return render_template('confirmation.html', data=inscription_data)

if __name__ == '__main__':
    app.run(debug=True)