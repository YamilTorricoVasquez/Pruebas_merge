from odoo import fields, models, api

import re


class StockPicking(models.Model):
    _inherit = "stock.picking"

    saleOrder = fields.Char(string="Order", compute="ordenes_de_venta", store=True)
    secuencia = fields.Char(
        string="Secuencia", compute="_compute_mes_secuencia", store=True
    )
    mes = fields.Char(string="Mes Secuencia",compute="_compute_mes_secuencia")

    def ordenes_de_venta(self):
        for record in self:
            for o in record.sale_id:
                record.saleOrder = o.name

    def _compute_mes_secuencia(self):
        for record in self:
            if record.mes_secuencia:
                record.secuencia = re.sub(r"-\d{2}-", "", record.mes_secuencia)
                record.mes = re.search(r"-(\d{2})-", record.mes_secuencia).group(1)
            # else:
            #     record.secuencia = ""

    def button_validate(self):
        res = super().button_validate()
        for record in self:
            record._compute_mes_secuencia()
            record.ordenes_de_venta()
        return res