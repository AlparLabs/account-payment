"""
Pre-migration script for account_payment_pro 19.0.3.6.0
=========================================================

[AlparData] El merge de upstream (ingadhoc 19.0, nov-2026) borró el campo
`account.payment.reconcile_on_company_currency` (ahora se lee directo
`company_id.reconcile_on_company_currency`) y lo sacó de las vistas.

Problema: al actualizar, el modelo ya no tiene el campo pero las vistas del
módulo en la base conservan el arch viejo. Al cargar `account_payment_view.xml`
Odoo escribe primero `view_account_payment_form` y valida la vista combinada
con `latam_check_view_account_payment_form_inherited` todavía vieja (se
actualiza más abajo en el mismo archivo) -> "Field reconcile_on_company_currency
does not exist in model account.payment".

Solución: desactivar las vistas del módulo cuyo arch todavía usa el campo.
Odoo no combina vistas inactivas (ni sus hijas) al validar, el XML les carga
el arch nuevo y `0.0.0/post-alpar_reactivate_views.py` las reactiva.
"""

import logging

_logger = logging.getLogger(__name__)

REMOVED_FIELD = "reconcile_on_company_currency"


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        UPDATE ir_ui_view v
           SET active = FALSE
          FROM ir_model_data d
         WHERE d.model = 'ir.ui.view'
           AND d.res_id = v.id
           AND d.module = 'account_payment_pro'
           AND v.model = 'account.payment'
           AND v.active
           AND v.arch_db::text LIKE %s
        RETURNING d.name
        """,
        ["%" + REMOVED_FIELD + "%"],
    )
    names = sorted(row[0] for row in cr.fetchall())
    if names:
        _logger.info(
            "account_payment_pro: desactivando vistas con el campo borrado %s "
            "(las reactiva post-alpar_reactivate_views): %s",
            REMOVED_FIELD,
            names,
        )
