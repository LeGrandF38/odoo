# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvestissementImmobilier(models.Model):
    _name = 'gaoh.investissement_immobilier'
    _description = 'Investissement Immobilier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nom_programme'

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
    
    # Informations programme
    stellium_sci = fields.Selection([
        ('stellium', 'Stellium'),
        ('sci', 'SCI'),
        ('autre', 'Autre'),
    ], string='Stellium/SCI', tracking=True)
    
    code_programme = fields.Char(string='Code Programme', tracking=True)
    nom_programme = fields.Char(string='Nom Programme', required=True, tracking=True)
    ville_programme = fields.Char(string='Ville Programme', tracking=True)
    promoteur = fields.Char(string='Promoteur', tracking=True)
    gestionnaire = fields.Char(string='Gestionnaire', tracking=True)
    
    # Informations lot
    lot = fields.Char(string='Lot', tracking=True)
    type_lot = fields.Char(string='Type de Lot', tracking=True)
    
    # Dispositif fiscal
    dispositif_fiscal = fields.Selection([
        ('pinel', 'Pinel'),
        ('pinel_plus', 'Pinel Plus'),
        ('denormandie', 'Denormandie'),
        ('malraux', 'Malraux'),
        ('monuments_historiques', 'Monuments Historiques'),
        ('lmnp', 'LMNP'),
        ('deficit_foncier', 'Déficit Foncier'),
        ('autre', 'Autre'),
    ], string='Dispositif Fiscal', tracking=True)
    
    # Dates importantes
    date_option = fields.Date(string='Date Option', tracking=True)
    date_reservation = fields.Date(string='Date Réservation', tracking=True)
    date_livraison = fields.Date(string='Date Livraison', tracking=True)
    date_acte = fields.Date(string='Date Acte', tracking=True)
    
    # Informations paiement et commande
    paiement_comptant = fields.Boolean(string='Paiement Comptant', default=False, tracking=True)
    numero_commande = fields.Char(string='Numéro Commande', tracking=True)
    
    etat_commande = fields.Selection([
        ('en_cours', 'En Cours'),
        ('validee', 'Validée'),
        ('signee', 'Signée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ], string='État Commande', default='en_cours', tracking=True)
    
    date_vc = fields.Date(string='Date VC (Validation Client)', tracking=True)
    pv_strategie = fields.Char(string='PV Stratégie', tracking=True)
    achat_personnel = fields.Boolean(string='Achat Personnel', default=False, tracking=True)
    
    # Informations financières
    base_commissionnement = fields.Float(string='Base Commissionnement (€)', tracking=True)
    prix_ttc = fields.Float(string='Prix TTC (€)', tracking=True)
    
    _sql_constraints = [
        ('numero_commande_unique', 'unique(numero_commande)', 'Le numéro de commande doit être unique!')
    ]
