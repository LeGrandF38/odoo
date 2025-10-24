# 🔍 Guide de Débogage - Module Gaoh Conseil

## Avant de Build l'Image Docker

Toujours exécuter ces validations **avant** de build l'image Docker pour éviter les surprises !

### 1️⃣ **Validation Complète (Recommandé)**

Exécute toutes les vérifications en une seule commande :

```bash
cd addons/gaoh_conseil
python debug.py
```

**Qu'est-ce que cela vérifie ?**
- ✅ Syntaxe XML valide
- ✅ Références entre fichiers (actions, parents, etc.)
- ✅ Syntaxe Python valide
- ✅ Fichiers requis existent
- ✅ Manifest complet et cohérent

### 2️⃣ **Validation XML Seule**

Si vous avez modifié des fichiers XML :

```bash
cd addons/gaoh_conseil
python validate_xml.py
```

**Affiche:**
- Fichiers XML valides/invalides
- Tous les IDs définis
- Toutes les références (et leur statut)

### 3️⃣ **Validation Python Seule**

Si vous avez modifié du code Python :

```bash
cd addons/gaoh_conseil
python validate_python.py
```

**Affiche:**
- Fichiers Python valides/invalides
- Tous les imports détectés
- Vérification du manifest.py

---

## 🚀 Workflow Avant Build Docker

```
1. Effectuer les modifications
   ↓
2. Exécuter: python debug.py
   ↓
3. Vérifier les résultats (tous ✓ ?)
   ↓
4. Si OK → Git commit et push
   ↓
5. Si Erreur → Corriger et relancer debug.py
   ↓
6. Build Docker une fois tout validé
```

---

## 📋 Fichiers de Validation

| Fichier | Rôle |
|---------|------|
| `debug.py` | Script principal - lance toutes les validations |
| `validate_xml.py` | Valide la syntaxe et les références XML |
| `validate_python.py` | Valide la syntaxe et les imports Python |

---

## ⚠️ Erreurs Courantes et Solutions

### ❌ "External ID not found"
```
Cause: Un fichier XML référence une action/menu qui n'existe pas ou n'est pas chargé
Solution: 
  1. Vérifier que l'ID est bien défini
  2. Vérifier l'ordre dans __manifest__.py (fichier qui définit l'ID doit être chargé avant)
```

### ❌ "Wrong value for ir.ui.view.type: 'tree'"
```
Cause: Odoo 18 utilise 'list' au lieu de 'tree'
Solution: 
  1. Remplacer <tree> par <list> dans les fichiers XML
  2. Ajouter <field name="type">list</field> aux vues
```

### ❌ Erreur de syntaxe XML
```
Cause: Balises mal fermées, caractères invalides, etc.
Solution:
  1. Vérifier les balises ouvrantes/fermantes
  2. Remplacer & par &amp; dans les textes
  3. Vérifier l'encodage UTF-8
```

---

## 🎯 Après Validation Réussie

Une fois `debug.py` 100% réussi :

```bash
# Vérifier les changements
git status

# Committer
git add addons/gaoh_conseil/
git commit -m "Fix: correction erreurs module gaoh_conseil"

# Pousser
git push origin 18.0

# Maintenant, build Docker sans crainte! 
docker-compose up --build
```

---

## 💡 Tips Pro

1. **Valider après chaque modification** : N'attendez pas d'avoir modifié 10 fichiers
2. **Garder les scripts de validation** : Les réutiliser pour les futures modifications
3. **Lire les logs de débogage** : Ils indiquent exactement où est le problème
4. **Tester localement** : Si possible, tester le module dans une instance Odoo locale avant Docker

---

## 📞 Support

Si les scripts trouvent une erreur :

1. ✅ Lire le message d'erreur en détail
2. ✅ Localiser le fichier et la ligne
3. ✅ Corriger l'erreur
4. ✅ Relancer `python debug.py`
5. ✅ Répéter jusqu'à avoir tous les ✓

