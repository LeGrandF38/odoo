# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import io
import logging

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except ImportError:
    _logger.warning("openpyxl not installed. Excel import will not work.")


class ImportExcelWizard(models.TransientModel):
    _name = 'gaoh.import_excel_wizard'
    _description = 'Assistant Import Excel'

    file = fields.Binary(string='Fichier Excel', required=True)
    filename = fields.Char(string='Nom du fichier')
    import_type = fields.Selection([
        ('investisseur', 'Investisseurs'),
        ('immobilier', 'Investissements Immobiliers'),
        ('placement', 'Placements Financiers'),
    ], string='Type d\'import', required=True, default='investisseur')
    
    sheet_name = fields.Char(string='Nom de la feuille', help='Laisser vide pour utiliser la première feuille')
    
    result_message = fields.Html(string='Résultat', readonly=True)

    def _parse_boolean(self, value):
        """Convertit différents formats en booléen"""
        if isinstance(value, bool):
            return value
        if not value:
            return False
        if isinstance(value, str):
            value = value.strip().upper()
            return value in ['OUI', 'O', 'YES', 'Y', 'TRUE', '1', 'VRAI']
        return bool(value)

    def _parse_float(self, value):
        """Convertit une valeur en float"""
        if not value:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Enlever les espaces et remplacer la virgule par un point
            value = value.strip().replace(' ', '').replace(',', '.')
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0

    def _parse_date(self, value):
        """Convertit une valeur en date"""
        if not value:
            return False
        if isinstance(value, str):
            # Essayer de parser différents formats de date
            from datetime import datetime
            for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y']:
                try:
                    return datetime.strptime(value.strip(), fmt).date()
                except ValueError:
                    continue
        return value if hasattr(value, 'year') else False

    def _get_or_create_country(self, country_name):
        """Récupère ou crée un pays"""
        if not country_name:
            return False
        country = self.env['res.country'].search([('name', 'ilike', country_name)], limit=1)
        return country.id if country else False

    def _get_or_create_investisseur(self, nom_complet, email):
        """Recherche un investisseur par nom complet ou email"""
        if not nom_complet:
            return False
        
        domain = []
        if email:
            domain.append(('email', '=', email))
        if nom_complet:
            domain.append(('nom_complet', '=', nom_complet))
        
        if domain:
            investisseur = self.env['gaoh.investisseur'].search(domain, limit=1)
            return investisseur.id if investisseur else False
        return False

    def import_investisseurs(self, sheet):
        """Importe les investisseurs depuis la feuille Excel"""
        created = 0
        updated = 0
        errors = []
        
        # Lire l'en-tête
        headers = [cell.value for cell in sheet[1]]
        
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                data = dict(zip(headers, row))
                
                # Préparer les données
                vals = {
                    'civilite': data.get('Civilité', '').lower() if data.get('Civilité') else False,
                    'nom': data.get('Nom', ''),
                    'prenom': data.get('Prénom', ''),
                    'nom_jeune_fille': data.get('Nom de Jeune Fille', ''),
                    'date_naissance': self._parse_date(data.get('Date de Naissance')),
                    'situation_familiale': data.get('Situation Familiale', '').lower().replace('é', 'e').replace(' ', '_') if data.get('Situation Familiale') else False,
                    'interlocuteur_principal': data.get('Interlocuteur Principal', ''),
                    'npai': self._parse_boolean(data.get('NPAI')),
                    'adresse_ligne1': data.get('Adresse Ligne 1', ''),
                    'adresse_ligne2': data.get('Adresse Ligne 2', ''),
                    'rue': data.get('Rue', ''),
                    'code_postal': data.get('Code Postal', ''),
                    'ville': data.get('Ville', ''),
                    'pays_id': self._get_or_create_country(data.get('Pays')),
                    'email': data.get('Email', ''),
                    'telephone_portable': data.get('Téléphone Portable', ''),
                    'telephone_domicile': data.get('Téléphone Domicile', ''),
                    'telephone_professionnel': data.get('Téléphone Professionnel', ''),
                    'autorisation_communication': self._parse_boolean(data.get('Autorisation Communication')),
                    'consultant_precedent': data.get('Consultant Précédent', ''),
                    'date_rattachement_precedent': self._parse_date(data.get('Date Rattachement Précédent')),
                    'consultant_apporteur': data.get('Consultant Apporteur', ''),
                    'date_derniere_signature': self._parse_date(data.get('Date Dernière Signature')),
                    'date_suppression_contact': self._parse_date(data.get('Date Suppression Contact')),
                    'detenteur_epargne_retraite': self._parse_boolean(data.get('Détenteur Épargne Retraite')),
                    'detenteur_capinvest': self._parse_boolean(data.get('Détenteur Capinvest')),
                    'detenteur_girardin': self._parse_boolean(data.get('Détenteur Girardin')),
                    'impot_revenu_brut': self._parse_float(data.get('Impôt Revenu Brut')),
                    'impot_revenu_net': self._parse_float(data.get('Impôt Revenu Net')),
                    'tmi': self._parse_float(data.get('TMI')),
                    'liquidites_seul': self._parse_float(data.get('Liquidités Seul')),
                    'liquidites_couple': self._parse_float(data.get('Liquidités Couple')),
                    'date_credit_recent': self._parse_date(data.get('Date Crédit Récent')),
                    'date_credit_futur': self._parse_date(data.get('Date Crédit Futur')),
                }
                
                # Rechercher si l'investisseur existe déjà
                existing = self.env['gaoh.investisseur'].search([
                    '|',
                    ('email', '=', vals['email']),
                    '&',
                    ('nom', '=', vals['nom']),
                    ('prenom', '=', vals['prenom'])
                ], limit=1)
                
                if existing:
                    existing.write(vals)
                    updated += 1
                else:
                    self.env['gaoh.investisseur'].create(vals)
                    created += 1
                    
            except Exception as e:
                errors.append(f"Ligne {row_idx}: {str(e)}")
                _logger.error(f"Erreur import ligne {row_idx}: {str(e)}")
        
        return created, updated, errors

    def import_investissements_immobiliers(self, sheet):
        """Importe les investissements immobiliers depuis la feuille Excel"""
        created = 0
        updated = 0
        errors = []
        
        headers = [cell.value for cell in sheet[1]]
        
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                data = dict(zip(headers, row))
                
                # Trouver l'investisseur
                investisseur_id = self._get_or_create_investisseur(
                    data.get('Nom complet Investisseur'),
                    data.get('Email Investisseur')
                )
                
                if not investisseur_id:
                    errors.append(f"Ligne {row_idx}: Investisseur non trouvé")
                    continue
                
                vals = {
                    'investisseur_id': investisseur_id,
                    'consultant_apporteur': data.get('Consultant Apporteur', ''),
                    'stellium_sci': data.get('Stellium/SCI', '').lower() if data.get('Stellium/SCI') else False,
                    'code_programme': data.get('Code Programme', ''),
                    'nom_programme': data.get('Nom Programme', ''),
                    'ville_programme': data.get('Ville Programme', ''),
                    'promoteur': data.get('Promoteur', ''),
                    'gestionnaire': data.get('Gestionnaire', ''),
                    'lot': data.get('Lot', ''),
                    'type_lot': data.get('Type de Lot', ''),
                    'dispositif_fiscal': data.get('Dispositif Fiscal', '').lower().replace(' ', '_').replace('+', '_plus') if data.get('Dispositif Fiscal') else False,
                    'date_option': self._parse_date(data.get('Date Option')),
                    'date_reservation': self._parse_date(data.get('Date Réservation')),
                    'date_livraison': self._parse_date(data.get('Date Livraison')),
                    'date_acte': self._parse_date(data.get('Date Acte')),
                    'paiement_comptant': self._parse_boolean(data.get('Paiement Comptant')),
                    'numero_commande': data.get('Numéro Commande', ''),
                    'etat_commande': data.get('État Commande', '').lower().replace('é', 'e').replace(' ', '_') if data.get('État Commande') else 'en_cours',
                    'date_vc': self._parse_date(data.get('Date VC')),
                    'pv_strategie': data.get('PV Stratégie', ''),
                    'achat_personnel': self._parse_boolean(data.get('Achat Personnel')),
                    'base_commissionnement': self._parse_float(data.get('Base Commissionnement')),
                    'prix_ttc': self._parse_float(data.get('Prix TTC')),
                }
                
                # Rechercher si existe déjà
                existing = False
                if vals.get('numero_commande'):
                    existing = self.env['gaoh.investissement_immobilier'].search([
                        ('numero_commande', '=', vals['numero_commande'])
                    ], limit=1)
                
                if existing:
                    existing.write(vals)
                    updated += 1
                else:
                    self.env['gaoh.investissement_immobilier'].create(vals)
                    created += 1
                    
            except Exception as e:
                errors.append(f"Ligne {row_idx}: {str(e)}")
                _logger.error(f"Erreur import ligne {row_idx}: {str(e)}")
        
        return created, updated, errors

    def import_investissements_placements(self, sheet):
        """Importe les placements depuis la feuille Excel"""
        created = 0
        updated = 0
        errors = []
        
        headers = [cell.value for cell in sheet[1]]
        
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                data = dict(zip(headers, row))
                
                # Trouver l'investisseur
                investisseur_id = self._get_or_create_investisseur(
                    data.get('Nom complet Investisseur'),
                    data.get('Email Investisseur')
                )
                
                if not investisseur_id:
                    errors.append(f"Ligne {row_idx}: Investisseur non trouvé")
                    continue
                
                vals = {
                    'investisseur_id': investisseur_id,
                    'consultant_apporteur': data.get('Consultant Apporteur', ''),
                    'type_produit': data.get('Type de Produit', ''),
                    'partenaire': data.get('Partenaire', ''),
                    'libelle_produit': data.get('Libellé Produit', ''),
                    'numero_contrat': data.get('Numéro Contrat', ''),
                    'date_effet': self._parse_date(data.get('Date Effet')),
                    'date_sortie': self._parse_date(data.get('Date Sortie')),
                    'programmation_versement': data.get('Programmation Versement', ''),
                    'programmation_date_debut': self._parse_date(data.get('Programmation Date Début')),
                    'programmation_date_fin': self._parse_date(data.get('Programmation Date Fin')),
                    'programmation_montant': self._parse_float(data.get('Programmation Montant')),
                    'dernier_mouvement_vc_date': self._parse_date(data.get('Dernier Mouvement VC - Date')),
                    'dernier_mouvement_vc_type': data.get('Dernier Mouvement VC - Type', '').lower() if data.get('Dernier Mouvement VC - Type') else False,
                    'dernier_mouvement_vc_montant': self._parse_float(data.get('Dernier Mouvement VC - Montant')),
                    'numero_commande': data.get('Numéro Commande', ''),
                    'achat_personnel': self._parse_boolean(data.get('Achat Personnel')),
                    'etat_commande': data.get('État Commande', '').lower().replace('é', 'e').replace(' ', '_') if data.get('État Commande') else 'en_cours',
                    'montant_versement_cumule': self._parse_float(data.get('Montant Versement Cumulé')),
                    'va_vc_cumule': self._parse_float(data.get('VA VC Cumulé')),
                    'va_vc_exercice': self._parse_float(data.get('VA VC Exercice')),
                    'versement_initial_ex': self._parse_float(data.get('Versement Initial Exercice')),
                    'versement_complementaire_ex': self._parse_float(data.get('Versement Complémentaire Exercice')),
                    'versement_programme_ex': self._parse_float(data.get('Versement Programmé Exercice')),
                    'va_encours': self._parse_float(data.get('VA Encours')),
                    'versement_initial_encours': self._parse_float(data.get('Versement Initial Encours')),
                    'versement_complementaire_encours': self._parse_float(data.get('Versement Complémentaire Encours')),
                    'versement_programme_encours': self._parse_float(data.get('Versement Programmé Encours')),
                }
                
                # Rechercher si existe déjà
                existing = False
                if vals.get('numero_contrat'):
                    existing = self.env['gaoh.investissement_placement'].search([
                        ('numero_contrat', '=', vals['numero_contrat'])
                    ], limit=1)
                
                if existing:
                    existing.write(vals)
                    updated += 1
                else:
                    self.env['gaoh.investissement_placement'].create(vals)
                    created += 1
                    
            except Exception as e:
                errors.append(f"Ligne {row_idx}: {str(e)}")
                _logger.error(f"Erreur import ligne {row_idx}: {str(e)}")
        
        return created, updated, errors

    def action_import(self):
        """Lance l'import"""
        self.ensure_one()
        
        try:
            import openpyxl
        except ImportError:
            raise UserError("La bibliothèque 'openpyxl' n'est pas installée. Veuillez l'installer avec: pip install openpyxl")
        
        if not self.file:
            raise UserError("Veuillez sélectionner un fichier Excel.")
        
        # Décoder le fichier
        file_data = base64.b64decode(self.file)
        workbook = openpyxl.load_workbook(io.BytesIO(file_data))
        
        # Sélectionner la feuille
        if self.sheet_name:
            if self.sheet_name not in workbook.sheetnames:
                raise UserError(f"La feuille '{self.sheet_name}' n'existe pas dans le fichier.")
            sheet = workbook[self.sheet_name]
        else:
            sheet = workbook.active
        
        # Import selon le type
        if self.import_type == 'investisseur':
            created, updated, errors = self.import_investisseurs(sheet)
        elif self.import_type == 'immobilier':
            created, updated, errors = self.import_investissements_immobiliers(sheet)
        elif self.import_type == 'placement':
            created, updated, errors = self.import_investissements_placements(sheet)
        else:
            raise UserError("Type d'import non valide.")
        
        # Préparer le message de résultat
        message = f"""
        <h3>Résultat de l'import</h3>
        <ul>
            <li><strong>Créés:</strong> {created}</li>
            <li><strong>Mis à jour:</strong> {updated}</li>
            <li><strong>Erreurs:</strong> {len(errors)}</li>
        </ul>
        """
        
        if errors:
            message += "<h4>Détail des erreurs:</h4><ul>"
            for error in errors[:50]:  # Limiter à 50 erreurs
                message += f"<li>{error}</li>"
            if len(errors) > 50:
                message += f"<li>... et {len(errors) - 50} autres erreurs</li>"
            message += "</ul>"
        
        self.result_message = message
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gaoh.import_excel_wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }
