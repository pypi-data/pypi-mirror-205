# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .pii_entity_masking import PiiEntityMasking
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PiiEntityMask(PiiEntityMasking):
    """
    Mask PII entities with the given masking character.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PiiEntityMask object with values from keyword arguments. The default value of the :py:attr:`~oci.ai_language.models.PiiEntityMask.mode` attribute
        of this class is ``MASK`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param mode:
            The value to assign to the mode property of this PiiEntityMask.
            Allowed values for this property are: "REPLACE", "MASK", "REMOVE"
        :type mode: str

        :param masking_character:
            The value to assign to the masking_character property of this PiiEntityMask.
        :type masking_character: str

        :param leave_characters_unmasked:
            The value to assign to the leave_characters_unmasked property of this PiiEntityMask.
        :type leave_characters_unmasked: int

        :param is_unmasked_from_end:
            The value to assign to the is_unmasked_from_end property of this PiiEntityMask.
        :type is_unmasked_from_end: bool

        """
        self.swagger_types = {
            'mode': 'str',
            'masking_character': 'str',
            'leave_characters_unmasked': 'int',
            'is_unmasked_from_end': 'bool'
        }

        self.attribute_map = {
            'mode': 'mode',
            'masking_character': 'maskingCharacter',
            'leave_characters_unmasked': 'leaveCharactersUnmasked',
            'is_unmasked_from_end': 'isUnmaskedFromEnd'
        }

        self._mode = None
        self._masking_character = None
        self._leave_characters_unmasked = None
        self._is_unmasked_from_end = None
        self._mode = 'MASK'

    @property
    def masking_character(self):
        """
        Gets the masking_character of this PiiEntityMask.
        Masking character. By default, the character is an asterisk (*)


        :return: The masking_character of this PiiEntityMask.
        :rtype: str
        """
        return self._masking_character

    @masking_character.setter
    def masking_character(self, masking_character):
        """
        Sets the masking_character of this PiiEntityMask.
        Masking character. By default, the character is an asterisk (*)


        :param masking_character: The masking_character of this PiiEntityMask.
        :type: str
        """
        self._masking_character = masking_character

    @property
    def leave_characters_unmasked(self):
        """
        Gets the leave_characters_unmasked of this PiiEntityMask.
        Number of characters to leave unmasked. By default, the whole entity is masked.


        :return: The leave_characters_unmasked of this PiiEntityMask.
        :rtype: int
        """
        return self._leave_characters_unmasked

    @leave_characters_unmasked.setter
    def leave_characters_unmasked(self, leave_characters_unmasked):
        """
        Sets the leave_characters_unmasked of this PiiEntityMask.
        Number of characters to leave unmasked. By default, the whole entity is masked.


        :param leave_characters_unmasked: The leave_characters_unmasked of this PiiEntityMask.
        :type: int
        """
        self._leave_characters_unmasked = leave_characters_unmasked

    @property
    def is_unmasked_from_end(self):
        """
        Gets the is_unmasked_from_end of this PiiEntityMask.
        Unmask from the end. By default, the whole entity is masked. This field works in concert with
        leaveCharactersUnmasked. For example, leaveCharactersUnmasked is 3 and isUnmaskedFromEnd is true,
        then if the entity is India the masked entity/result is **dia.


        :return: The is_unmasked_from_end of this PiiEntityMask.
        :rtype: bool
        """
        return self._is_unmasked_from_end

    @is_unmasked_from_end.setter
    def is_unmasked_from_end(self, is_unmasked_from_end):
        """
        Sets the is_unmasked_from_end of this PiiEntityMask.
        Unmask from the end. By default, the whole entity is masked. This field works in concert with
        leaveCharactersUnmasked. For example, leaveCharactersUnmasked is 3 and isUnmaskedFromEnd is true,
        then if the entity is India the masked entity/result is **dia.


        :param is_unmasked_from_end: The is_unmasked_from_end of this PiiEntityMask.
        :type: bool
        """
        self._is_unmasked_from_end = is_unmasked_from_end

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
