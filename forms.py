from django import forms
from django.core.exceptions import ValidationError

from bonbons.models import Bonbon


class BonbonForm(forms.ModelForm):
    """
    Classe de formulaire lié au modèle des bonbons.

    """
    class Meta:
        model = Bonbon
        # L'option permet de choisir la liste des champs qui seront affichés dans
        # le formulaire. Le champ "id" est toujours de type caché donc même si vous l'insérez
        # dans la liste, vous ne le verrez pas dans votre page.
        fields = ["nom", "marque", "gout", "prix", "poids", "fabricant"]

    def clean_poids(self):
        """
        Personnaliser la validation du poids.

        Par exemple, on empêche l'utilisateur de rentrer
        un poids supérieur à 10 000 grammes ou inférieur à 0
        gramme.

        Returns:
            Renvoie le poids que vous avez passé en entrée.

        """
        poids = self.cleaned_data["poids"]
        if poids < 0 or poids > 10000:
            raise ValidationError("Le poids doit être compris entre 0 et 10000 grammes.")
        return poids


class NameForm(forms.Form):
    """
    Classe de formulaire standard, non lié à un modèle.

    Dans une classe de formulaire de ce type, vous définissez tous vos
    champs de formulaire manuellement.

    Vous pouvez vous entraîner à afficher ce formulaire dans une nouvelle page
    et essayer de valider son contenu (la classe est écrite, mais j'ai retiré la
    page qui l'affiche pour que vous puissiez vous entraîner)
    Documentation disponible : https://docs.djangoproject.com/fr/3.1/topics/forms/#building-a-form-in-django


    """
    nom = forms.CharField(label="Nom", max_length=32, min_length=3, required=True)
    prenom = forms.CharField(label="Prenom", max_length=32, min_length=3, required=True)
    age = forms.IntegerField(label="Âge", min_value=15, max_value=120, required=True)

    def clean_nom(self):
        """
        Personnaliser la validation du champ de nom.

        Ici, on va décider que le nom "bulle" (majuscules ou pas)
        est incorrect.

        """
        if self.data["nom"].lower() == "bulle":
            raise ValidationError("Le nom « bulle » n'est pas autorisé.")
        return self.data["nom"]

    def clean(self):
        """
        Personnaliser la validation de tous les champs en même temps.

        Dans notre cas, on va par exemple interdire le choix
        "Jacques" et "Paul" dans prénom et nom respectivement.

        """
        # cleaned_data est un dictionnaire qui contient toutes les
        # valeurs de notre formulaire, mais à la place d'avoir des valeurs
        # textuelles qui viennent d'une page web, toutes les valeurs sont
        # converties dans le bon type python (ex. "15" devient 15, "15/08/2015"
        # devient un objet python datetime.date correspondant au 15 aout 2015)
        self.cleaned_data = super().clean()
        nom = self.cleaned_data["nom"]
        prenom = self.cleaned_data["prenom"]
        if nom.lower() == "paul" and prenom.lower() == "jacques":
            raise ValidationError("Le nom « Paul Jacques » n'est pas autorisé.")
        return self.cleaned_data

