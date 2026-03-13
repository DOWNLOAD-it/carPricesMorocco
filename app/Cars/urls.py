from django.urls import path
from .api import (
    MarqueList,
    VilleList,
    ModelesByMarque,
    SecteursByVille,
    PredictPriceView,
)

urlpatterns = [
    path(
        "modeles_by_marque/<int:marque>/",
        ModelesByMarque.as_view(),
        name="modeles_by_marque",
    ),
    path(
        "secteurs_by_ville/<int:ville>/",
        SecteursByVille.as_view(),
        name="secteurs_by_ville",
    ),
    path("marques/", MarqueList.as_view()),
    path("villes/", VilleList.as_view()),
    path("predict/", PredictPriceView.as_view(), name="predict-form"),  # Add this line
]
