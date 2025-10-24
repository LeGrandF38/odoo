# Gaoh Conseil - Module de Gestion des Investisseurs

## 📋 Description

Module Odoo 18 pour la gestion des investisseurs et de leurs portefeuilles d'investissements (immobilier et placements financiers).

## ✨ Fonctionnalités

### 👥 Gestion des Investisseurs
- Fiche complète avec informations personnelles et fiscales
- Suivi des coordonnées et autorisations de communication
- **Lien automatique avec les contacts Odoo** (res.partner)
- **Accès portail pour les investisseurs**

### 🏢 Investissements Immobiliers
- Suivi des programmes immobiliers
- Dispositifs fiscaux (Pinel, Denormandie, etc.)
- États de commande (Réservation, Signature, Livraison, etc.)
- Suivi des dates et prix

### 💰 Placements Financiers
- Gestion des produits financiers (Assurance-vie, PER, SCPI, etc.)
- Suivi des partenaires et valeurs d'encours
- États de commande et dates d'effet

### 📊 Import de Données
- Import Excel pour migration de données
- Support de fichiers .xlsx et .xls
- Mapping automatique des colonnes

## 🚀 Installation

1. **Copier le module** dans le dossier `addons` de votre instance Odoo
2. **Redémarrer Odoo** pour qu'il détecte le nouveau module
3. **Activer le mode développeur** : Paramètres → Activer le mode développeur
4. **Mettre à jour la liste des applications** : Applications → Mettre à jour la liste des applications
5. **Installer le module** : Rechercher "Gaoh Conseil" et cliquer sur Installer

## ⚙️ Configuration

### Groupes de Sécurité

Le module définit 3 niveaux d'accès :

#### 🔹 Utilisateur Gaoh Conseil
- Peut consulter tous les investisseurs
- Peut créer et modifier ses propres investisseurs
- Accès en lecture aux investissements

**Pour affecter ce rôle :**
1. Aller dans **Paramètres → Utilisateurs & Sociétés → Utilisateurs**
2. Sélectionner un utilisateur
3. Dans l'onglet **"Droits d'accès"**, section **"Gaoh Conseil"**
4. Cocher **"Utilisateur"**

#### 🔸 Manager Gaoh Conseil
- Tous les droits de l'utilisateur
- Peut modifier tous les investisseurs et investissements
- Peut supprimer des enregistrements
- Accès à l'import Excel

**Pour affecter ce rôle :**
1. Aller dans **Paramètres → Utilisateurs & Sociétés → Utilisateurs**
2. Sélectionner un utilisateur
3. Dans l'onglet **"Droits d'accès"**, section **"Gaoh Conseil"**
4. Cocher **"Manager"**

#### 🔷 Administrateur
- Accès total au module
- Peut configurer la sécurité
- Peut gérer les accès portail

### 🌐 Accès Portail pour Investisseurs

Les investisseurs peuvent accéder à leurs informations via le portail client :

1. **Créer/Lier le contact** : Le module lie automatiquement chaque investisseur à un contact Odoo
2. **Inviter au portail** :
   - Ouvrir la fiche investisseur
   - Cliquer sur le champ "Contact Odoo Associé"
   - Dans la fiche du contact, utiliser l'action **"Accorder l'accès au portail"**
   - Envoyer l'invitation par email
3. **Accès de l'investisseur** :
   - L'investisseur reçoit un email avec ses identifiants
   - Il peut se connecter sur `/my/investisseur`
   - Il voit ses informations et investissements en lecture seule

## 📖 Utilisation

### Créer un Investisseur

1. Menu : **Gaoh Conseil → Investisseurs → Investisseurs**
2. Cliquer sur **Nouveau**
3. Remplir les informations :
   - **Informations Personnelles** : Civilité, nom, prénom, date de naissance
   - **Contact** : Email, téléphones, autorisations
   - **Adresse** : Adresse complète
   - **Consultant** : Consultant apporteur
   - **Informations Fiscales** : TMI, impôts
   - **Liquidités et Crédits**
4. Le nom complet et l'âge sont calculés automatiquement
5. Un contact Odoo est créé automatiquement

### Ajouter des Investissements

#### Investissement Immobilier
1. Dans la fiche investisseur, onglet **Investissements Immobiliers**
2. Cliquer sur **Ajouter une ligne**
3. Remplir les informations du programme
4. Sauvegarder

#### Placement Financier
1. Dans la fiche investisseur, onglet **Placements Financiers**
2. Cliquer sur **Ajouter une ligne**
3. Remplir les informations du placement
4. Sauvegarder

### 📥 Importer des Données Excel

1. Menu : **Gaoh Conseil → Configuration → Import Excel**
2. Télécharger le **Fichier Modèle** pour voir le format attendu
3. Préparer votre fichier Excel avec les colonnes correspondantes
4. Sélectionner votre fichier et cliquer sur **Importer**
5. Vérifier les résultats dans les logs

**Format Excel attendu :**
- **Investisseurs** : nom, prénom, email, téléphone, etc.
- **Investissements Immobiliers** : nom_complet_investisseur, nom_programme, ville_programme, etc.
- **Placements** : nom_complet_investisseur, libelle_produit, type_produit, etc.

### 🔍 Recherches et Filtres

#### Recherche Rapide
- Utiliser la barre de recherche pour trouver par nom, email, téléphone, ville

