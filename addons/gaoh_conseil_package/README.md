# 📦 Package Gaoh Conseil - Module Odoo

Bienvenue ! Ce package contient tout le nécessaire pour installer et utiliser le module Gaoh Conseil sur votre serveur Odoo.

## 📋 Contenu du Package

```
gaoh_conseil_package/
├── gaoh_conseil.zip                    # Module Odoo complet (prêt à installer)
├── gaoh_conseil_import_exemple.xlsx   # Fichier Excel d'exemple pour l'import
├── INSTALLATION_GAOH_CONSEIL.md       # Guide d'installation et d'utilisation complet
└── README.md                          # Ce fichier
```

## ⚡ Installation Rapide

### 1. Prérequis

Avant de commencer, assurez-vous d'avoir :
- ✅ Odoo 18.0 installé et fonctionnel
- ✅ Accès administrateur à votre instance Odoo
- ✅ Python 3.8+ avec pip

### 2. Installation des dépendances

```bash
pip install openpyxl python-dateutil
```

### 3. Installation du module

```bash
# Décompresser le module
unzip gaoh_conseil.zip

# Copier dans le dossier addons de votre Odoo
cp -r gaoh_conseil /chemin/vers/votre/odoo/addons/

# Redémarrer Odoo
sudo systemctl restart odoo  # ou votre méthode de redémarrage
```

### 4. Activation dans Odoo

1. Connectez-vous à votre instance Odoo
2. Activez le **mode développeur** (Paramètres > Activer le mode développeur)
3. Allez dans **Apps**
4. Cliquez sur **Mettre à jour la liste des applications**
5. Recherchez **"Gaoh Conseil"**
6. Cliquez sur **Installer**

## 🎯 Fonctionnalités Principales

### 👥 Gestion des Investisseurs
- Fiche complète avec informations personnelles, fiscales et financières
- Suivi des consultants et dates importantes
- Gestion des liquidités et crédits
- Archivage et historique

### 🏢 Investissements Immobiliers
- Détails des programmes immobiliers
- Dispositifs fiscaux (Pinel, Pinel+, LMNP, Malraux, etc.)
- Suivi des dates (option, réservation, livraison, acte)
- Gestion des commandes et états
- Calcul automatique des commissions

### 💰 Placements Financiers
- Produits variés (assurance vie, PER, etc.)
- Suivi des contrats et partenaires
- Programmation des versements
- Historique des mouvements
- Calcul automatique de l'ancienneté
- Suivi des encours et valeurs actualisées

### 📥 Import Excel
- Import massif depuis fichiers Excel
- Support des 3 types de données
- Gestion intelligente des doublons
- Rapport détaillé avec statistiques

## 📚 Documentation

Consultez le fichier **`INSTALLATION_GAOH_CONSEIL.md`** pour :
- Guide d'installation détaillé (2 méthodes)
- Configuration initiale et droits d'accès
- Procédure complète d'import Excel
- Guide d'utilisation quotidienne
- Conseils et bonnes pratiques
- Dépannage des problèmes courants

## 🔧 Configuration Requise

| Composant | Version/Détails |
|-----------|-----------------|
| **Odoo** | 18.0 |
| **Python** | 3.8+ |
| **Dépendances Odoo** | `base`, `mail`, `contacts` |
| **Bibliothèques Python** | `openpyxl`, `python-dateutil` |
| **Base de données** | PostgreSQL (recommandé par Odoo) |

## 🚀 Démarrage Rapide

### Premier investisseur

1. Allez dans **Gaoh Conseil > Investisseurs**
2. Cliquez sur **Créer**
3. Remplissez au minimum :
   - Nom
   - Prénom
   - Email
4. Enregistrez

### Premier import Excel

1. Ouvrez le fichier **`gaoh_conseil_import_exemple.xlsx`**
2. Modifiez les exemples avec vos données
3. Dans Odoo : **Gaoh Conseil > Configuration > Import Excel**
4. Sélectionnez "Investisseurs"
5. Choisissez votre fichier
6. Cliquez sur "Importer"
7. Consultez le rapport

## 🔐 Droits d'Accès

Le module propose 2 niveaux de droits :

| Groupe | Lecture | Écriture | Création | Suppression |
|--------|---------|----------|----------|-------------|
| **Utilisateur** | ✅ | ✅ | ✅ | ❌ |
| **Manager** | ✅ | ✅ | ✅ | ✅ |

## 📊 Structure des Données

```
Investisseur
├── Informations personnelles
├── Contact et adresse
├── Informations fiscales
├── Liquidités et crédits
├── 📁 Investissements Immobiliers (One2many)
└── 📁 Placements Financiers (One2many)
```

## 🎨 Captures d'Écran

Le module dispose de :
- 📋 **Vues listes** : Tableaux avec filtres et recherches avancées
- 📝 **Vues formulaires** : Fiches détaillées avec onglets
- 📊 **Tableaux de bord** : Statistiques et indicateurs
- 🔍 **Recherche avancée** : Filtres multiples et groupements

## 🐛 Dépannage Express

### Le module n'apparaît pas
```bash
# Vérifier l'emplacement
ls -la /chemin/vers/odoo/addons/gaoh_conseil

# Redémarrer Odoo
sudo systemctl restart odoo

# Mettre à jour la liste (mode dev requis)
# Apps > Mettre à jour la liste des applications
```

### Erreur import Excel
```bash
# Installer openpyxl
pip install openpyxl

# Vérifier le format
# Fichier doit être .xlsx (pas .xls)
```

### Problème de droits
```
Paramètres > Utilisateurs & Entreprises > Groupes
Cherchez "Gaoh Conseil"
Ajoutez les utilisateurs aux groupes appropriés
```

## 📞 Support

- 📧 **Email** : support@gaohconseil.com
- 📖 **Documentation Odoo** : https://www.odoo.com/documentation/18.0/
- 🌐 **Site Web** : https://www.gaohconseil.com

## 📝 Informations Techniques

- **Nom technique** : `gaoh_conseil`
- **Version** : 1.0.0
- **Licence** : LGPL-3
- **Auteur** : Gaoh Conseil
- **Compatible** : Odoo 18.0
- **Type** : Application métier (Business App)

## ✨ Prochaines Étapes

1. ✅ Installer le module
2. ✅ Configurer les droits d'accès
3. ✅ Importer vos données (ou créer manuellement)
4. ✅ Former vos utilisateurs
5. ✅ Commencer à utiliser le module quotidiennement

## 🎓 Formation

Nous recommandons :
1. Lire le guide d'installation complet
2. Tester avec les données d'exemple
3. Importer vos vraies données progressivement
4. Former les utilisateurs par groupe (Utilisateur puis Manager)

## 📌 Version

```
Module Gaoh Conseil
Version: 1.0.0
Date: Octobre 2024
Odoo: 18.0
Statut: Production Ready ✅
```

---

**Merci d'avoir choisi Gaoh Conseil !**  
Pour toute question, n'hésitez pas à consulter la documentation ou à nous contacter.

🚀 **Bonne utilisation !**
