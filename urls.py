from django.urls import path

from bonbons.views import view_bonbon, view_all_bonbons, view_formulaire_creation

# Liste des sous-URL qui sont reconnues par l'application des bonbons.
# Ces chemins s'ajoutent à l'URL utilisée dans notre fichier projet/urls.py
# qui fait un "include" vers bonbons/urls.py
urlpatterns = [
    # On définit une URL dynamique dont une partie est un nombre entier
    # on se sert de ce nombre entier pour aller chercher un bonbon.
    path('view_one/<int:identifier>', view_bonbon, name="viewone"),
    # Le reste, c'est des URLs classiques, auxquelles on a attribué un nom
    # Et on préférera retrouver ces URLs par leur nom que les réécrire entièrement
    # à chaque fois qu'on veut les référencer.
    path('view_all', view_all_bonbons, name="viewall"),
    path('formulaire', view_formulaire_creation, name="formulaire"),
]
