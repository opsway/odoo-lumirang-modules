from odoo.tests import tagged, TransactionCase

from ..lib.format import format_name, decompose_name
from parameterized import parameterized


@tagged("first_last_name_mixin")
class TestMixin(TransactionCase):
    @parameterized.expand((
            ("John", "Doe",),
            ("John M", "Doe",),
    ))
    def test_mixin(self, first, last):
        p = self.env['full.name.test.mixin'].create({
            'first_name': first,
            'last_name': last,
        })
        self.assertEqual(format_name(first, last), p.name)
        self.assertEqual(first, p.first_name)
        self.assertEqual(last, p.last_name)

        p.write({'first_name': last, 'last_name': first})
        self.assertEqual(format_name(last, first), p.name)

    @parameterized.expand((
            ("John", "Doe",),
            ("John M", "Doe",),
    ))
    def test_mixin_with_name(self, first, last):
        p = self.env['full.name.test.mixin'].create({
            'name': format_name(first, last),
        })
        self.assertEqual(format_name(first, last), p.name)
        self.assertEqual(first, p.first_name)
        self.assertEqual(last, p.last_name)

        p.write({'first_name': last, 'last_name': first})
        self.assertEqual(format_name(last, first), p.name)

    @parameterized.expand((
            ("Jason Dean", "Jason", "Dean",),
            ("Jason J Dean", "Jason J", "Dean",),
            ("Jason J Dean Jr", "Jason J", "Dean Jr",),
            ("Jason Michael Lawrence Dean Jr", "Jason Michael Lawrence", "Dean Jr",),
    ))
    def test_decompose(self, name, first, last):
        self.assertTupleEqual((first, last), decompose_name(name))
