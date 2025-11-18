import requests
from deep_translator import GoogleTranslator
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-final-v3-corrigida'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#MODELOS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    animes = db.relationship('Anime', backref='owner', lazy=True)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    episodios = db.Column(db.Integer)
    capa = db.Column(db.String(500))
    sinopse = db.Column(db.Text)
    assistido = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


SUGESTOES = [
    {'titulo': 'Solo Leveling', 'genero': 'Ação', 'episodios': 12, 'img': 'https://4kwallpapers.com/images/walls/thumbs_2t/20374.png', 'sinopse': 'Sung Jin-Woo, o caçador mais fraco, desperta um poder infinito.'},
    {'titulo': 'Jujutsu Kaisen', 'genero': 'Shonen', 'episodios': 47, 'img': 'https://cdn.myanimelist.net/images/anime/1171/109222.jpg', 'sinopse': 'Maldições reais nascem das emoções negativas dos humanos.'},
    {'titulo': 'Kimetsu no Yaiba', 'genero': 'Ação', 'episodios': 55, 'img': 'https://cdn.myanimelist.net/images/anime/1286/99889.jpg', 'sinopse': 'Um jovem vende carvão para sustentar sua família até que o horror acontece.'},
    {'titulo': 'Sousou no Frieren', 'genero': 'Fantasia', 'episodios': 28, 'img': 'https://img.goodfon.com/wallpaper/big/4/8a/sousou-no-frieren-frieren-himmel-heiter-eisen.webp', 'sinopse': 'A jornada da elfa Frieren para entender os humanos após o fim da aventura.'}
]


DESTAQUES = [
    {
        'titulo': 'ONE PIECE: GEAR 5',
        'desc': 'Acompanhe o ápice da libertação de Luffy!',
        'img': 'https://cdn.observatoriodocinema.com.br/2024/03/luffy-gear-5-1024x571.jpg',
        'link': 'https://www.crunchyroll.com/pt-br/series/GRMG8ZQZR/one-piece'
    },
    {
        'titulo': 'JUJUTSU KAISEN: SHIBUYA',
        'desc': 'O incidente que mudou o mundo jujutsu para sempre.',
        'img': 'https://wallpapercave.com/wp/wp13223654.jpg',
        'link': 'https://www.crunchyroll.com/pt-br/series/GRDV0019R/jujutsu-kaisen'
    },
    {
        'titulo': 'BLEACH: TYBW',
        'desc': 'A guerra sangrenta de mil anos começou.',
        'img': 'https://images5.alphacoders.com/131/1319289.jpeg',
        'link': 'https://www.disneyplus.com/pt-br/series/bleach-thousand-year-blood-war/44J9a2312a4h' 
    }
]

#FUNÇÃO DE BUSCA
def buscar_dados_anime_simples(nome_anime):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={nome_anime}&limit=1"
        resposta = requests.get(url, timeout=5)
        json_data = resposta.json()
        
        anime_data = json_data.get('data', [])
        if not anime_data:
            return None
            
        data = anime_data[0]
        
        eps = data.get('episodes')
        if eps is None or eps == 1:
            eps = 0
            
        genero_api = "Anime"
        if data.get('genres') and len(data['genres']) > 0:
            genero_api = data['genres'][0]['name']

        sinopse_en = data.get('synopsis')
        sinopse_final = "Sinopse indisponível."

        if sinopse_en:
            try:
                sinopse_final = GoogleTranslator(source='auto', target='pt').translate(sinopse_en)
            except:
                sinopse_final = sinopse_en
            
        return {
            'titulo': data.get('title'),
            'capa': data['images']['jpg']['large_image_url'],
            'sinopse': sinopse_final,
            'episodios': eps,
            'genero': genero_api
        }

    except Exception as e:
        print(f"Erro na Busca: {e}")
        return None 

#ROTAS
@app.route('/')
@login_required
def index():
    termo_busca = request.form.get('busca')
    
    if termo_busca:
        meus_animes = Anime.query.filter(
            Anime.titulo.contains(termo_busca), 
            Anime.user_id == current_user.id
        ).all()
    else:
        meus_animes = Anime.query.filter_by(user_id=current_user.id).all()
    
    return render_template('index.html', animes=meus_animes, sugestoes=SUGESTOES, destaques=DESTAQUES, nome=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Dados incorretos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe.', 'warning')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add_anime():
    titulo_busca = request.form.get('titulo')
    dados_anime = buscar_dados_anime_simples(titulo_busca)
    
    if not dados_anime:
        flash(f'Anime "{titulo_busca}" não encontrado.', 'warning')
        return redirect(url_for('index'))
        
    existing_anime = Anime.query.filter_by(titulo=dados_anime['titulo'], user_id=current_user.id).first()
    if existing_anime:
        flash(f'Você já tem "{dados_anime["titulo"]}" na lista.', 'info')
        return redirect(url_for('index'))

    novo_anime = Anime(
        titulo=dados_anime['titulo'], 
        genero=dados_anime['genero'], 
        episodios=dados_anime['episodios'], 
        capa=dados_anime['capa'], 
        sinopse=dados_anime['sinopse'],
        owner=current_user
    )
    db.session.add(novo_anime)
    db.session.commit()
    flash(f'"{dados_anime["titulo"]}" adicionado!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_anime(id):
    anime = Anime.query.get_or_404(id)
    if anime.user_id != current_user.id:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        anime.titulo = request.form.get('titulo')
        anime.genero = request.form.get('genero')
        eps_form = request.form.get('episodios')
        if eps_form:
            anime.episodios = int(eps_form)
        
        if request.form.get('atualizar_auto'):
             dados = buscar_dados_anime_simples(anime.titulo)
             if dados:
                anime.capa = dados['capa']
                anime.sinopse = dados['sinopse']
                if dados['episodios'] > 0:
                    anime.episodios = dados['episodios']

        db.session.commit()
        flash('Atualizado!', 'success')
        return redirect(url_for('index'))
        
    return render_template('edit.html', anime=anime)

@app.route('/toggle/<int:id>')
@login_required
def toggle_status(id):
    anime = Anime.query.get_or_404(id)
    if anime.user_id == current_user.id:
        anime.assistido = not anime.assistido
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete_anime(id):
    anime = Anime.query.get_or_404(id)
    if anime.user_id == current_user.id:
        db.session.delete(anime)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)