# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class GaohPortal(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        """Ajouter les compteurs pour le portail"""
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        
        # Trouver l'investisseur lié au partner
        Investisseur = request.env['gaoh.investisseur']
        investisseur = Investisseur.sudo().search([('partner_id', '=', partner.id)], limit=1)
        
        if investisseur:
            if 'investissement_immobilier_count' in counters:
                values['investissement_immobilier_count'] = len(investisseur.investissement_immobilier_ids)
            if 'investissement_placement_count' in counters:
                values['investissement_placement_count'] = len(investisseur.investissement_placement_ids)
        
        return values
    
    @http.route(['/my/investisseur', '/my/investisseur/<int:investisseur_id>'], type='http', auth="user", website=True)
    def portal_my_investisseur(self, investisseur_id=None, **kw):
        """Page portail pour voir ses informations d'investisseur"""
        partner = request.env.user.partner_id
        Investisseur = request.env['gaoh.investisseur']
        
        # Trouver l'investisseur lié
        if investisseur_id:
            investisseur = Investisseur.sudo().browse(investisseur_id)
            # Vérifier que c'est bien l'investisseur du partner connecté
            if investisseur.partner_id.id != partner.id:
                return request.redirect('/my')
        else:
            investisseur = Investisseur.sudo().search([('partner_id', '=', partner.id)], limit=1)
            if not investisseur:
                return request.redirect('/my')
        
        values = {
            'investisseur': investisseur,
            'page_name': 'investisseur',
        }
        
        return request.render('gaoh_conseil.portal_my_investisseur', values)
    
    @http.route(['/my/investissements/immobilier'], type='http', auth="user", website=True)
    def portal_my_investissements_immobilier(self, **kw):
        """Page portail pour voir ses investissements immobiliers"""
        partner = request.env.user.partner_id
        Investisseur = request.env['gaoh.investisseur']
        
        investisseur = Investisseur.sudo().search([('partner_id', '=', partner.id)], limit=1)
        if not investisseur:
            return request.redirect('/my')
        
        values = {
            'investisseur': investisseur,
            'investissements': investisseur.investissement_immobilier_ids,
            'page_name': 'investissements_immobilier',
        }
        
        return request.render('gaoh_conseil.portal_my_investissements_immobilier', values)
    
    @http.route(['/my/investissements/placements'], type='http', auth="user", website=True)
    def portal_my_investissements_placement(self, **kw):
        """Page portail pour voir ses placements financiers"""
        partner = request.env.user.partner_id
        Investisseur = request.env['gaoh.investisseur']
        
        investisseur = Investisseur.sudo().search([('partner_id', '=', partner.id)], limit=1)
        if not investisseur:
            return request.redirect('/my')
        
        values = {
            'investisseur': investisseur,
            'placements': investisseur.investissement_placement_ids,
            'page_name': 'investissements_placement',
        }
        
        return request.render('gaoh_conseil.portal_my_investissements_placement', values)
