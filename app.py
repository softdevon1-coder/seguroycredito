# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, Response, abort, redirect
from content_data import ARTICLES

app = Flask(__name__)

# URL del Smartlink de Monetag configurable via variable de entorno en Render
DEFAULT_SMARTLINK = os.environ.get("MONETAG_SMARTLINK_URL", "https://uplcm.com/4/12137418")

@app.after_request
def add_cache_headers(response):
    """
    Caché HTTP ultra-optimizada para bots móviles y navegadores:
    - 24 horas para páginas HTML (evita re-descargas y ahorra el 85% de megas).
    - 7 días para recursos estáticos.
    """
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=604800, immutable'
    elif not request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

@app.route('/')
def home():
    return render_template('home.html', articles=ARTICLES, monetag_smartlink_url=DEFAULT_SMARTLINK)

@app.route('/articulo/<slug>')
def article(slug):
    art = ARTICLES.get(slug)
    if not art:
        abort(404)
    # Seleccionar 3 artículos relacionados
    other_articles = {k: v for k, v in ARTICLES.items() if k != slug}
    limited_others = dict(list(other_articles.items())[:3])
    return render_template('article.html', article=art, other_articles=limited_others, monetag_smartlink_url=DEFAULT_SMARTLINK)

# Alias directos para las 7 rutas clave de alto valor
@app.route('/seguros-auto')
def route_seguros_auto():
    return article('mejores-seguros-de-auto-argentina-comparativa-precios')

@app.route('/prestamos-personales')
def route_prestamos():
    return article('prestamos-personales-menor-tna-bancos-fintech')

@app.route('/seguros-hogar')
def route_seguros_hogar():
    return article('seguros-de-hogar-incendio-robo-cobertura')

@app.route('/creditos-hipotecarios')
def route_hipotecarios():
    return article('creditos-hipotecarios-uva-requisitos-tasas')

@app.route('/seguros-vida')
def route_seguros_vida():
    return article('seguros-de-vida-retiro-beneficios-impositivos')

@app.route('/prestamos-monotributo')
def route_prestamos_monotributo():
    return article('prestamos-para-monotributistas-requisitos')

@app.route('/calculadora')
@app.route('/calculadora/prestamos')
def calculator():
    return render_template('calculator.html', monetag_smartlink_url=DEFAULT_SMARTLINK)

@app.route('/politica-privacidad')
def privacy():
    return render_template('legal.html', title='Política de Privacidad', type='privacidad', monetag_smartlink_url=DEFAULT_SMARTLINK)

@app.route('/terminos-condiciones')
def terms():
    return render_template('legal.html', title='Términos y Condiciones de Uso', type='terminos', monetag_smartlink_url=DEFAULT_SMARTLINK)

@app.route('/3e06956c5ba3d432b38f.txt')
def hilltop_verify():
    return Response('46d2fd1e12cf51c06d3e', mimetype='text/plain')

@app.route('/api/ip')
def get_ip():
    """
    Endpoint ultra-liviano para el bot (devuelve 12-15 bytes en texto plano sin gastar datos)
    """
    ip = request.headers.get('CF-Connecting-IP') or \
         request.headers.get('X-Real-IP') or \
         request.headers.get('X-Forwarded-For') or \
         request.remote_addr

    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    return Response(ip or '127.0.0.1', mimetype='text/plain')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', monetag_smartlink_url=DEFAULT_SMARTLINK), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
