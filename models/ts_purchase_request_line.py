from odoo import models,fields,api

class TsPurchaseRequestLine(models.Model):
    _name = "ts.purchase.request.line"
    _description = "San pham can mua"

    request_id = fields.Many2one("ts.payroll.request", string="Phieu yeu cau", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="San pham/Vat tu", required=True, ondelete="cascade")
    description = fields.Text(string="Mo ta")
    quantity = fields.Float(string="So luong")
    uom_id = fields.Many2one("uom.uom", string="Don vi tinh")
    estimated_price = fields.Float(string="Gia du kien")
    subtotal = fields.Float(string="Thanh tien", compute="_compute_subtotal")
    vendor_id = fields.Many2one("res.partner",string="Nha cung cap")
    note = fields.Text(string="Ghi chu")

    @api.depends("quantity","estimated_price")
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.estimated_price