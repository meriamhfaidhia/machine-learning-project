from flask import Flask, render_template, request
import pickle
import traceback

app = Flask(__name__)

# Charger le modèle
model = pickle.load(open('savedmodel.sav', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboards')
def dashboards():
    # Données pour les graphiques
    dashboard_data = {
        'customer_health': {
            'title': 'Santé Clients',
            'charts': {
                'churn_risk': {
                    'type': 'doughnut',
                    'data': [32, 68],  # 32% risque, 68% safe
                    'labels': ['À risque', 'Fidèles'],
                    'colors': ['#ff6384', '#36a2eb']
                },
                'satisfaction': {
                    'type': 'bar',
                    'data': [15, 35, 40, 10],  # Très satisfait à très insatisfait
                    'labels': ['Très satisfait', 'Satisfait', 'Neutre', 'Insatisfait'],
                    'colors': ['#4bc0c0', '#4bc0c0', '#ffcd56', '#ff6384']
                }
            }
        },
        'retention': {
            'title': 'Rétention Clients',
            'charts': {
                'monthly_churn': {
                    'type': 'line',
                    'data': [12, 19, 15, 8, 7, 10],
                    'labels': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
                    'colors': '#9966ff'
                },
                'retention_reasons': {
                    'type': 'polarArea',
                    'data': [35, 25, 20, 15, 5],
                    'labels': ['Prix', 'Service', 'Produit', 'Concurrence', 'Autre'],
                    'colors': ['#ff9f40', '#ff6384', '#36a2eb', '#9966ff', '#c9cbcf']
                }
            }
        }
    }
    return render_template('dashboards.html', dashboards=dashboard_data)

@app.route('/retention-tips')
def retention_tips():
    return render_template('retention_tips.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les valeurs des champs du formulaire
        Account_length = float(request.form.get('Account_length', 0))
        International_plan = 1 if request.form.get('International_plan', '').lower() == 'yes' else 0
        Voice_mail_plan = 1 if request.form.get('Voice_mail_plan', '').lower() == 'yes' else 0
        Number_vmail_messages = float(request.form.get('Number_vmail_messages', 0))
        Total_day_minutes = float(request.form.get('Total_day_minutes', '0').replace(',', '.'))
        Total_day_calls = float(request.form.get('Total_day_calls', 0))
        Total_eve_minutes = float(request.form.get('Total_eve_minutes', '0').replace(',', '.'))
        Total_eve_calls = float(request.form.get('Total_eve_calls', 0))
        Total_night_minutes = float(request.form.get('Total_night_minutes', '0').replace(',', '.'))
        Total_night_calls = float(request.form.get('Total_night_calls', 0))
        Total_intl_minutes = float(request.form.get('Total_intl_minutes', '0').replace(',', '.'))
        Total_intl_calls = float(request.form.get('Total_intl_calls', 0))
        Customer_service_calls = float(request.form.get('Customer_service_calls', 0))

        # Préparer les features pour la prédiction
        features = [[
            Account_length, International_plan, Voice_mail_plan,
            Number_vmail_messages, Total_day_minutes, Total_day_calls,
            Total_eve_minutes, Total_eve_calls, Total_night_minutes,
            Total_night_calls, Total_intl_minutes, Total_intl_calls,
            Customer_service_calls
        ]]
        
        
        print(f"Features utilisées pour la prédiction : {features}")

        # Effectuer la prédiction
        prediction = model.predict(features)[0]
        print(f"Résultat de la prédiction : {prediction}")
        return render_template('result.html', result=prediction)

    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        traceback.print_exc()
        return f"Une erreur est survenue : {e}<br>{traceback.format_exc()}"
    

if __name__ == '__main__':
    app.run(debug=True)
