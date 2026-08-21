import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    _logger.info("l10n_ar_payment_bundle: running pre-migration for %s", version)

    # Delete all views of l10n_ar_payment_bundle to prevent xpath errors
    # (e.g. 'action_post_and_new' removed from parent views in 19.0)
    # when reloading views during module update.
    cr.execute("""
        DELETE FROM ir_ui_view
        WHERE id IN (
            SELECT res_id FROM ir_model_data
            WHERE model = 'ir.ui.view'
            AND module = 'l10n_ar_payment_bundle'
        )
    """)
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE model = 'ir.ui.view'
        AND module = 'l10n_ar_payment_bundle'
    """)
