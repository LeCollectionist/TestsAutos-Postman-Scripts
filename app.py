import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
# Structure du modèle attendu
expected_keys = ["id", "name", "timestamp", "collection_id", "folder_id",
                 "environment_id", "totalPass", "delay", "persist", "status",
                 "startedAt", "totalFail", "results", "count", "totalTime", "collection"]

# Fonction pour vérifier l'intégrité du fichier JSON
def check_json_integrity(json_data):
    try:
        # Charger le fichier JSON
        data = json.loads(json_data)

        # Vérifier si toutes les clés attendues sont présentes
        if all(key in data for key in expected_keys):
            print("\n")
            print("Intégrité du fichier JSON vérifiée.")
            return True, data
        else:
            print("Erreur : Le fichier JSON ne correspond pas à la structure attendue.")
            return False, None
    except json.JSONDecodeError as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        return False, None

# Fonction pour afficher les informations de la run
def display_run_info(run_data):
    run_name = run_data.get('name', 'N/A')
    started_at = run_data.get('startedAt', 'N/A')

    # Convertir la date et l'heure en un format lisible
    try:
        started_at_datetime = datetime.strptime(started_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        started_at_readable = started_at_datetime.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        started_at_readable = 'Format de date invalide'

    print("\n")
    print(f"Collection ou dossier : {run_name}")
    print(f"Date de l'export : {started_at_readable}")
    print("\n")

# Fonction pour extraire les noms avec tests et les noms sans tests
def extract_names(data):
    results = data.get('results', [])

    names_with_tests = []
    names_without_tests = []

    if isinstance(results, list):
        for item in results:
            name = item.get('id')
            if name:
                if item.get('tests'):
                    names_with_tests.append(name)
                else:
                    names_without_tests.append(name)

    print('Names with tests:', names_with_tests)
    print('Names without tests:', names_without_tests)

    return names_with_tests, names_without_tests

# Fonction pour générer un fichier JSON avec les noms
def generate_output_file(file_path, names):
    with open(file_path, 'w') as output_file:
        json.dump(names, output_file, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

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

            # Sauvegarder les noms avec tests dans le fichier JSON
            output_json_path = "chemin/vers/le/fichier/names_with_tests.json"
            generate_output_file(output_json_path, names_with_tests)

            return render_template('results.html', names_with_tests_output=names_with_tests, names_without_tests_output=names_without_tests)
        else:
            return jsonify({'error': 'Le fichier JSON ne correspond pas à la structure attendue'})

    except Exception as e:
        return jsonify({'error': f'Une erreur est survenue : {str(e)}'})

# Ajout de la route pour sauvegarder les noms avec tests
@app.route('/save_names_with_tests', methods=['POST'])
def save_names_with_tests():
    try:
        # Récupérer les noms avec tests depuis la requête
        names_with_tests = request.json.get('names_with_tests')

        # Vérifier si la clé 'names_with_tests' existe dans la requête
        if names_with_tests is not None:
            # Générer et sauvegarder le fichier JSON avec les noms et les tests
            output_json_path = "names_with_tests.json"
            generate_output_file(output_json_path, names_with_tests)
            return jsonify({'success': 'Noms avec tests sauvegardés avec succès'})
        else:
            return jsonify({'error': 'La clé "names_with_tests" est manquante dans la requête'})
    except Exception as e:
        return jsonify({'error': f'Une erreur est survenue : {str(e)}'})
