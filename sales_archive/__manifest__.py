{
    'name': 'Sales Archive',
    'summary': '',
    'description': '''
    
    ''',
    'author': 'Patryk Kosnik',
    'website': '',
    'category': 'Sales',
    'version': '[V15].0.0.2',
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/sale_order_archive.xml'
    ],
    'installable': True,
    'auto_install': False
}
