# -*- coding: utf-8 -*-
import logging

from odoo.tests.common import TransactionCase

from ..log_filter import CORE_LOGGER, MISSING_FILE_MESSAGE


class TestFilestoreLogFilter(TransactionCase):

    def test_missing_file_log_is_downgraded_to_debug(self):
        """Lire un fichier absent du filestore doit logger en DEBUG, pas en INFO."""
        with self.assertLogs(CORE_LOGGER, level='DEBUG') as capture:
            content = self.env['ir.attachment']._file_read('ab/fichier-absent-du-filestore')

        # Le comportement fonctionnel du coeur est preserve : contenu vide,
        # aucune exception remontee a l'appelant.
        self.assertEqual(content, b'')

        matching = [r for r in capture.records if r.msg == MISSING_FILE_MESSAGE]
        self.assertTrue(
            matching,
            "Le message du coeur a change : le filtre ne correspond plus et le "
            "traceback va reapparaitre dans les logs Odoo.sh"
        )
        self.assertEqual(
            matching[0].levelno, logging.DEBUG,
            "Le log du fichier manquant doit etre abaisse a DEBUG"
        )

    def test_other_records_on_the_same_logger_are_untouched(self):
        """Le filtre ne doit toucher qu'au message du fichier manquant."""
        logger = logging.getLogger(CORE_LOGGER)
        with self.assertLogs(CORE_LOGGER, level='DEBUG') as capture:
            logger.info("un autre message sans rapport %s", 'x')

        self.assertEqual(
            capture.records[0].levelno, logging.INFO,
            "Un autre INFO du meme logger doit rester en INFO"
        )
