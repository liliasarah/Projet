from django.db import models
from authentication.models import Client
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
################leproduit####################
class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='produits/')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    CATEGORIE_CHOICES = [
        ('Occasion', 'Occasion'),
        ('Collection', 'Collection'),
        ('Cadeaux', 'Cadeaux'),
        ('Decoration', 'Decoration'),
    ]
    categorie = models.CharField(
        max_length=20, choices=CATEGORIE_CHOICES, default='Occasion')


    def __str__(self):
        return self.nom
    
###################lacommande et le panier#####################
class Commande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField(default=1)
    WILAYA_CHOICES = [
        ('Adrar', 'Adrar'),
        ('Chlef', 'Chlef'),
        ('Laghouat', 'Laghouat'),
        ('Oum El Bouaghi', 'Oum El Bouaghi'),
        ('Batna', 'Batna'),
        ('Béjaïa', 'Béjaïa'),
        ('Biskra', 'Biskra'),
        ('Béchar', 'Béchar'),
        ('Blida', 'Blida'),
        ('Bouira', 'Bouira'),
        ('Tamanrasset', 'Tamanrasset'),
        ('Tébessa', 'Tébessa'),
        ('Tlemcen', 'Tlemcen'),
        ('Tiaret', 'Tiaret'),
        ('Tizi Ouzou', 'Tizi Ouzou'),
        ('Alger', 'Alger'),
        ('Djelfa', 'Djelfa'),
        ('Jijel', 'Jijel'),
        ('Sétif', 'Sétif'),
        ('Saïda', 'Saïda'),
        ('Skikda', 'Skikda'),
        ('Sidi Bel Abbès', 'Sidi Bel Abbès'),
        ('Annaba', 'Annaba'),
        ('Guelma', 'Guelma'),
        ('Constantine', 'Constantine'),
        ('Médéa', 'Médéa'),
        ('Mostaganem', 'Mostaganem'),
        ('M\'Sila', 'M\'Sila'),
        ('Mascara', 'Mascara'),
        ('Ouargla', 'Ouargla'),
        ('Oran', 'Oran'),
        ('El Bayadh', 'El Bayadh'),
        ('Illizi', 'Illizi'),
        ('Bordj Bou Arreridj', 'Bordj Bou Arreridj'),
        ('Boumerdès', 'Boumerdès'),
        ('El Tarf', 'El Tarf'),
        ('Tindouf', 'Tindouf'),
        ('Tissemsilt', 'Tissemsilt'),
        ('El Oued', 'El Oued'),
        ('Khenchela', 'Khenchela'),
        ('Souk Ahras', 'Souk Ahras'),
        ('Tipaza', 'Tipaza'),
        ('Mila', 'Mila'),
        ('Aïn Defla', 'Aïn Defla'),
        ('Naâma', 'Naâma'),
        ('Aïn Témouchent', 'Aïn Témouchent'),
        ('Ghardaïa', 'Ghardaïa'),
        ('Relizane', 'Relizane')
    ]

    wilaya = models.CharField(
        max_length=20, choices=WILAYA_CHOICES, default='Alger')

    def __str__(self):
        return f"Commande #{self.pk} - {self.client.username}"

######################livraison###################
class Livraison(models.Model):
    commande = models.ManyToManyField(Commande)
    date_livraison = models.DateTimeField()
    statut_livraison = models.CharField(max_length=255, default='En cours de préparation')

   
    @property
    def valide(self):
        commandes = self.commande.all()
        n = len(commandes)
        for c in commandes:
            for i in range(n):
                if c.client != commandes[i].client:
                    return False
        return True
        
    @property
    def adresse_livraison(self):
        return self.commande.all()[0].client.adresse
        
    @property
    def prix_livraison(self):
        wilayas = ['Adrar', 'Chlef', 'Laghouat', 'Oum El Bouaghi', 'Batna', 'Béjaïa', 'Biskra', 'Béchar', 'Blida', 'Bouira', 'Tamanrasset', 'Tébessa', 'Tlemcen', 'Tiaret', 'Tizi Ouzou', 'Alger', 'Djelfa', 'Jijel', 'Sétif', 'Saïda', 'Skikda', 'Sidi Bel Abbès', 'Annaba', 'Guelma', 'Constantine', 'Médéa', 'Mostaganem', 'M\'Sila', 'Mascara', 'Ouargla', 'Oran', 'El Bayadh', 'Illizi', 'Bordj Bou Arreridj', 'Boumerdès', 'El Tarf', 'Tindouf', 'Tissemsilt', 'El Oued', 'Khenchela', 'Souk Ahras', 'Tipaza', 'Mila', 'Aïn Defla', 'Naâma', 'Aïn Témouchent', 'Ghardaïa', 'Relizane']
        if self.commande.wilaya == 'Adrar':
            return 2300.00
        elif self.commande.wilaya == 'Chlef':
            return 4000.00

    @property
    def prix_total(self):
        somme = 0
        for commande in self.commande.all():
            prix = commande.produit.prix
            quantite = commande.quantite
            resultat = prix * quantite
            somme = somme + resultat

        return somme
    

class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit, through='CartItem')

    def __str__(self):
         return f"Cart #{self.pk} - {self.client.username}"   

class CartItem(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite}x {self.produit.nom}"

    
    
###################wishlist##################
class Wishlist(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)





    






