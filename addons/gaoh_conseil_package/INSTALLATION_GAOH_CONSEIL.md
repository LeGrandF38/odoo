# Guide d'Installation et d'Utilisation - Module Gaoh Conseil

## 📦 Contenu du Package

- `gaoh_conseil.zip` - Module Odoo complet
- `gaoh_conseil_import_exemple.xlsx` - Fichier Excel d'exemple pour l'import

## 🔧 Installation

### Prérequis

- Odoo 18.0 installé et fonctionnel
- Python 3.8 ou supérieur
- Accès administrateur à votre instance Odoo

### Dépendances Python

Avant d'installer le module, assurez-vous que ces bibliothèques Python sont installées :

```bash
pip install openpyxl python-dateutil
```

### Méthode 1 : Installation via l'interface Odoo (Recommandé)

1. **Décompresser le module**
   ```bash
   unzip gaoh_conseil.zip
   ```

2. **Copier dans le dossier addons**
   ```bash
   cp -r gaoh_conseil /chemin/vers/odoo/addons/
   ```

3. **Redémarrer le serveur Odoo**
   ```bash
   # Si vous utilisez systemd
   sudo systemctl restart odoo
   
   # Ou directement
   ./odoo-bin --stop
   ./odoo-bin --config=/etc/odoo/odoo.conf
   ```

4. **Activer le mode développeur**
   - Connectez-vous à Odoo
   - Allez dans Paramètres > Activer le mode développeur

5. **Mettre à jour la liste des applications**
   - Apps > Mettre à jour la liste des applications

6. **Installer le module**
   - Recherchez "Gaoh Conseil"
   - Cliquez sur "Installer"

### Méthode 2 : Installation en ligne de commande

```bash
# Décompresser
unzip gaoh_conseil.zip -d /chemin/vers/odoo/addons/

# Installer le module
./odoo-bin -c /etc/odoo/odoo.conf -d nom_de_la_base -i gaoh_conseil --stop-after-init

# Redémarrer normalement
./odoo-bin -c /etc/odoo/odoo.conf
```

## 🎯 Premier Démarrage

### 1. Accéder au module

Après installation, un nouveau menu "Gaoh Conseil" apparaît dans la barre de navigation principale.

### 2. Structure du menu

```
Gaoh Conseil
├── Investisseurs
├── Investissements
│   ├── Investissements Immobiliers
│   └── Placements Financiers
└── Configuration
    └── Import Excel
```

### 3. Configuration initiale

#### Attribution des droits

1. Allez dans **Paramètres > Utilisateurs & Entreprises > Groupes**
2. Recherchez "Gaoh Conseil"
3. Deux groupes sont disponibles :
   - **Utilisateur** : Lecture, écriture, création (pas de suppression)
   - **Manager** : Tous les droits

4. Assignez les utilisateurs aux groupes appropriés

## 📥 Import de Données

### Préparer vos fichiers Excel

Le module accepte des fichiers Excel (.xlsx) avec une structure spécifique. Utilisez le fichier `gaoh_conseil_import_exemple.xlsx` comme modèle.

### Structure des feuilles

#### Feuille "Investisseurs"

**Colonnes obligatoires :**
- Nom
- Prénom

**Colonnes optionnelles :**
- Civilité (M/Mme/Mlle)
- Date de Naissance (format: JJ/MM/AAAA)
- Email
- Téléphone Portable
- Ville
- Consultant Apporteur
- TMI
- Liquidités Seul
- Liquidités Couple
- etc.

**Format des booléens :** Oui/O/Non/N ou True/False

#### Feuille "Investissements Immobiliers"

**Colonnes obligatoires :**
- Nom complet Investisseur (doit correspondre à un investisseur existant)
- Nom Programme

**Colonnes optionnelles :**
- Email Investisseur
- Code Programme
- Ville Programme
- Promoteur
- Dispositif Fiscal (Pinel/LMNP/Malraux/etc.)
- Prix TTC
- etc.

#### Feuille "Placements Financiers"

**Colonnes obligatoires :**
- Nom complet Investisseur (doit correspondre à un investisseur existant)
- Libellé Produit

**Colonnes optionnelles :**
- Type de Produit
- Partenaire
- Numéro Contrat
- VA Encours
- etc.

### Procédure d'import

1. **Préparer le fichier Excel**
   - Utilisez le modèle fourni
   - Remplissez les données
   - Vérifiez que les en-têtes correspondent exactement

2. **Lancer l'import**
   - Allez dans **Gaoh Conseil > Configuration > Import Excel**
   - Sélectionnez le type d'import (Investisseurs/Immobilier/Placements)
   - Choisissez le fichier Excel
   - (Optionnel) Spécifiez le nom de la feuille
   - Cliquez sur "Importer"

