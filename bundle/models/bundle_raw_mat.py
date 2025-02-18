# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class BundleRawMat(models.Model):
    _name = 'bundle.raw.mat'
    _description = 'Represent the component of a bundle'

    sequence = fields.Integer(string='sequence', default=10)
    product_tmpl_id = fields.Many2one('product.template', string='Bundle prueba', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    name = fields.Text(string="Name", required=True)

    def prepare_raw_mat_wiz(self, quantity=1.0):
        """
        Create a dictionary of values for creating bundle.raw.mat.wiz records.
        """
        self.ensure_one()
        return {
            'sequence': self.sequence,
            'product_id': self.product_id.id if self.product_id else False,
            'unit_quantity': self.quantity,
            'quantity': self.quantity * quantity,
            'uom_id': self.uom_id.id if self.uom_id else False,
            'display_type': self.display_type,
            'name': self.name,
        }

    @api.constrains('product_id', 'display_type')
    def none_section_line_product_mandatory(self):
        """
        Line which are not a section or a comment must have a product.
        """
        for line in self:
            if not line.display_type and not line.product_id:
                raise ValidationError(_("Bundle's raw materials must have a product."))

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id
            self.name = self.product_id.get_product_multiline_description_sale()

    def name_get(self):
        """
        Compute the raw mat name.
        """
        result = []
        for line in self.sudo():
            name = '%s - %s' % (line.product_tmpl_id.name, line.product_id.name)
            result.append((line.id, name))
        return result

    @api.model
    def _prepare_add_missing_fields(self, values):
        """ Deduce missing required fields"""
        res = values.copy()
        onchange_fields = ['name']
        if any(f not in values for f in onchange_fields):
            if 'product_id' in res:
                product = self.env['product.product'].browse(res['product_id'])
                res['name'] = product.name
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """
        Add required field in the dictionary if not explicitly given.
        """
        for values in vals_list:
            values.update(self._prepare_add_missing_fields(values))
        return super().create(vals_list)
