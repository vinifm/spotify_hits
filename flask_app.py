from flask import Flask, jsonify, url_for
from flask import request
import sqlite3
import os

def execute_query(query):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

app = Flask(__name__)

# Lista as urls disponíveis
# ex.: http://127.0.0.1:5000/
@app.route("/")
def index():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and not rule.endpoint.startswith('static'):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    return '\n'.join([f'<div><a href="{url}">{endpoint}</a></div>' for url, endpoint in links])

# Retorna todas os países no banco de dados
# ex.: http://127.0.0.1:5000/all_playlists
@app.route("/all_playlists",methods = ['GET'])
def all_playlists():
    return jsonify(execute_query("SELECT DISTINCT playlist_country FROM top_songs"))

# Retorna todas as músicas de um país
# ex.: http://127.0.0.1:5000/playlist?country=Brazil
@app.route("/playlist",methods = ['GET'])
def country():
    country = request.args.get('country')
    return jsonify(execute_query(f"SELECT * FROM top_songs WHERE playlist_country='{country}'"))

# Retorna as músicas mais populares
# ex.: http://127.0.0.1:5000/popular
@app.route("/popular",methods = ['GET'])
def popular():
    return jsonify(execute_query(f"SELECT * FROM top_songs ORDER BY popularity DESC"))

# Retorna as músicas menos populares
# ex.: http://127.0.0.1:5000/unpopular
@app.route("/unpopular",methods = ['GET'])
def unpopular():
    return jsonify(execute_query(f"SELECT * FROM top_songs ORDER BY popularity ASC"))

# Retorna as músicas mais antigas
# ex.: http://127.0.0.1:5000/old_songs
@app.route("/old_songs",methods = ['GET'])
def old_songs():
    return jsonify(execute_query(f"SELECT * FROM top_songs ORDER BY release_date ASC"))

# Retorna as músicas mais recentes
# ex.: http://127.0.0.1:5000/new_songs
@app.route("/new_songs",methods = ['GET'])
def new_songs():
    return jsonify(execute_query(f"SELECT * FROM top_songs ORDER BY release_date DESC"))

# Retorna os artistas que mais aparecem
# ex.: http://127.0.0.1:5000/frequent_artists
@app.route("/frequent_artists",methods = ['GET'])
def frequent_artists():
    return jsonify(execute_query(f"SELECT artist_name, COUNT(artist_name) AS frequency \
                                FROM top_songs \
                                GROUP BY artist_name \
                                HAVING frequency > 1 \
                                ORDER BY frequency DESC"))

if __name__=="__main__":
    app.run(
        port=5000,
        debug=True)
