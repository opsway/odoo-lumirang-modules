import logging
from collections import Iterable
from functools import lru_cache
from typing import Tuple, Dict, List

from odoo import fields
from odoo.fields import resolve_mro

_logger = logging.getLogger(__name__)


class Choice:
    id: int
    ref: str
    name: str

    def __init__(self, id_: int, ref: str, name: str):
        self.id = id_
        self.ref = ref
        self.name = name

    def as_dict(self):
        return {
            'id': self.id,
            'ref': self.ref,
            'name': self.name,
        }

    __json__ = as_dict


@lru_cache(maxsize=None)
def choices_data(model) -> Tuple[List[Choice], Dict[str, Choice], Dict[int, Choice]]:
    """
    Prepares choices hash: choice by ext id and choice by resource id.
    :param model: Odoo model
    :return: choice by ext id and choice by resource id
    """
    all_choices = model.search([])
    # dict with key as a complaint id, and value as a complaint external id local part.
    choice_ext_ids = {k: v.split(".")[1] for k, v in all_choices.get_external_id().items()}
    choices = [Choice(x.id, choice_ext_ids[x.id], x.name) for x in all_choices]
    choice_refs = {x.ref: x for x in choices}
    choice_ids = {x.id: x for x in choices}
    return choices, choice_refs, choice_ids


class Many2manyChoices(fields.Many2many):
    """
    Provides list of possible ids for the field.
    :param choices: specifies the possible values for this field.
        It is given as a list of string ids.

    :param choices_add: provides an extension of the choices in the case
        of an overridden field. It is a list of string ids.

    The attribute ``choices`` is mandatory.
    """

    _slots = {
        'choices': None,
        'choices_data': None,
    }

    def _setup_attrs(self, model, name):
        super(Many2manyChoices, self)._setup_attrs(model, name)
        # determine choices (applying 'choices_add' extensions)
        values = None

        for field in reversed(resolve_mro(model, name, self._can_setup_from)):
            # We cannot use field.choices or field.choices_add here
            # because those attributes are overridden by ``_setup_attrs``.
            if 'choices' in field.args:
                choices = field.args['choices']
                assert isinstance(choices, Iterable), "{}: choices={} must be an iterable".format(self, choices)
                if values is not None and values != [x for x in choices]:
                    _logger.warning("{}: choices={} overrides existing choices; use choices_add instead"
                                    .format(self, choices))
                values = [x for x in choices]

            if 'choices_add' in field.args:
                choices_add = field.args['choices_add']
                assert isinstance(choices_add, Iterable), "{}: choices_add={} must be an iterable".format(self,
                                                                                                          choices_add)
                assert values is not None, "{}: choices_add={} on non-initialized choices {}".format(self, choices_add,
                                                                                                     self.choices)
                values.extend(choices_add)

        if values is not None:
            self.choices = values

    def _description_choices(self, env):
        if self.choices_data is None:
            all_choices, refs, _ = choices_data(env[self.comodel_name])
            choices = self.choices
            if not all_choices:
                # happens during module installation. Data is not yet installed, just empty result will suffice
                return []
            if not choices:
                choices = [x.ref for x in all_choices]
            self.choices_data = tuple(refs[x] for x in choices)
        return self.choices_data
