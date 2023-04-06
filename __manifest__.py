{
    'name': 'Linha Fala Crianca Agent App',
    'summary': 'Aplicativo de agente da Linha Fala Crianca',
    'version': '1.0',
    'category': 'Web',
    'description': """
        Aplicativo de agente da Linha Fala Crianca. A ser usado por agentes e outros intervinientes relevantes.
    """,
    'author': "team@robobo.org",
    "website": "www.robobo.org",
    'data': [
        'views/linhafala_menus.xml',
        'views/linhafala_calls_views.xml',
        'views/linhafala_cases_views.xml',
        'views/linhafala_case_form_view.xml',
        'views/linhafala_configurations_views.xml',
        'security/ir.model.access.csv',
        'data/linhafala.provincia.csv',
        'data/linhafala.distrito.csv',
        'data/linhafala.categoria.csv',
        'data/linhafala.subcategoria.csv',
        'data/linhafala.caso.categoria.csv',
        'data/linhafala.caso.subcategoria.csv',
        'data/linhafala.caso.case_type_classification.csv',
        'data/linhafala.caso.referencearea.csv',
        'data/linhafala.chamada.assistance.categoria.csv',
        'data/linhafala.chamada.assistance.subcategoria.csv',
    ],
    'assets': {
    },
    'depends': [
        'mail'
    ],
    'images': ['static/src/img/icon_module.png'],
    'price': 0,
    'price_comparison': {'standard': 0},
    'license': 'OPL-1',
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': [
        'static/src/img/overview.png',
    ],
}
