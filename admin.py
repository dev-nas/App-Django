from django.contrib import admin

from bonbons.models import Bonbon, Fabricant

admin.site.register(Fabricant)

@admin.register(Bonbon)
class BonbonAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'admin Django pour les bonbons.

    """
    # Vous pouvez afficher les valeurs des champs du modèle, mais aussi des
    # valeurs renvoyées par des méthodes du modèle (ex. prix_au_kilo)
    list_display = ['id', "nom", "marque", "prix", "poids", "gout", "fabricant", "prix_au_kilo"]
    list_filter = ["fabricant"]
    search_fields = ["nom", "marque"]
    actions = ["changer_poids"]

    def get_autre_valeur(self, instance: Bonbon):
        """
        Cette méthode permet de renvoyer une valeur calculée pour une instance du modèle.

        Args:
            instance: l'instance de bonbon à afficher dans l'admin

        Returns:
            Une valeur calculée quelconque. On peut se servir du nom de
            cette méthode comme entrée dans l'option "list_display".

        """
        return "Valeur calculée"

    def changer_poids(self, request, queryset):
        """
        Cette méthode est une action qui permet de changer le poids de bonbons
        sélectionnés dans l'admin.

        Args:
            request: une action prend un argument request
            queryset: il faut aussi le queryset contenant la liste des bonbons sélectionnés.

        """
        # On utilise la méthode update() pour changer une ou plusieurs valeurs
        # de tous les éléments d'un queryset.
        queryset.update(poids=1000)
        self.message_user(request, f"Le poids des {queryset.count()} bonbons a été mis à jour.")
