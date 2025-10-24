# -*- coding: utf-8 -*-
{
    'name': 'Gaoh Conseil - Gestion des Investisseurs',
    'version': '18.0.1.1.1',
    'category': 'Sales/CRM',
    'summary': 'Gestion des investisseurs, placements et investissements immobiliers',
    'description': """
Gaoh Conseil - Module de Gestion
=================================
Module de gestion des investisseurs et de leurs portefeuilles:
* Gestion des investisseurs avec informations complètes
* Suivi des investissements immobiliers
* Suivi des placements financiers
* Import de données depuis Excel
    """,
    'author': 'Gaoh Conseil',
    'website': 'https://www.gaohconseil.com',
    'depends': ['base', 'mail', 'contacts', 'portal'],
    'data': [
        'security/gaoh_security.xml',
        'security/ir.model.access.csv',
        'views/investisseur_views.xml',
        'views/investissement_immobilier_views.xml',
        'views/investissement_placement_views.xml',
        'wizards/import_excel_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gaoh_conseil/static/src/css/gaoh_conseil.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
