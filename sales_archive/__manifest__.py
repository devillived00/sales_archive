{
    'name': 'Sales Archive',
    'summary': '',
    'description': '''
    
    ''',
    'author': 'Patryk Kosnik',
    'website': '',
    'category': 'Sales',
    'version': '[V15].0.1.0',
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/sale_report_action.xml',
        'views/sale_order_archive.xml',
        'wizards/sale_custom_report.xml'
    ],
    'installable': True,
    'auto_install': False
}
