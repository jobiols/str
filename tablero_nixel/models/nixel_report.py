# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.osv import osv
from openerp.report import report_sxw

class nixel_report_demo(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(nixel_report_demo, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_total': self._get_total,
        })

    def _get_total(self, lines, field):
        total = 10
        return total

class report_nixel_class(osv.AbstractModel):
    _name = 'report.tablero_nixel.nixel_report'
    _inherit = 'report.abstract_report'
    _template = 'tablero_nixel.nixel_report'
    _wrapped_report_class = nixel_report_demo


"""
from openerp import api, models

class ParticularReport(models.AbstractModel):
    _name = 'report.tablero_nixel.nixel_report'
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('tablero_nixel.nixel_report')

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('tablero_nixel.nixel_report', docargs)

"""
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
