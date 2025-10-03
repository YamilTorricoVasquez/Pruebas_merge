{
    'name': 'Reporte Stock Picking',
    'version': '1.0',
    'summary': 'Reporte personalizado para stock picking',
    'description': 'Módulo para generar reportes personalizados de stock picking.',
    'author': 'AppexBolivia, Yamil Torrico Vasquez',
    'website': 'https://www.appexbo.com/',
    'category': 'Inventory',
    'depends': ['base','stock','reporte_nota_venta'],
    'data': [
      "views/view_stock_picking.xml"
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}