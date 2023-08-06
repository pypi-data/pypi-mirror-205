# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .pii_entity_masking import PiiEntityMasking
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PiiEntityRemove(PiiEntityMasking):
    """
    Remove PII entities from output.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PiiEntityRemove object with values from keyword arguments. The default value of the :py:attr:`~oci.ai_language.models.PiiEntityRemove.mode` attribute
        of this class is ``REMOVE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param mode:
            The value to assign to the mode property of this PiiEntityRemove.
            Allowed values for this property are: "REPLACE", "MASK", "REMOVE"
        :type mode: str

        """
        self.swagger_types = {
            'mode': 'str'
        }

        self.attribute_map = {
            'mode': 'mode'
        }

        self._mode = None
        self._mode = 'REMOVE'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
