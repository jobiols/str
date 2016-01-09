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

PROVEEDORES = 79
DEUDORES_POR_VENTAS = 8
GASTOS = 155


class nixel_report_def(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(nixel_report_def, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_debtors': self._get_debtors,
            'get_creditors': self._get_creditors,

            'get_venta': self._get_venta,
            'get_compra': self._get_compra,
            'get_gastos': self._get_gastos,
        })

    def _get_compute_balance(self, cr, uid, account_id):
        accounts = self.pool['account.account']
        ids = accounts.search(cr, uid, [('id', '=', account_id)])
        result = []
        for account in accounts.browse(cr, uid, ids):
            type = account.type

            if type == 'receivable':
                sumarg = 'debit-credit'
            else:
                sumarg = 'credit-debit'

            cr.execute("""
                select sum(%s) as balance,  res_partner.name
                from account_move_line
                inner join res_partner
                on res_partner.id = account_move_line.partner_id
                where account_id = %s
                group by partner_id, res_partner.name
                """ % (sumarg, account_id))
            result = cr.fetchall()
        return result

    def _summarize_account(self, cr, uid, account_id):
        """
        Sumariza la cuenta account_id en elementos del elementos del diario dando
        los créditos y débitos en un diccionario
        """
        accounts = self.pool['account.move.line']
        ids = accounts.search(cr, uid, [('account_id', '=', account_id)])
        debit = credit = 0.0
        for account in accounts.browse(cr, uid, ids):
            debit += account.debit
            credit += account.credit
        return {'debit': debit, 'credit': credit}

    def _get_debtors(self):
        debtors = []
        elements = self._get_compute_balance(self.cr, self.uid, DEUDORES_POR_VENTAS)
        for element in elements:
            debtors.append({'amount': element[0], 'name': element[1]})
        return debtors

    def _get_creditors(self):
        creditors = []
        elements = self._get_compute_balance(self.cr, self.uid, PROVEEDORES)
        for element in elements:
            creditors.append({'amount': element[0], 'name': element[1]})
        return creditors

    def _get_venta(self):
        dic = self._summarize_account(self.cr, self.uid, DEUDORES_POR_VENTAS)
        return {'fac': dic['debit'], 'cob': dic['credit'],
                'pen': dic['debit'] - dic['credit']}

    def _get_compra(self):
        dic = self._summarize_account(self.cr, self.uid, PROVEEDORES)
        return {'fac': dic['credit'], 'cob': dic['debit'],
                'pen': dic['credit'] - dic['debit']}

    def _get_gastos(self):
        dic = self._summarize_account(self.cr, self.uid, GASTOS)
        return {'gas': dic['debit']}


class report_nixel_class(osv.AbstractModel):
    _name = 'report.tablero_nixel.nixel_report'
    _inherit = 'report.abstract_report'
    _template = 'tablero_nixel.nixel_report'
    _wrapped_report_class = nixel_report_def

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
