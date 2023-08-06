# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalServicedAsm(object):
    """
    The details of ASM serviced by an external listener.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalServicedAsm object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalServicedAsm.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalServicedAsm.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalServicedAsm.
        :type compartment_id: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalServicedAsm.
        The `OCID`__ of the external ASM.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalServicedAsm.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalServicedAsm.
        The `OCID`__ of the external ASM.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalServicedAsm.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalServicedAsm.
        The user-friendly name for the external ASM. The name does not have to be unique.


        :return: The display_name of this ExternalServicedAsm.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalServicedAsm.
        The user-friendly name for the external ASM. The name does not have to be unique.


        :param display_name: The display_name of this ExternalServicedAsm.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this ExternalServicedAsm.
        The `OCID`__ of the compartment in which the external ASM resides.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalServicedAsm.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalServicedAsm.
        The `OCID`__ of the compartment in which the external ASM resides.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalServicedAsm.
        :type: str
        """
        self._compartment_id = compartment_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
