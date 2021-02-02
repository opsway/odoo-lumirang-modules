from odoo.tests import tagged, TransactionCase

from ..lib.format import format_name


@tagged("first_last_name")
class TestUsers(TransactionCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        self.first = "1"
        self.last = "2"
        self.user = self.env['res.users'].create({
            'first_name': self.first,
            'last_name': self.last,
            'login': "login",
            'email': "email",
            'active': True,
        })

    def test_user(self):
        self.assertEqual(self.user.name, format_name(self.first, self.last))
        self.assertEqual(self.user.partner_id.name, format_name(self.first, self.last))

        self.user.write({'first_name': self.last, 'last_name': self.first})
        self.assertEqual(self.user.partner_id.name, self.user.name)
        self.assertEqual(self.user.partner_id.name, format_name(self.last, self.first))

    def test_partner(self):
        partner_first = "p1"
        partner_last = "p2"
        self.assertNotEqual(partner_first, self.first)
        self.assertNotEqual(partner_last, self.last)
        partner = self.env['res.partner'].create({
            'first_name': partner_first,
            'last_name': partner_last,
            'email': "email",
        })

        self.user.partner_id = partner
        self.assertEqual(self.user.name, format_name(partner_first, partner_last))

    def test_partner_with_name(self):
        partner_first = "p1"
        partner_last = "p2"
        self.assertNotEqual(partner_first, self.first)
        self.assertNotEqual(partner_last, self.last)
        partner = self.env['res.partner'].create({
            'name': "{} {}".format(partner_first, partner_last),
            'email': "email",
        })

        self.user.partner_id = partner
        self.assertEqual(self.user.name, format_name(partner_first, partner_last))
