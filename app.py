import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)

# ... (votre code existant)

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # Récupérer le fichier JSON téléchargé
        uploaded_file = request.files['file']
        json_data = uploaded_file.read()

        # Vérifier l'intégrité du fichier JSON
        success, data = check_json_integrity(json_data)

        # Traiter les résultats
        if success:
            print('Data from JSON file:', data) 
            display_run_info(data)
            names_with_tests, names_without_tests = extract_names(data)
            print('Names with tests:', names_with_tests)
            print('Names without tests:', names_without_tests)

            # Stocker les noms avec tests dans la session Flask
            session['names_with_tests'] = names_with_tests

            return render_template('results.html', names_with_tests_output=names_with_tests, names_without_tests_output=names_without_tests)
        else:
            return jsonify({'error': 'Le fichier JSON ne correspond pas à la structure attendue'})

    except Exception as e:
        return jsonify({'error': f'Une erreur est survenue : {str(e)}'})

@app.route('/get_names_with_tests', methods=['GET'])
def get_names_with_tests():
    # Récupérer les noms avec tests depuis la session Flask
    names_with_tests = session.get('names_with_tests', [])

    # Retourner les noms avec tests au format JSON
    return jsonify({'names_with_tests': names_with_tests})

if __name__ == '__main__':
    app.run(debug=True)
