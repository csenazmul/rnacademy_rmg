{
    'name': "RMG Base",
    'version': '19.0.1.1.0',

    'summary': "Bangladesh RMG Factory ERP - Base Module",

    'description': """
Long description of module's purpose
    """,

    'author': "RN Academy",
    'website': "https://www.rnacademy.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/rmg_security_groups.xml',
        'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/rmg_buyer_views.xml',
        'views/rmg_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

