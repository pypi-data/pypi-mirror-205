# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PiiEntityMasking(object):
    """
    Mask recognized PII entities with different modes.
    """

    #: A constant which can be used with the mode property of a PiiEntityMasking.
    #: This constant has a value of "REPLACE"
    MODE_REPLACE = "REPLACE"

    #: A constant which can be used with the mode property of a PiiEntityMasking.
    #: This constant has a value of "MASK"
    MODE_MASK = "MASK"

    #: A constant which can be used with the mode property of a PiiEntityMasking.
    #: This constant has a value of "REMOVE"
    MODE_REMOVE = "REMOVE"

    def __init__(self, **kwargs):
        """
        Initializes a new PiiEntityMasking object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.ai_language.models.PiiEntityReplace`
        * :class:`~oci.ai_language.models.PiiEntityRemove`
        * :class:`~oci.ai_language.models.PiiEntityMask`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param mode:
            The value to assign to the mode property of this PiiEntityMasking.
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

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['mode']

        if type == 'REPLACE':
            return 'PiiEntityReplace'

        if type == 'REMOVE':
            return 'PiiEntityRemove'

        if type == 'MASK':
            return 'PiiEntityMask'
        else:
            return 'PiiEntityMasking'

    @property
    def mode(self):
        """
        **[Required]** Gets the mode of this PiiEntityMasking.
        The type of masking mode.

        Allowed values for this property are: "REPLACE", "MASK", "REMOVE"


        :return: The mode of this PiiEntityMasking.
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the mode of this PiiEntityMasking.
        The type of masking mode.


        :param mode: The mode of this PiiEntityMasking.
        :type: str
        """
        allowed_values = ["REPLACE", "MASK", "REMOVE"]
        if not value_allowed_none_or_none_sentinel(mode, allowed_values):
            raise ValueError(
                "Invalid value for `mode`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._mode = mode

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
