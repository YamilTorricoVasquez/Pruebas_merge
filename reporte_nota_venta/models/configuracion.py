from odoo import models, fields, api
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from num2words import num2words
from datetime import datetime

import re


import logging
_logger = logging.getLogger(__name__)




# class Configuracion(models.Model):
#     _inherit = 'account.move'


#     terms_and_conditions = fields.Text('Términos y condiciones')  # Aquí agregamos el campo
#     razon_social_micelaneo_id = fields.Many2one( comodel_name='res.partner', string='Razón Social', store=True)
#     def number_to_word(self, number: float):
#         decimal_part = int(round(number % 1, 2) * 100)
#         integer_part = int(number)
#         # get actual language
#         lang = self.env.context.get('lang', 'es_ES')
#         return f"{num2words(integer_part, lang=lang)} con {decimal_part}/100 {self.currency_id.symbol}"
#     codigo_A1_or_A2 = fields.Char(
#         string='Código A1 o A2',
#         compute='_compute_codigo_fiscal',
#         store=False
#     )

#     @api.depends('company_id.company_registry')
#     def _compute_codigo_fiscal(self):
#         for record in self:
#             if record.company_id.company_registry == '100':
#                 record.codigo_A1_or_A2 = "A1"
#             elif record.company_id.company_registry == '200':
#                 record.codigo_A1_or_A2 = "A2"
#             else:
#                 record.codigo_A1_or_A2 = ""


#     mes_secuencia = fields.Char(string="Secuencia por Mes", compute='_compute_mes_secuencia', store=True)

#     @api.depends('date', 'journal_id', 'journal_id.type')
#     def _compute_mes_secuencia(self):
#         for record in self:
#             if record.date and record.journal_id and record.journal_id.type:
#                 # Extraer el mes en formato 'MM' (ej. '03' para marzo)
#                 mes = record.date.strftime('%m')
#                 # Definir el rango del mes actual
#                 start_of_month = record.date.replace(day=1)
#                 end_of_month = start_of_month + relativedelta(months=1)

#                 # Dominio para contar movimientos en el mismo mes y tipo de diario
#                 domain = [
#                     ('date', '>=', start_of_month),
#                     ('date', '<', end_of_month),
#                     ('journal_id.type', '=', record.journal_id.type),  # Filtrar por tipo de diario
#                 ]
#                 # Excluir el registro actual si ya existe
#                 if record.id:
#                     domain.append(('id', '!=', record.id))

#                 # Contar los movimientos previos en este mes y tipo de diario, y sumar 1
#                 ultimo_numero = self.env['account.move'].search_count(domain) + 1
#                 secuencial = f"{ultimo_numero:05d}"  # Formato '00001', '00002', etc.
#                 record.mes_secuencia = f"-{mes}-{secuencial}"
#             else:
#                 record.mes_secuencia = ''

#     @api.model
#     def create(self, vals):
#         record = super(Configuracion, self).create(vals)
#         record._compute_mes_secuencia()  # Asegurar que se calcule al crear
#         return record


class ResCompany(models.Model):
    _inherit = 'sale.order'

    phone_new = fields.Char(
        string='phone_new',
        store=True,
        compute="eliminar_codigo_pais"
    )

    def eliminar_codigo_pais(self):
        for order in self:
            phone = order.partner_id.phone or order.partner_id.mobile or ''
            # Elimina el código de país al inicio, como +591, +1, +44, etc.
            phone_clean = re.sub(r'^\+\d+\s*', '', phone)
            order.phone_new = phone_clean.strip()

    mes_secuencia = fields.Char(
        string="Secuencia por Mes",
        compute='_compute_mes_secuencia',
        store=True,
        copy=False
    )

    def number_to_word(self, number: float):
        decimal_part = int(round(number % 1, 2) * 100)
        integer_part = int(number)
        # obtener el idioma actual
        lang = self.env.context.get('lang', 'es_ES')
        return f"{num2words(integer_part, lang=lang)} con {decimal_part}/100 {self.currency_id.symbol}"

    def amount_to_text(self, amount):
        # Usar num2words para convertir el monto en número a texto
        return num2words(amount, lang='es')

    @api.depends('date_order')
    def _compute_mes_secuencia(self):
        for record in self:
            if record.date_order:
                # Convertir a fecha para evitar errores por hora
                fecha = record.date_order.date()
                mes = fecha.strftime('%m')
                start_of_month = fecha.replace(day=1)
                end_of_month = (start_of_month + relativedelta(months=1))

                domain = [
                    ('date_order', '>=', datetime.combine(
                        start_of_month, datetime.min.time())),
                    ('date_order', '<', datetime.combine(
                        end_of_month, datetime.min.time())),
                ]
                if record.id:
                    domain.append(('id', '!=', record.id))

                count = self.env['sale.order'].search_count(domain) + 1
                secuencia = f"{count:05d}"
                record.mes_secuencia = f"-{mes}-{secuencia}"
            else:
                record.mes_secuencia = ''
    
    # @api.model
    # def create(self, vals):
    #     record = super().create(vals)
    #     record._compute_mes_secuencia()  # Asegurar que se calcule al crear
    #     return record
    def action_confirm(self):
        res = super().action_confirm()
        for record in self:
            record._compute_mes_secuencia()
        return res
    # def button_validate(self):
    #     res = super().button_validate()
    #     # Solo ejecutar si estamos en el modelo sale.order
    #     if self._name == 'sale.order':
    #         for record in self:
    #             record._compute_mes_secuencia()
    #     return res

    codigo_A1_or_A2 = fields.Char(
        string='Código A1 o A2',
        compute='_compute_codigo_fiscal',
        store=False
    )

    @api.depends('company_id.is_fiscal_or_interna')
    def _compute_codigo_fiscal(self):
        for record in self:
            if record.company_id.is_fiscal_or_interna == '1':
                record.codigo_A1_or_A2 = "A1"
            elif record.company_id.is_fiscal_or_interna == '2':
                record.codigo_A1_or_A2 = "A2"
            else:
                record.codigo_A1_or_A2 = ""


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_fiscal_or_interna = fields.Selection(
        [('1', 'Fiscal'), ('2', 'Interna')], string='Tipo de Cotización',  store=True, required=True)




