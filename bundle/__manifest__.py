# -*- coding: utf-8 -*-

{
    'name': 'Prueba',
    'category': 'Technical',
    'summary': 'Bundles',
    'version': '1.0.1',
    'sequence': 50,
    'author': 'The Fish Consulting',
    'website': 'https://thefishconsulting.be',
    'images': ['static/description/bundle_components.png'],
    'description': """
        
        """,
    'depends': [
        'product',
        'stock',
        'account',
    ],
    'qweb': [],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'wizard/add_bundle_product_views.xml',
    ],
    'currency': 'EUR',
    'support': 'contact@thefishconsulting.be',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