3. **Vérifier le résultat**
   - Un rapport détaillé s'affiche
   - Nombre d'enregistrements créés
   - Nombre d'enregistrements mis à jour
   - Liste des erreurs éventuelles

### Conseils pour l'import

✅ **Bonnes pratiques :**
- Commencez par importer les investisseurs
- Puis importez les investissements (immobiliers et placements)
- Vérifiez que le "Nom complet" correspond exactement
- Utilisez des formats de date cohérents (JJ/MM/AAAA)
- Nettoyez les données (supprimez les espaces inutiles)

⚠️ **Gestion des doublons :**
- Les investisseurs sont identifiés par email OU nom+prénom
- Les investissements immobiliers par numéro de commande
- Les placements par numéro de contrat
- Si trouvé : mise à jour, sinon : création

## 📊 Utilisation Quotidienne

### Créer un investisseur

1. **Gaoh Conseil > Investisseurs > Créer**
2. Remplissez les informations :
   - Informations personnelles (nom, prénom, civilité)
   - Contact (email, téléphones)
   - Adresse complète
   - Informations fiscales
   - Liquidités
3. Cliquez sur "Enregistrer"

### Ajouter un investissement immobilier

1. **Depuis la fiche investisseur** :
   - Onglet "Investissements Immobiliers"
   - Cliquez sur "Ajouter une ligne"

2. **Ou directement** :
   - **Gaoh Conseil > Investissements > Investissements Immobiliers > Créer**
   - Sélectionnez l'investisseur
   - Remplissez les détails du programme

### Ajouter un placement

1. **Depuis la fiche investisseur** :
   - Onglet "Placements Financiers"
   - Cliquez sur "Ajouter une ligne"

2. **Ou directement** :
   - **Gaoh Conseil > Investissements > Placements Financiers > Créer**
   - Sélectionnez l'investisseur
   - Remplissez les détails du produit

### Recherche et filtres

#### Investisseurs
- Filtrer par détention (Épargne Retraite, Capinvest, Girardin)
- Grouper par consultant, ville, situation familiale

#### Investissements Immobiliers
- Filtrer par dispositif fiscal (Pinel, LMNP, etc.)
- Filtrer par état (En cours, Signée, Livrée)
- Grouper par promoteur, ville, dispositif

#### Placements
- Filtrer par âge 67-69 ans
- Filtrer par état (En vigueur, Sortie)
- Grouper par type de produit, partenaire

## 🔄 Suivi et Communication

### Activités
- Planifiez des appels, réunions, tâches
- Recevez des rappels automatiques
- Suivez l'historique des actions

### Messagerie
- Envoyez des notes internes
- Échangez avec les collègues
- Historique complet des communications

### Abonnés
- Suivez les investisseurs importants
- Recevez des notifications automatiques
- Restez informé des changements

## 🛠️ Dépannage

### Le module n'apparaît pas dans la liste

1. Vérifiez que le dossier est bien dans `addons/`
2. Redémarrez Odoo
3. Mettez à jour la liste des apps (mode développeur requis)

### Erreur lors de l'import Excel

1. Vérifiez que `openpyxl` est installé : `pip install openpyxl`
2. Vérifiez le format du fichier (.xlsx uniquement)
3. Vérifiez que les en-têtes correspondent exactement
4. Consultez le rapport d'erreur pour les détails

### Erreur "Investisseur non trouvé" lors de l'import

- L'investisseur doit exister avant d'importer ses investissements
- Vérifiez que le "Nom complet" ou l'email correspondent exactement
- Importez d'abord les investisseurs, puis leurs investissements

### Problèmes de droits d'accès

- Vérifiez que l'utilisateur est dans un groupe Gaoh Conseil
- Les managers ont tous les droits
- Les utilisateurs ne peuvent pas supprimer

## 📞 Support

Pour toute question ou problème :
- Consultez la documentation Odoo : https://www.odoo.com/documentation/18.0/
- Contactez votre administrateur système
- Email : support@gaohconseil.com

## 📝 Notes de Version

### Version 1.0.0 (Octobre 2024)
- ✨ Version initiale
- 👥 Gestion des investisseurs
- 🏢 Suivi des investissements immobiliers
- 💰 Suivi des placements financiers
- 📥 Import Excel
- 🔒 Gestion des droits (Utilisateur/Manager)

---

**Module développé pour Gaoh Conseil**  
Compatible avec Odoo 18.0  
Licence : LGPL-3
