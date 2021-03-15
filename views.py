from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from bonbons.forms import BonbonForm
from bonbons.models import Bonbon


def view_all_bonbons(request):
    """
    Fonction de vue pour afficher tous les bonbons de la base de données.

    C'est une fonction de vue simple, qui ne prend pas de paramètre
    autre que request, puisque dans notre définition d'URL qui pointe
    vers cette fonction, l'URL ne prend pas de paramètre dynamique.
    """
    # On récupère tous les bonbons de notre base de données.
    bonbons = Bonbon.objects.all()
    # On affiche notre page en utilisant un fichier de gabarit, qui
    # aura accès à notre liste de `bonbons` via le nom "bonbons".
    return render(request, "bonbons/view_all.html", {"bonbons": bonbons})


def view_bonbon(request, identifier=None):
    """
    Fonction de vue pour afficher le détail d'un bonbon.

    Cette fonction prend en paramètre un paramètre nommé
    `identifier`, que l'on a configuré dans nos URLS de
    l'application bonbons. (voir fichier urls.py).

    Ce paramètre `identifier` est un entier, et on s'en sert
    pour récupér un bonbon qui possède la même valeur que `identifier`
    dans son champ `id` (clé primaire, c'est-à-dire un champ dont les
    valeurs sont différentes pour chacun des bonbons et qui permet donc
    d'identifier à coup sûr chaque bonbon dans notre base).
    """
    # On a importé `get_object_or_404`, qui permet de récupérer un bonbon selon
    # des critères qu'on passe en paramètres, et si on ne trouve rien en base
    # de données, on renvoie une erreur 404, ce qui pousse Django à Afficher
    # la page "Non trouvé".
    bonbon = get_object_or_404(Bonbon, id=identifier)
    # Si la ligne du dessus n'a pas provoqué d'erreur, afficher notre page de bonbon.
    # Via la fonction `render`, on affiche un gabarit auquel on injecte notre variable
    # `bonbon`, à laquelle le gabarit aura accès via le nom `bonbon`.
    return render(request, "bonbons/view_one.html", {"bonbon": bonbon})


def view_formulaire_creation(request):
    """
    Afficher un formulaire destiné à ajouter de nouveaux bonbons.

    Args:
        request: objet de requête HTTP (la requête envoyée par le navigateur)

    Returns:
        Une réponse HTTP qui est une instance de la classe HttpResponse (comme
        dans toutes les vues Django).

    """
    # Une requête HTTP possède la méthode "POST" lorsque des données de formulaires sont transmises.
    if request.method == "POST":
        # Initialiser un formulaire lié aux données de formulaire
        # passées par le navigateur.
        form = BonbonForm(request.POST)
        # Vérifie que toutes les contraintes du formulaire
        # (vérification des types de valeurs + vérifications
        # personnalisées) sont respectées.
        if form.is_valid():
            # On crée une nouvelle instance de notre modèle `Bonbon`
            # initialisé avec les données de formulaire
            nouveau_bonbon = form.save()
            # puis on le sauvegarde en base de données
            nouveau_bonbon.save()
            # Ensuite, on indique au système de messages de Django
            # (https://docs.djangoproject.com/fr/3.1/ref/contrib/messages/)
            # qu'à la prochaine page affichée, il faudrait afficher un message à
            # l'utilisateur.
            # L'affichage de ce message est géré dans notre template
            # base.html.
            messages.add_message(request, messages.SUCCESS, "Bonbon bien ajouté")
            # Et on demande au navigateur de rediriger vers l'URL de base du site
            return HttpResponseRedirect(reverse("home"))
    else:
        # Par défaut, lorsqu'on affiche notre page avec la méthode GET
        # (en opposition à la méthode POST), on génère une instance de notre
        # formulaire de bonbons, mais vierge.
        form = BonbonForm()
    # Afficher la page via un gabarit auquel on transmet notre formulaire à afficher.
    return render(request, "bonbons/view_formulaire.html", {"form": form})
