# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def _file_read(self, fname, size=None):
        """
        Overwrite the native _file_read to change the log level from INFO to DEBUG
        when a file is missing in the filestore.
        This prevents misleading tracebacks in Odoo.sh deployments and development branches.
        """
        full_path = self._full_path(fname)
        try:
            with open(full_path, 'rb') as f:
                return f.read(size)
        except OSError:
            # Replaced _logger.info with _logger.debug to keep logs clean
            _logger.debug("_read_file reading %s", full_path, exc_info=True)
        return b''
