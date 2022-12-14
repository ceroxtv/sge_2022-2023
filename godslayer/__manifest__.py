# -*- coding: utf-8 -*-
{
    'name': "godslayer",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mundo_view.xml',
        'views/aldea_view.xml',
        'views/templo_view.xml',
        'views/dioses_view.xml',
        'views/edificio_type.xml',
        'views/edificio_view.xml',
        'views/religion_view.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/battle_view.xml',
        'demo/data.xml',
        'views/cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
