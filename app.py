from flask import Flask, request, send_from_directory
import os
app = Flask(__name__)

# Dossier où les fichiers sont stockés
UPLOAD_FOLDER = '/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
# Point de terminaison pour servir un fichier (GET)
@app.route('/public-key.pem', methods=['GET'])
def serve_public_key():
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'public-key.pem', as_attachment=True)
    except FileNotFoundError:
        return "Fichier public-key.pem non trouvé", 404

# Point de terminaison pour recevoir un fichier (POST)
# Point de terminaison pour recevoir un fichier (PUT)
@app.route('/', methods=['POST'])
def receive_file():
    try:
        filename = request.headers.get('Filename')
        
        if not filename:
            return "Aucun nom de fichier spécifié", 400
        data = request.get_data()  # Récupération fiable des données
        if not data:
            return "Données vides reçues", 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info(f"Taille des données reçues : {len(request.data)} octets")
        with open(filepath, "wb") as f:
            f.write(data)
        
        '''file = request.files['secret']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], ducky_name))'''
        return f"Fichier {filename} reçu avec succès.", 200
    except Exception as e:
        return f"Erreur lors de la réception du fichier : {str(e)}", 500

'''@app.route('/', methods=['POST'])
#def receive_file():
   try:
        
        filename = request.headers.get('Filename')
        
        
        if not filename:
            return "Aucun nom de fichier spécifié", 400

        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, "wb") as f:
            f.write(request.data)
        return f"Fichier {filename} reçu avec succès.", 200
    except Exception as e:
        return f"Erreur lors de la réception du fichier : {str(e)}", 500'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9002)
