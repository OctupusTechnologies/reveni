{
    'name': 'RMA Reveni',
    'version': '15.0.0.0.0',
    'summary': 'RMA Reveni',
    'description': 'RMA Reveni',
    'category': '',
    'author': 'Octupus Technologies',
    'website': 'http://www.octupus.es',
    'license': 'AGPL-3',
    # TODO add dependencies of RMA module and Channel module( shopify, magento, prestashop)
    'depends': ['base', 'sale'],
    'data': ['views/res_config.xml',
             'data/data.xml',
             'views/reveni_event.xml',
             'security/ir.model.access.csv'],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #     'python': [''],
    # }
}
