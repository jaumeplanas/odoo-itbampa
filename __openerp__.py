# -*- coding: utf-8 -*-
{
    'name': "itbampa",

    'summary': """
        Magagement of an AMPA for Catalan Public Education System""",

    'description': """
        Tutor, Student, Teacher, Board management. Fees, Lunch Vouchers, Accounting,
        Payments ...
    """,

    'author': "Infonomia Tecnica Berga, S.L.",
    'website': "http://ampa.itberga.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Association',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/itbampa_security.xml',
        'security/ir.model.access.csv',
        'view/activity_data.xml',
        'view/templates.xml',
        'view/itbampa_menu.xml',
        'view/partner_view.xml',
        'view/board_role_view.xml',
        'view/board_view.xml',
        'workflow/board_wkf.xml',
        'view/school_calendar_view.xml',
        'view/activity_quick_select_wizard_view.xml',
        'view/activity_type_view.xml',
        'view/activity_partner_view.xml',
        'view/activity_report_wizard_view.xml',
        'view/activity_daily_report_view.xml',
        'view/activity_view.xml',
        'workflow/activity_event_wkf.xml',
        'view/product_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
