from odoo.tests import tagged, TransactionCase

from ..lib.format import format_name


@tagged("first_last_name")
class TestPartner(TransactionCase):
    def test_partner(self):
        first = "1"
        last = "2"
        p = self.env['res.partner'].create({
            'first_name': first,
            'last_name': last,
            'email': "email",
        })
        self.assertEqual(p.name, format_name(first, last))

        p.write({'first_name': last, 'last_name': first})
        self.assertEqual(p.name, format_name(last, first))

    def test_company(self):
        name = "name"
        name2 = "name2"
        self.assertNotEqual(name, name2)
        p = self.env['res.partner'].create({
            'name': name,
            'email': "email",
            'company_type': "company"
        })
        self.assertEqual(p.name, name)
        p.name = name2
        self.assertEqual(p.name, name2)
        self.assertEqual(p.first_name, name2)
        self.assertEqual(p.last_name, "")
