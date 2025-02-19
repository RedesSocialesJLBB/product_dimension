from odoo import api, fields, models


class ProductMeasures(models.Model):
    _name = "product.measures"
    _description = "Medidas del producto"

    product_measures_length = fields.Many2one(
        "product.measures",
        "Largo",
        readonly=False
    )
    product_measures_width = fields.Many2one(
        "product.measures",
        "Ancho",
        readonly=False
    )
    product_measures_thickness = fields.Many2one(
        "product.measures",
        "Grueso",
        readonly=False
    )
    product_template_id = fields.Many2one(
        "product.template",
        "ID de Producto",
        readonly=True
    )