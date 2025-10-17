# Gaoh Conseil - Module de Gestion des Investisseurs

## Description

Module Odoo pour la gestion complète des investisseurs et de leurs portefeuilles d'investissements immobiliers et placements financiers.

## Fonctionnalités

### Gestion des Investisseurs
- Informations personnelles complètes (civilité, nom, prénom, date de naissance, etc.)
- Adresse et coordonnées
- Informations fiscales (TMI, impôts, liquidités)
- Suivi des consultants et dates importantes
- Détentions (épargne retraite, capinvest, girardin)

### Investissements Immobiliers
- Détails des programmes immobiliers
- Dispositifs fiscaux (Pinel, LMNP, Malraux, etc.)
- Suivi des dates importantes (option, réservation, livraison, acte)
- Gestion des commandes et états
- Informations financières

### Placements Financiers
- Produits de placement variés
- Suivi des contrats et partenaires
- Programmation des versements
- Historique des mouvements
- Encours et valeurs actualisées

### Import Excel
- Import massif depuis fichiers Excel
- Support des trois types de données (investisseurs, immobilier, placements)
- Gestion intelligente des doublons (création ou mise à jour)
- Rapport détaillé des imports

## Installation

1. Copier le dossier `gaoh_conseil` dans le répertoire `addons` de votre instance Odoo
2. Redémarrer le serveur Odoo
3. Activer le mode développeur
4. Aller dans Apps et mettre à jour la liste des applications
5. Rechercher "Gaoh Conseil" et installer le module

## Dépendances

- Python 3.8+
- Odoo 18.0
- openpyxl (pour l'import Excel): `pip install openpyxl`
- python-dateutil

## Utilisation

### Accès au module
Après installation, un nouveau menu "Gaoh Conseil" apparaît dans la barre de navigation principale.

### Menu principal
- **Investisseurs** : Gestion de la liste des investisseurs
- **Investissements**
  - Investissements Immobiliers
  - Placements Financiers
- **Configuration**
  - Import Excel

### Import de données
1. Préparer un fichier Excel avec les colonnes appropriées
2. Aller dans Configuration > Import Excel
3. Sélectionner le type d'import
4. Choisir le fichier
5. Lancer l'import
6. Consulter le rapport

### Format des fichiers Excel

#### Investisseurs
Colonnes requises :
- Nom (obligatoire)
- Prénom
- Email
- Téléphone Portable
- Ville
- Consultant Apporteur
- etc.

#### Investissements Immobiliers
Colonnes requises :
- Nom complet Investisseur (obligatoire)
- Email Investisseur
- Nom Programme (obligatoire)
- Ville Programme
- Prix TTC
- etc.

#### Placements Financiers
Colonnes requises :
- Nom complet Investisseur (obligatoire)
- Email Investisseur
- Libellé Produit (obligatoire)
- Type de Produit
- Partenaire
- etc.

## Droits d'accès

Deux groupes sont disponibles :
- **Utilisateur** : Lecture, écriture et création (pas de suppression)
- **Manager** : Tous les droits (y compris suppression)

## Support

Pour toute question ou problème, contactez l'équipe Gaoh Conseil.

## Version

- Version actuelle : 1.0.0
- Compatible avec : Odoo 18.0
- Licence : LGPL-3

## Auteur

Gaoh Conseil