class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mes_secuencia = fields.Char(
        string='Secuencia Mensual', store=True, copy=False)


    def obtener_campo(self):
        for record in self:
            # Acceder al modelo sale.order
            sale_order_obj = self.env['sale.order']
            
            # Buscar la orden de venta relacionada
            domain = [('procurement_group_id', '=', record.group_id.id)]
            sale_order = sale_order_obj.search(domain, limit=1)
            if sale_order:
                record.mes_secuencia = sale_order.mes_secuencia
            # if sale_order:
            #     _logger.info("=== Datos de Sale Order ===")
            #     _logger.info(f"Nombre: {sale_order.name}")
            #     _logger.info(f"Fecha: {sale_order.date_order}")
            #     _logger.info(f"Total: {sale_order.amount_total}")
                
            #     # Si necesitas el mes_secuencia del PICKING actual
            #     _logger.info(f"Mes Secuencia del Picking: {record.mes_secuencia}")
            # else:
            #     _logger.warning("No se encontró sale order relacionada")

    def button_validate(self):
        res = super().button_validate()
        for record in self:
            record.obtener_campo()
        return res


    # @api.depends('scheduled_date')
    # def _compute_mes_secuencia(self):
    #     for record in self:
    #         if record.scheduled_date:
    #             # Convertir a fecha para evitar errores por hora
    #             fecha = record.scheduled_date.date() if isinstance(
    #                 record.scheduled_date, datetime) else record.scheduled_date
    #             mes = fecha.strftime('%m')
    #             start_of_month = fecha.replace(day=1)
    #             end_of_month = (start_of_month + relativedelta(months=1))

    #             domain = [
    #                 ('scheduled_date', '>=', datetime.combine(
    #                     start_of_month, datetime.min.time())),
    #                 ('scheduled_date', '<', datetime.combine(
    #                     end_of_month, datetime.min.time())),
    #                 ('state', 'in', ['done']),
    #             ]
    #             if record.id:
    #                 domain.append(('id', '!=', record.id))

    #             count = self.env['stock.picking'].search_count(domain) + 1
    #             secuencia = f"{count:05d}"
    #             record.mes_secuencia = f"-{mes}-{secuencia}"
    #         else:
    #             record.mes_secuencia = ''
    codigo_A1_or_A2 = fields.Char(
        string='Código A1 o A2',
        compute='_compute_codigo_fiscal',
        store=False
    )

    # @api.depends('company_id.company_registry')
    # def _compute_codigo_fiscal(self):
    #     for record in self:
    #         if record.company_id.company_registry == '100':
    #             record.codigo_A1_or_A2 = "A1"
    #         elif record.company_id.company_registry == '200':
    #             record.codigo_A1_or_A2 = "A2"
    #         else:
    #             record.codigo_A1_or_A2 = ""
    @api.depends('company_id.is_fiscal_or_interna')
    def _compute_codigo_fiscal(self):
        for record in self:
            if record.company_id.is_fiscal_or_interna == '1':
                record.codigo_A1_or_A2 = "A1"
            elif record.company_id.is_fiscal_or_interna == '2':
                record.codigo_A1_or_A2 = "A2"
            else:
                record.codigo_A1_or_A2 = ""

    def number_to_word(self, number: float):
        decimal_part = int(round(number % 1, 2) * 100)
        integer_part = int(number)
        # obtener el idioma actual
        lang = self.env.context.get('lang', 'es_ES')
        return f"{num2words(integer_part, lang=lang)} con {decimal_part}/100 BS"

    def amount_to_text(self, amount):
        # Usar num2words para convertir el monto en número a texto
        return num2words(amount, lang='es')