#### Filtres Prédéfinis
- **Avec Épargne Retraite** : Investisseurs détenteurs de PER
- **Avec Capinvest** : Investisseurs détenteurs de Capinvest
- **Avec Girardin** : Investisseurs en Girardin
- **NPAI** : Contacts N'habite Pas à l'Adresse Indiquée

#### Grouper par
- Consultant Apporteur
- Ville
- Situation Familiale

## 🗂️ Structure des Données

### Modèle : gaoh.investisseur
**Champs principaux :**
- `nom_complet` : Nom complet calculé automatiquement
- `partner_id` : Lien vers res.partner (contact Odoo)
- `civilite` : M./Mme/Autre
- `date_naissance` : Date de naissance
- `age` : Âge calculé automatiquement
- `situation_familiale` : Célibataire/Marié(e)/Pacsé(e)/etc.
- `consultant_apporteur` : Consultant responsable

### Modèle : gaoh.investissement.immobilier
**Champs principaux :**
- `investisseur_id` : Lien vers l'investisseur
- `nom_programme` : Nom du programme immobilier
- `dispositif_fiscal` : Pinel/Denormandie/etc.
- `prix_ttc` : Prix TTC en euros
- `etat_commande` : Réservation/Signature/etc.

### Modèle : gaoh.investissement.placement
**Champs principaux :**
- `investisseur_id` : Lien vers l'investisseur
- `type_produit` : Assurance-vie/PER/SCPI/etc.
- `va_encours` : Valeur d'encours en euros
- `etat_commande` : Demande/En cours/Effectif/etc.

## 🔧 Support Technique

### Prérequis
- **Odoo** 18.0 ou supérieur
- **Python** 3.10 ou supérieur
- **Modules dépendants** : `base`, `mail`, `contacts`, `portal`

### Dépendances Python
Installées automatiquement avec Odoo :
- `openpyxl` : Pour l'import Excel (.xlsx)
- `xlrd` : Pour les anciens formats Excel (.xls)

### Logs et Débogage

Les erreurs d'import Excel sont loggées dans :
- **Interface** : Messages dans le wizard
- **Console** : Logs serveur Odoo avec préfixe `[Import Excel]`

Pour activer les logs détaillés :
```bash
# Dans odoo.conf ou ligne de commande
--log-level=debug
```

## 🔄 Maintenance

### Mise à Jour du Module

1. **Sauvegarder la base de données**
2. **Remplacer les fichiers** du module
3. **Redémarrer Odoo**
4. **Mettre à jour** : Applications → Rechercher "Gaoh Conseil" → Mettre à jour

### Sauvegarde des Données

Recommandé avant toute mise à jour :
```bash
# Sauvegarder la base PostgreSQL
pg_dump nom_base > backup.sql

# Ou via l'interface Odoo
Paramètres → Base de données → Sauvegarder
```

## ❓ Foire Aux Questions (FAQ)

### Q: Comment donner accès à un utilisateur interne ?
**R:** Aller dans Paramètres → Utilisateurs, créer/modifier l'utilisateur, et dans "Droits d'accès" → section "Gaoh Conseil", cocher "Utilisateur" ou "Manager".

### Q: Comment donner accès portail à un investisseur ?
**R:** Ouvrir la fiche investisseur → Cliquer sur le contact associé → Action "Accorder l'accès au portail".

### Q: L'import Excel échoue, que faire ?
**R:** Vérifier que :
- Le fichier est au format .xlsx ou .xls
- Les colonnes correspondent au modèle
- Les noms des investisseurs existent déjà pour les investissements
- Les dates sont au format JJ/MM/AAAA

### Q: Comment personnaliser les états de commande ?
**R:** Les états sont définis dans les modèles. Pour les modifier, éditer les fichiers :
- `models/investissement_immobilier.py` (etat_commande)
- `models/investissement_placement.py` (etat_commande)

### Q: Peut-on exporter les données ?
**R:** Oui, utiliser l'export standard d'Odoo :
- Vue liste → ☰ Actions → Exporter
- Sélectionner les champs à exporter
- Format : CSV, Excel, etc.

### Q: Les sections "Nom de modèle de document" sont-elles nécessaires ?
**R:** Non, ces sections font partie du chatter (système de messages d'Odoo). Elles sont masquées pour les utilisateurs normaux et visibles uniquement pour les administrateurs qui en ont besoin pour le suivi technique.

## 📝 Changelog

### Version 18.0.1.1.1 (Actuelle)
- ✅ Amélioration du responsive design (largeur max 1200px)
- ✅ Ajout de l'accès portail pour investisseurs
- ✅ Lien automatique avec res.partner
- ✅ Optimisation des vues formulaires
- ✅ Correction des erreurs CSS/JavaScript
- ✅ Masquage des sections techniques du chatter
- ✅ Documentation complète (README détaillé)

### Version 18.0.1.0.0
- ✅ Migration vers Odoo 18
- ✅ Compatibilité view type "list" (au lieu de "tree")
- ✅ Correction des références XML

### Version 1.0.0
- 🎉 Version initiale
- ✅ Gestion des investisseurs
- ✅ Investissements immobiliers
- ✅ Placements financiers
- ✅ Import Excel

## 📄 Licence

LGPL-3 - Voir le fichier LICENSE pour plus de détails.

## 👥 Auteur

**Gaoh Conseil**
- Site web : https://www.gaohconseil.com
- Email : contact@gaohconseil.com

---

*Dernière mise à jour : 24 octobre 2025*
