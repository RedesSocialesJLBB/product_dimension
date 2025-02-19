# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for height, width, thickness",
        readonly=False,
    )
    product_height = fields.Many2one(
        "product.measures",
        "height",
        related="product_measures_id.product_measures_length", 
        readonly=False,
        store=True
    )
    product_width = fields.Many2one(
        "product.measures",
        "width",
        related="product_measures_id.product_measures_width", 
        readonly=False,
        store=True
    )
    product_thickness = fields.Many2one(
        "product.measures",
        "thickness",
        related="product_measures_id.product_measures_thickness", 
        readonly=False,
        store=True
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )
    product_measures_id = fields.One2many(
        "product.measures",
        "product_template_id",
        "ID de medidas del producto"
    )
    #volume_2 = fields.Float(
    #    compute="_compute_area",
    #    readonly=False,
    #    store=True,
    #)
    #volume_3 = fields.Float(
    #    compute="_compute_length",
    #    readonly=False,
    #    store=True,
    #)

    @api.model
    def _calc_volume(self, product_height, product_width, product_thickness, uom_id):
        volume = 0
        if product_height and product_width and product_thickness and uom_id:
            height_m = self.convert_to_meters(product_height, uom_id)
            width_m = self.convert_to_meters(product_width, uom_id)
            thickness_m = self.convert_to_meters(product_thickness, uom_id)
            volume = height_m * width_m * thickness_m

        return volume

    # def _calc_area(self, product_height, product_width,uom_id):
    #   area = 0
    #    if product_height and product_width and uom_id:
    #        height_m = self.convert_to_meters(product_height, uom_id)     
    #        width_m = self.convert_to_meters(product_width, uom_id)
    #        area = height_m * width_m
            
    #   return area

    #def _calc_length(self, product_height, uom_id):
    #    length = 0
    #    if product_height and uom_id:
    #        height_m = self.convert_to_meters(product_height, uom_id)
    #        length = height_m
            
    #   return length

    @api.depends(
        "product_height", "product_width", "product_thickness", "dimensional_uom_id"
    )
    def _compute_volume(self):
        for template in self:
            template.volume = template._calc_volume(
                template.product_height,
                template.product_width,
                template.product_thickness,
                template.dimensional_uom_id,
            )

    # def _compute_area(self):
    #    for template in self:
    #        template.volume_2 = template._calc_area(
    #            template.product_height,
    #            template.product_width,
    #            template.dimensional_uom_id,
    #        )

    # def _compute_length(self):
    #   for template in self:
    #        template.volume_3 = template._calc_length(
    #            template.product_height,
    #            template.dimensional_uom_id,
    #        )

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    def _prepare_variant_values(self, combination):
        """
        As variant is created inside template create() method and as
        template fields values are flushed after _create_variant_ids(),
        we catch the variant values preparation to update them
        """
        res = super()._prepare_variant_values(combination)
        if self.product_height:
            res.update({"product_height": self.product_height})
        if self.product_width:
            res.update({"product_width": self.product_width})
        if self.product_thickness:
            res.update({"product_thickness": self.product_thickness})        
        return res
