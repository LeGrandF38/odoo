# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class Investisseur(models.Model):
    _name = 'gaoh.investisseur'
    _description = 'Investisseur'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nom_complet'

    # Champ actif pour archivage
    active = fields.Boolean(string='Actif', default=True, tracking=True)

    # Informations personnelles
    nom_complet = fields.Char(
        string='Nom Complet',
        compute='_compute_nom_complet',
        store=True,
        tracking=True
    )
    civilite = fields.Selection([
        ('m', 'Monsieur'),
        ('mme', 'Madame'),
        ('mlle', 'Mademoiselle'),
    ], string='Civilité', tracking=True)
    
    nom = fields.Char(string='Nom', required=True, tracking=True)
    prenom = fields.Char(string='Prénom', tracking=True)
    nom_jeune_fille = fields.Char(string='Nom de Jeune Fille', tracking=True)
    
    date_naissance = fields.Date(string='Date de Naissance', tracking=True)
    age = fields.Integer(
        string='Âge',
        compute='_compute_age',
        store=True
    )
    
    situation_familiale = fields.Selection([
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('pacse', 'Pacsé(e)'),
        ('divorce', 'Divorcé(e)'),
        ('veuf', 'Veuf(ve)'),
        ('concubinage', 'Concubinage'),
    ], string='Situation Familiale', tracking=True)
    
    interlocuteur_principal = fields.Char(string='Interlocuteur Principal', tracking=True)
    npai = fields.Boolean(string='NPAI (N\'habite Pas à l\'Adresse Indiquée)', default=False, tracking=True)
    
    # Adresse
    adresse_ligne1 = fields.Char(string='Adresse Ligne 1 (N° appt, étage)', tracking=True)
    adresse_ligne2 = fields.Char(string='Adresse Ligne 2 (Entrée, bâtiment)', tracking=True)
    rue = fields.Char(string='Rue', tracking=True)
    code_postal = fields.Char(string='Code Postal', tracking=True)
    ville = fields.Char(string='Ville', tracking=True)
    pays_id = fields.Many2one('res.country', string='Pays', tracking=True)
    
    # Contact
    email = fields.Char(string='Email', tracking=True)
    telephone_portable = fields.Char(string='Téléphone Portable', tracking=True)
    telephone_domicile = fields.Char(string='Téléphone Domicile', tracking=True)
    telephone_professionnel = fields.Char(string='Téléphone Professionnel', tracking=True)
    autorisation_communication = fields.Boolean(
        string='Autorisation de Communication',
        default=True,
        tracking=True
    )
    
    # Informations consultant
    consultant_precedent = fields.Char(string='Consultant Précédent', tracking=True)
    date_rattachement_precedent = fields.Date(string='Date Rattachement Précédent', tracking=True)
    consultant_apporteur = fields.Char(string='Consultant Apporteur', tracking=True)
    date_derniere_signature = fields.Date(string='Date Dernière Signature', tracking=True)
    date_suppression_contact = fields.Date(string='Date Suppression Contact', tracking=True)
    
    # Détentions
    detenteur_epargne_retraite = fields.Boolean(string='Détenteur Épargne Retraite', default=False, tracking=True)
    detenteur_capinvest = fields.Boolean(string='Détenteur Capinvest', default=False, tracking=True)
    detenteur_girardin = fields.Boolean(string='Détenteur Girardin', default=False, tracking=True)
    
    # Informations fiscales et financières
    impot_revenu_brut = fields.Float(string='Impôt Revenu Brut (€)', tracking=True)
    impot_revenu_net = fields.Float(string='Impôt Revenu Net (€)', tracking=True)
    tmi = fields.Float(string='TMI (Tranche Marginale d\'Imposition) %', tracking=True)
    
    liquidites_seul = fields.Float(string='Liquidités Seul (€)', tracking=True)
    liquidites_couple = fields.Float(string='Liquidités Couple (€)', tracking=True)
    liquidites_total = fields.Float(
        string='Liquidités Total (€)',
        compute='_compute_liquidites_total',
        store=True
    )
    
    # Crédits
    date_credit_recent = fields.Date(string='Date Crédit Récent', tracking=True)
    date_credit_futur = fields.Date(string='Date Crédit Futur', tracking=True)
    
    # Relations
    investissement_immobilier_ids = fields.One2many(
        'gaoh.investissement_immobilier',
        'investisseur_id',
        string='Investissements Immobiliers'
    )
    investissement_placement_ids = fields.One2many(
        'gaoh.investissement_placement',
        'investisseur_id',
        string='Investissements Placements'
    )
    
    # Compteurs
    nb_investissements_immobiliers = fields.Integer(
        string='Nb Investissements Immobiliers',
        compute='_compute_nb_investissements'
    )
    nb_investissements_placements = fields.Integer(
        string='Nb Investissements Placements',
        compute='_compute_nb_investissements'
    )
    
    @api.depends('nom', 'prenom')
    def _compute_nom_complet(self):
        for record in self:
            if record.prenom and record.nom:
                record.nom_complet = f"{record.prenom} {record.nom}"
            elif record.nom:
                record.nom_complet = record.nom
            else:
                record.nom_complet = ''
    
    @api.depends('date_naissance')
    def _compute_age(self):
        for record in self:
            if record.date_naissance:
                today = date.today()
                record.age = today.year - record.date_naissance.year - (
                    (today.month, today.day) < (record.date_naissance.month, record.date_naissance.day)
                )
            else:
                record.age = 0
    
    @api.depends('liquidites_seul', 'liquidites_couple')
    def _compute_liquidites_total(self):
        for record in self:
            record.liquidites_total = record.liquidites_seul + record.liquidites_couple
    
    @api.depends('investissement_immobilier_ids', 'investissement_placement_ids')
    def _compute_nb_investissements(self):
        for record in self:
            record.nb_investissements_immobiliers = len(record.investissement_immobilier_ids)
            record.nb_investissements_placements = len(record.investissement_placement_ids)
