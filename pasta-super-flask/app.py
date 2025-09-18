from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'  # Definir uma chave secreta para gerenciar a sessão

# Usuário fictício para login
users = {
    'usuario@exemplo.com': generate_password_hash('senha123', method='pbkdf2:sha256')
}

@app.route('/')
def index():
    return redirect(url_for('login'))  # Redireciona para o login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificando se o e-mail existe e a senha está correta
        if email in users and check_password_hash(users[email], senha):
            session['email'] = email  # Armazenando o e-mail do usuário na sessão
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Email ou senha inválidos.')

    return render_template('login.html')

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    return render_template('home.html', nome=email.split('@')[0])  # Exibindo o nome antes do "@" no email

@app.route('/logout')
def logout():
    session.pop('email', None)  # Remover o usuário da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
