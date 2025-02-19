# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_height = fields.Many2one(
        "product.measures",
        "height",
        related="product_tmpl_id.product_height", 
        readonly=False
        )
    product_width = fields.Many2one(
        "product.measures",
        "width",
        related="product_tmpl_id.product_width", 
        readonly=False
        )
    product_thickness = fields.Many2one(
        "product.measures",
        "thickness",
        related="product_tmpl_id.product_thickness", 
        readonly=False
        )
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for height, width, thickness",
        default=lambda self: self.env.ref("uom.product_uom_meter"),
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )
   # volume_2 = fields.Float(
   #     "Volume 2",
   #     compute="_compute_area",
   #     readonly=False,
   #     store=True,
   # )
   # volume_3 = fields.Float(
   #     "Volume 3",
   #     compute="_compute_length",
   #     readonly=False,
   #     store=True,
   # )

    @api.depends(
        "product_height", "product_width", "product_thickness", "dimensional_uom_id"
    )
    def _compute_volume(self):
        template_obj = self.env["product.template"]
        for product in self:
            product.volume = template_obj._calc_volume(
                product.product_height,
                product.product_width,
                product.product_thickness,
                product.dimensional_uom_id,
            )

   # def _compute_area(self):
   #     template_obj = self.env["product.template"]
   #     for product in self:
   #         product.volume_2 = template_obj._calc_area(
   #             product.product_height,
   #             product.product_width,
   #             product.dimensional_uom_id,
   #         )

   # def _compute_length(self):
   #     template_obj = self.env["product.template"]
   #     for product in self:
   #         product.volume_3 = template_obj._calc_length(
   #             product.product_height,
   #             product.dimensional_uom_id,
   #         )

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]
