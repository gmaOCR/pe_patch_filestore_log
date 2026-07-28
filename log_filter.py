# -*- coding: utf-8 -*-
import logging

# Logger et message exacts emis par ir.attachment._file_read du coeur
# lorsqu'un fichier est absent du filestore.
CORE_LOGGER = 'odoo.addons.base.models.ir_attachment'
MISSING_FILE_MESSAGE = "_read_file reading %s"


class MissingFilestoreFileFilter(logging.Filter):
    """Ramene a DEBUG le log INFO emis quand un fichier manque au filestore.

    Contexte : restaurer une base sans son filestore fait emettre par
    ir.attachment._file_read un INFO avec traceback complet pour CHAQUE fichier
    absent. Les logs de build Odoo.sh sont noyes et cela ressemble a un
    plantage, alors qu'il s'agit d'un decalage base/filestore.

    Pourquoi un filtre de log plutot qu'une surcharge de _file_read : la version
    precedente de ce module recopiait la methode du coeur mot pour mot, sans
    appeler super(). Elle annulait donc silencieusement toute evolution amont,
    et sa copie avait deja derive : elle avait perdu le garde
    `assert isinstance(self, IrAttachment)` present dans Odoo 19.

    Un filtre ne touche a aucune logique metier et degrade sans danger : si le
    message du coeur change un jour, le filtre cesse simplement de correspondre
    et le log redevient visible. C'est l'inverse du risque precedent, ou une
    evolution du coeur etait perdue sans que rien ne le signale.
    """

    def filter(self, record):
        if record.msg == MISSING_FILE_MESSAGE:
            record.levelno = logging.DEBUG
            record.levelname = logging.getLevelName(logging.DEBUG)
        # Toujours True : on abaisse le niveau, on ne supprime pas le record.
        # Ce sont les handlers qui l'ecarteront selon leur propre niveau, donc
        # le message reste consultable en --log-level=debug.
        return True


logging.getLogger(CORE_LOGGER).addFilter(MissingFilestoreFileFilter())
