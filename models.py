from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Bonbon(models.Model):
    """
    Classe de modèle représentant un bonbon.

    Notre classe représente à la fois la table et les champs de base
    de données.

    """

    # Pour chaque champ, il existe plusieurs options possibles selon le type,
    # qui sont décrits ici : https://docs.djangoproject.com/fr/3.1/topics/db/models/#field-options
    # Presque tous les champs possèdent une option "verbose_name" qui permet
    # de définir le nom "lisible" pour le champ. Ce nom est utilisé automatiquement
    # par l'admin de Django.
    # Dans notre projet, j'ai marqué tous les "verbose_name" comme traduisibles,
    # ainsi il serait possible dans l'administration, de voir tous nos en-têtes
    # de listes d'objets traduits, selon la langue qu'on utilise dans l'admin.
    nom = models.CharField(max_length=64, verbose_name=_("Nom"))
    marque = models.CharField(max_length=64, verbose_name=_("Marque"))
    gout = models.CharField(max_length=32, verbose_name=_("Goût"))
    prix = models.FloatField(default=0.0, verbose_name=_("Prix du paquet"))
    poids = models.IntegerField(default=0, verbose_name=_("Poids du paquet"))
    creation = models.DateField(auto_now=True, verbose_name=_("Créé le"))
    # Ce champ, qui est une clé étrangère, est représenté dans votre base
    # de données comme un champ qui pointe vers une entrée dans la table
    # des fabricants.
    fabricant = models.ForeignKey("bonbons.Fabricant", on_delete=models.CASCADE, related_name="bonbons_fabriques", null=True, blank=True)

    class Meta:
        # Ces deux options définissent le nom lisible de notre modèle
        # c'est utilisé par exemple dans l'interface d'administration de Django.
        verbose_name = "Bonbon"
        verbose_name_plural = "Bonbons"

    def prix_au_kilo(self):
        """
        Renvoie le prix au kilo du bonbon.

        Returns:
            Connaissant le prix du paquet et le poids du paquet,
            on renvoie le prix au kilo.
            Si le paquet a un poids nul, et qu'on ne peut donc
            pas calculer son prix au kilo, la méthode renvoie
            la valeur `None`.

        """
        try:
            return self.prix * (1000 / self.poids)
        except ZeroDivisionError:
            return None


class Fabricant(models.Model):
    """
    Classe de modèle représentant un fabricant de bonbon.

    Notre classe représente à la fois la table et les champs de base
    de données pour la table.

    """

    nom = models.CharField(max_length=50, verbose_name=_("Nom"))
    url = models.URLField(max_length=100, verbose_name=_("Site web"))
    email = models.EmailField(max_length=50, verbose_name=_("Contact"))
    cree_le = models.DateField(auto_now_add=True, verbose_name=_("Date de création"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    def __str__(self):
        """
        Définit la représentation textuelle de l'objet.

        On définit via cette méthode ce qu'on verrait par exemple dans une
        console, si on exécutait "print(objet)".
        Par défaut, si vous ne redéfinissez pas cette méthode, Django
        fournit une implémentation qui afficherait "<Fabricant object 1>" par
        exemple.

        """
        return f"Fabricant : {self.nom}"

    def get_absolute_url(self):
        """
        Définit l'URL pour accéder à la page de détail de l'instance.

        Returns:
            L'URL de la page de détail de l'objet.

        Notes:
            Quand vous définissez cette méthode, l'administration de Django
            s'en sert pour que quand vous cliquez sur un objet de votre modèle
            pour le modifier, il y a un lien qui s'affiche pour aller voir
            la page de détail de l'objet.

        """
        return reverse("viewone", kwargs={"identifier": self.id})
