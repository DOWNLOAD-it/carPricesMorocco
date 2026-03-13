from rest_framework.views import APIView
import numpy as np
import pandas as pd
import joblib
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import os
from .models import Marque, Modele, Secteur, Ville


class MarqueList(APIView):
    def get(self, request):
        data = list(Marque.objects.values("id", "name"))
        return JsonResponse(data, safe=False)


class VilleList(APIView):
    def get(self, request):
        data = list(Ville.objects.values("id", "name"))
        return JsonResponse(data, safe=False)


class ModelesByMarque(View):
    def get(self, request, marque):
        modeles = Modele.objects.filter(marque_id=marque).values("id", "name")
        return JsonResponse(list(modeles), safe=False)


class SecteursByVille(View):
    def get(self, request, ville):
        secteurs = Secteur.objects.filter(ville_id=ville).values("id", "name")
        return JsonResponse(list(secteurs), safe=False)


# Load ML model and preprocessors once at the module level
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "ml_assets", "car_price_model.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "ml_assets", "target_encoder.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "ml_assets", "standard_scaler.pkl"))


@method_decorator(csrf_exempt, name="dispatch")
class PredictPriceView(View):
    def post(self, request):
        try:

            body = json.loads(request.body)

            # Extract the required fields and store each in a variable
            age = body.get("Age (annees)")
            modele = body.get("Modele")
            marque = body.get("Marque")
            boite_de_vitesses_manuelle = body.get("Boite de vitesses_Manuelle")
            puissance_fiscale = body.get("Puissance fiscale")
            type_de_carburant_essence = body.get("Type de carburant_Essence")
            kilometrage = body.get("Kilometrage lisse (en milliers km)")
            type_de_carburant_diesel = body.get("Type de carburant_Diesel")
            secteur = body.get("Secteur")
            origine_ww_au_maroc = body.get("Origine_WW au Maroc")
            ville = body.get("Ville")
            origine_dedouanee = body.get("Origine_Dédouanée")

            # Create a DataFrame from the extracted fields
            data = {
                "Age (annees)": [age],
                "Modele": [modele],
                "Marque": [marque],
                "Boite de vitesses_Manuelle": [boite_de_vitesses_manuelle],
                "Puissance fiscale": [puissance_fiscale],
                "Type de carburant_Essence": [type_de_carburant_essence],
                "Kilometrage lisse (en milliers km)": [kilometrage],
                "Type de carburant_Diesel": [type_de_carburant_diesel],
                "Secteur": [secteur],
                "Origine_WW au Maroc": [origine_ww_au_maroc],
                "Ville": [ville],
                "Origine_Dédouanée": [origine_dedouanee],
            }

            df = pd.DataFrame(data)

            # Target encode the categorical fields
            categorical_columns = ["Modele", "Marque", "Secteur", "Ville"]
            encoded_features = encoder.transform(df[categorical_columns])
            encoded_df = pd.DataFrame(
                encoded_features, columns=encoder.get_feature_names_out()
            )

            # Replace the original categorical columns with the encoded ones
            df[encoded_df.columns] = encoded_df

            # Scale the specified numerical features
            numerical_features = [
                "Puissance fiscale",
                "Kilometrage lisse (en milliers km)",
                "Age (annees)",
            ]
            df[numerical_features] = scaler.transform(df[numerical_features])

            # Define the exact column order as per the model's expected order
            model_columns = [
                "Age (annees)",
                "Modele",
                "Marque",
                "Boite de vitesses_Manuelle",
                "Puissance fiscale",
                "Type de carburant_Essence",
                "Kilometrage lisse (en milliers km)",
                "Type de carburant_Diesel",
                "Secteur",
                "Origine_WW au Maroc",
                "Ville",
                "Origine_Dédouanée",
            ]

            # Reorder the columns to match the model's expected order
            df = df[model_columns]

            # Keep df as a DataFrame for model input
            # Get predictions from the model
            predictions = model.predict(df)  # Pass the DataFrame directly

            # Convert the log-transformed predictions back to normal scale
            normal_prices = np.exp(predictions) * 1000  # Adjust scaling as necessary

            # Return the predictions as JSON
            return JsonResponse({"predictions": normal_prices.tolist()}, safe=False)

        except Exception as e:
            # Return error message if an exception occurs
            return JsonResponse({"error": str(e)}, status=400)
