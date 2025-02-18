# -*- coding: utf-8 -*-
{
    'name': "jt_sales_invoice",


    'summary': "Sale order invoice overruling",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '18.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale', 'sale_stock'],

    # always loaded
    'data': [
        'views/sale_order_views.xml',
    ],
}
