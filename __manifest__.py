{
    'name': 'Patch: Filestore Log Level Fix',
    'version': '19.0.1.0.0',
    'category': 'Hidden/Technical',
    'summary': 'Changes ir.attachment._file_read log level from info to debug to avoid misleading tracebacks in Odoo.sh logs',
    'author': 'Pacific ERP',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [],
    'installable': True,
    'auto_install': True,
    'application': False,
}
