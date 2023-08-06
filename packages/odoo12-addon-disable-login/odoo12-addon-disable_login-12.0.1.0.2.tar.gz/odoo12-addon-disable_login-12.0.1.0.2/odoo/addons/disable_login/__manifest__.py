# Copyright 2023-Coopdevs Treball SCCL (<https://coopdevs.org>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Disable Odoo Login",
    "version": "12.0.1.0.2",
    "depends": ["web", "auth_oauth"],
    "author": "Coopdevs Treball SCCL",
    "category": "Auth",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Disable login template to force to use the OAuth login.
    """,
    "data": ["views/auth_templates.xml"],
    "installable": True,
}
