from odoo.tests import tagged, TransactionCase

from ..lib.format import format_name


@tagged("first_last_name_mixin")
class TestMixin(TransactionCase):
    def test_mixin(self):
        first = "1"
        last = "2"
        p = self.env['full.name.test.mixin'].create({
            'first_name': first,
            'last_name': last,
        })
        self.assertEqual(p.name, format_name(first, last))

        p.write({'first_name': last, 'last_name': first})
        self.assertEqual(p.name, format_name(last, first))

    def test_mixin_with_name(self):
        first = "1"
        last = "2"
        p = self.env['full.name.test.mixin'].create({
            'name': "{} {}".format(first, last),
        })
        self.assertEqual(p.name, format_name(first, last))

        p.write({'first_name': last, 'last_name': first})
        self.assertEqual(p.name, format_name(last, first))
