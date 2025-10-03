# -*- coding:utf-8 -*-
{
    'name': 'Reporte nota de venta v18',
    'version': '1.0',
    'depends': [
        'base', 
        'sale',
    ],
    'author': 'APPEX BOLIVIA SRL.',
    'summary': 'Reporte nota de venta v18',
    'data': [
      #Nota de venta
      'reports/formato_papel.xml',
      'reports/boton_imprimir_pdf_nota_venta.xml',
      'reports/cabecera_pdf_nota_venta.xml',
      'reports/cuerpo_pdf_nota_venta.xml',
      'views/campo_adicional.xml',
    ],
    'installable': True,
    'license': 'OPL-1',
}