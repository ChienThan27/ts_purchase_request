from odoo import models,fields,api

class TsPurchaseRequestAddProductsWizard(models.TransientModel):
    _name = "ts.purchase.request.add.products.wizard"
    _description = "Thêm sản phẩm"

    request_id = fields.Many2one("ts.purchase.request", string="Phiếu yêu cầu", required=True)
    product_ids = fields.Many2many("product.product", string="Sản Phẩm", required=True)
    default_quantity = fields.Integer(string="Số lượng", defaulf=0)
    skip_existing = fields.Boolean(string="Bỏ qua sản phẩm trùng", default=False)

    def action_add_products(self):
        for product in self.product_ids:
            self.env["ts.purchase.request.line"].create({
                "request_id": self.request_id.id,
                "product_id": product.id,
                "quantity": self.default_quantity,
            })
