from django.test import TestCase, Client
from django.urls import reverse

from bonbons.models import Bonbon


class TestBonbon(TestCase):
    """
    Classe de tests Django pour tester nos fonctionnalités sur les bonbons.

    Pour lancer les tests dans Django, en ligne de commande, il faut taper
    `./manage.py test`. Le processus va créer une base de données de test,
    lancer les migrations pour y ajouter les tables et les champs.
    Ensuite c'est à vous d'ajouter des données dans cette table et de tester
    ce que vous souhaitez.

    """

    def setUp(self):
        """
        Cette méthode est appelée automatiquement une fois au début des tests
        de notre classe TestBonbon, et permet de mettre en place nos données
        dans la base, avant de commencer à faire des tests dessus.

        Dans notre cas, on crée quelques bonbons avec des valeurs différentes
        pour tester par exemple que le calcul du poids au kilo fonctionne comme
        prévu.
        Et on se garde ces trois bonbons dans des attributs de notre instance de
        BonbonCase (en faisant "self.bonbon1 = ...")

        """
        self.bonbon1 = Bonbon.objects.create(nom="A", marque="AA", gout="AAA", poids=0, prix=1000)
        self.bonbon2 = Bonbon.objects.create(nom="B", marque="BB", gout="BBB", poids=400, prix=1000)
        self.bonbon3 = Bonbon.objects.create(nom="C", marque="CC", gout="CCC", poids=500, prix=4)

    def test_prix_au_kilo(self):
        """
        Tester que le calcul du prix au kilo des bonbons se comporte comme prévu.

        On s'assure ainsi que si un jour, un autre développeur touche à la
        méthode qui fait le calcul, pour une raison ou pour une autre, les
        résultats resteront correct.

        """
        # Notre instance de BonbonTest a accès à des méthodes "assertTruc"
        # qui permettent de faire plusieurs types de vérifications.
        self.assertIsNone(self.bonbon1.prix_au_kilo())
        self.assertEqual(self.bonbon2.prix_au_kilo(), 2500)
        self.assertEqual(self.bonbon3.prix_au_kilo(), 8)

    def test_page_bonbon(self):
        """
        On peut effectuer des tests en allant récupérer des pages
        de notre site, et en allant voir si ces pages contiennent du
        contenu ou si ce sont des pages d'erreur 404 ou autres.

        Pour ça on utilise ce qu'on appelle un clien de test.

        """
        # On instancie simplement un client de test, et on pourra
        # l'utiliser pour aller chercher des pages, envoyer des données
        # de formulaire, etc.
        client = Client()
        # On choisit une page que l'on souhaite tester, en l'occurrence
        # la page de détail de `self.bonbon2`.
        url = reverse("viewone", kwargs={"identifier": self.bonbon2.id})
        # On utilise notre client pour récupérer la page
        response = client.get(url)
        # Et on vérifie que la page a été renvoyée sans problème
        # ce qui en HTTP correspond à un code 200. (404 si la page est introuvable)
        self.assertEqual(response.status_code, 200)
        # Ici on vérifie que le texte de la page contient certains mots.
        # la spéficité ici est que `response.content` ne contient pas du Unicode
        # mais des `bytes`. Il faut donc que la chaîne à comparer soit une chaîne
        # préfixée par un b"". Il s'agit de python intermédiaire/avancé.
        self.assertTrue(b"body" in response.content)
        # Ici on récupère une page qui n'existe pas, et on vérifie bien
        # que la réponse du serveur contient un code HTTP 404
        response = client.get("dgjdfkdfgkljdfglkjdflkfd")
        self.assertEqual(response.status_code, 404)


