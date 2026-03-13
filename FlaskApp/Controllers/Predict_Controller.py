from flask import Flask, request, render_template, Blueprint
import numpy as np
import joblib
import pandas as pd

# Load your trained model and target encoder
model = joblib.load("../../Model/car_price_model.pkl")
encoder = joblib.load(
    "../../Model/target_encoder.pkl"
)  # Contains target encoding for ['Secteur', 'Ville', 'Marque', 'Modele']

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/api/predict", methods=["POST"])
def predict():
    try:
        # Read form data
        age = float(request.form["age"])
        modele = request.form["modele"]
        marque = request.form["marque"]
        boite_manuelle = int(request.form["boite_manuelle"])
        puissance_fiscale = float(request.form["puissance_fiscale"])
        carburant_essence = int(request.form["carburant_essence"])
        kilometrage = float(request.form["kilometrage"])
        carburant_diesel = int(request.form["carburant_diesel"])
        secteur = request.form["secteur"]
        origine_ww = int(request.form["origine_ww"])
        ville = request.form["ville"]
        boite_auto = int(request.form["boite_auto"])

        # Prepare a DataFrame for encoding
        input_df = pd.DataFrame(
            [{"Secteur": secteur, "Ville": ville, "Marque": marque, "Modele": modele}]
        )

        # Apply the saved target encoding
        encoded_df = encoder.transform(input_df)

        # Combine with the rest of the numeric features
        other_features = np.array(
            [
                [
                    age,
                    puissance_fiscale,
                    kilometrage,
                    boite_manuelle,
                    carburant_essence,
                    carburant_diesel,
                    origine_ww,
                    boite_auto,
                ]
            ]
        )

        final_input = np.concatenate([other_features, encoded_df.values], axis=1)

        # Make prediction
        prediction = model.predict(final_input)
        predicted_price = np.exp(prediction[0])  # if you trained with log_price

        return f"<h2>Predicted Price: {predicted_price:.2f} MAD</h2>"

    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>"
