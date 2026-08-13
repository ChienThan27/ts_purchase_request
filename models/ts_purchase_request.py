from odoo import models,fields,api
from odoo.exceptions import ValidationError, UserError

class TsPurchaseRequest(models.Model):
    _name= "ts.purchase.request"
    _description = "Yeu cau mua hang"

    name = fields.Char(string="Ma yeu cau", required=True)
    request_date = fields.Date(string="Ngay yeu cau", required=True)
    requester_id = fields.Many2one("res.users", string="Nguoi yeu cau", required=True)
    department_name = fields.Char(string="Bo phan yeu cau")
    purpose = fields.Text(string="Muc dich mua")
    needed_date = fields.Date(string="Ngay can hang")
    line_ids = fields.One2many("ts.purchase.request.line", "request_id", string="Dong vat tu can mua")
    line_count = fields.Integer(string="So dong vat tu", compute="_compute_line_ids")
    amount_total = fields.Float(string="Tong tien du kien", compute="_compute_amount_total", aggregator="sum", store=True)
    state = fields.Selection(string="Trang thai", selection=[
        ("draft", "Nhap"), ("submitted","Da gui duyet"), ("approved","Da duyet"), ("purchasing","Dang mua hang"), ("done","Hoan tat"), ("cancel","Huy"), ("rejected","Tu choi")   
    ], default="draft")
    note = fields.Text(string="Ghi chu")

    @api.depends("line_ids")
    def _compute_line_ids(self):
        for rec in self:
            rec.line_count = len(rec.line_ids)

    @api.depends("line_ids.subtotal")
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = sum(rec.line_ids.mapped("subtotal"))

    @api.constrains("needed_date","request_date")
    def _compute_constrains_error(self):
        for rec in self:
            if rec.needed_date < rec.request_date:
                raise ValidationError(f"Không cho 'Ngày cần hàng' nhỏ hơn 'Ngày yêu cầu'.")

    def action_submitted(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError("Chưa có sản phẩm yêu cầu mua.")
            rec.state = "submitted"

    def action_approved(self):
        for rec in self:
            rec.state = "approved"

    def action_rejected(self):
        for rec in self:
            rec.state = "rejected"

    def action_purchasing(self):
        for rec in self:
            if rec.state != "approved":
                raise UserError("Yêu cầu chưa được duyệt.")
            rec.state = "purchasing"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_open_wizard_product(self):
        self.ensure_one()
        return{
            "type":"ir.actions.act_window",
            "name":"Them san pham",
            "res_model":"ts.purchase.request.add.products.wizard",
            "view_mode":"form",
            "target":"new",
            "context":{
                "default_request_id": self.id,
            }
        }
