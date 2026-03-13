from flask import Blueprint, render_template
import pandas as pd

# Load the dataset once when app starts
df = pd.read_csv("cars.csv")

# Get unique values
unique_marques = sorted(df["Marque"].dropna().unique())
unique_modeles = sorted(df["Modele"].dropna().unique())
unique_villes = sorted(df["Ville"].dropna().unique())
unique_secteurs = sorted(df["Secteur"].dropna().unique())

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/")
def home():
    return render_template(
        "form.html",
        marques=unique_marques,
        modeles=unique_modeles,
        villes=unique_villes,
        secteurs=unique_secteurs,
    )
