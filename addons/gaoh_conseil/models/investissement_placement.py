# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class InvestissementPlacement(models.Model):
    _name = 'gaoh.investissement_placement'
    _description = 'Investissement Placement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'libelle_produit'

    # Relation avec investisseur
    investisseur_id = fields.Many2one(
        'gaoh.investisseur',
        string='Investisseur',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    email_investisseur = fields.Char(
        string='Email Investisseur',
        related='investisseur_id.email',
        store=True
    )
    
    # Informations consultant
    consultant_apporteur = fields.Char(string='Consultant Apporteur', tracking=True)
    
    # Informations investisseur liées
    age_67_69 = fields.Boolean(
        string='Âge entre 67 et 69 ans',
        compute='_compute_age_67_69',
        store=True
    )
    tmi = fields.Float(
        string='TMI (%)',
        related='investisseur_id.tmi',
        store=True
    )
    
    # Informations produit
    type_produit = fields.Char(string='Type de Produit', tracking=True)
    partenaire = fields.Char(string='Partenaire', tracking=True)
    libelle_produit = fields.Char(string='Libellé Produit', required=True, tracking=True)
    numero_contrat = fields.Char(string='Numéro Contrat', tracking=True)
    
    # Dates
    date_effet = fields.Date(string='Date Effet', tracking=True)
    date_sortie = fields.Date(string='Date Sortie', tracking=True)
    
    # Programmation versement
    programmation_versement = fields.Char(string='Programmation Versement', tracking=True)
    programmation_date_debut = fields.Date(string='Programmation Date Début', tracking=True)
    programmation_date_fin = fields.Date(string='Programmation Date Fin', tracking=True)
    programmation_montant = fields.Float(string='Programmation Montant (€)', tracking=True)
    
    # Dernier mouvement VC
    dernier_mouvement_vc_date = fields.Date(string='Dernier Mouvement VC - Date', tracking=True)
    dernier_mouvement_vc_type = fields.Selection([
        ('versement', 'Versement'),
        ('rachat', 'Rachat'),
        ('arbitrage', 'Arbitrage'),
        ('autre', 'Autre'),
    ], string='Dernier Mouvement VC - Type', tracking=True)
    dernier_mouvement_vc_montant = fields.Float(string='Dernier Mouvement VC - Montant (€)', tracking=True)
    
    # Commande
    numero_commande = fields.Char(string='Numéro Commande', tracking=True)
    achat_personnel = fields.Boolean(string='Achat Personnel', default=False, tracking=True)
    etat_commande = fields.Selection([
        ('en_cours', 'En Cours'),
        ('validee', 'Validée'),
        ('signee', 'Signée'),
        ('en_vigueur', 'En Vigueur'),
        ('sortie', 'Sortie'),
        ('annulee', 'Annulée'),
    ], string='État Commande', default='en_cours', tracking=True)
    
    # Ancienneté
    anciennete_mois = fields.Integer(
        string='Ancienneté (mois)',
        compute='_compute_anciennete_mois',
        store=True
    )
    
    # Montants cumulés
    montant_versement_cumule = fields.Float(string='Montant Versement Cumulé (€)', tracking=True)
    va_vc_cumule = fields.Float(string='VA VC Cumulé (€)', tracking=True)
    va_vc_exercice = fields.Float(string='VA VC Exercice (€)', tracking=True)
    
    # Versements exercice
    versement_initial_ex = fields.Float(string='Versement Initial Exercice (€)', tracking=True)
    versement_complementaire_ex = fields.Float(string='Versement Complémentaire Exercice (€)', tracking=True)
    versement_programme_ex = fields.Float(string='Versement Programmé Exercice (€)', tracking=True)
    
    # Encours
    va_encours = fields.Float(string='VA Encours (€)', tracking=True)
    versement_initial_encours = fields.Float(string='Versement Initial Encours (€)', tracking=True)
    versement_complementaire_encours = fields.Float(string='Versement Complémentaire Encours (€)', tracking=True)
    versement_programme_encours = fields.Float(string='Versement Programmé Encours (€)', tracking=True)
    
    @api.depends('investisseur_id.age')
    def _compute_age_67_69(self):
        for record in self:
            if record.investisseur_id and record.investisseur_id.age:
                age = record.investisseur_id.age
                record.age_67_69 = 67 <= age <= 69
            else:
                record.age_67_69 = False
    
    @api.depends('date_effet')
    def _compute_anciennete_mois(self):
        for record in self:
            if record.date_effet:
                delta = relativedelta(fields.Date.today(), record.date_effet)
                record.anciennete_mois = delta.years * 12 + delta.months
            else:
                record.anciennete_mois = 0
    
    _sql_constraints = [
        ('numero_contrat_unique', 'unique(numero_contrat)', 'Le numéro de contrat doit être unique!')
    ]
