# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateScheduledTaskDetails(object):
    """
    Details for creating a scheduled task.
    """

    #: A constant which can be used with the kind property of a CreateScheduledTaskDetails.
    #: This constant has a value of "ACCELERATION"
    KIND_ACCELERATION = "ACCELERATION"

    #: A constant which can be used with the kind property of a CreateScheduledTaskDetails.
    #: This constant has a value of "STANDARD"
    KIND_STANDARD = "STANDARD"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateScheduledTaskDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.log_analytics.models.CreateStandardTaskDetails`
        * :class:`~oci.log_analytics.models.CreateAccelerationTaskDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this CreateScheduledTaskDetails.
            Allowed values for this property are: "ACCELERATION", "STANDARD"
        :type kind: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateScheduledTaskDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateScheduledTaskDetails.
        :type display_name: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateScheduledTaskDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateScheduledTaskDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'kind': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'kind': 'kind',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._kind = None
        self._compartment_id = None
        self._display_name = None
        self._freeform_tags = None
        self._defined_tags = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['kind']

        if type == 'STANDARD':
            return 'CreateStandardTaskDetails'

        if type == 'ACCELERATION':
            return 'CreateAccelerationTaskDetails'
        else:
            return 'CreateScheduledTaskDetails'

    @property
    def kind(self):
        """
        **[Required]** Gets the kind of this CreateScheduledTaskDetails.
        Discriminator.

        Allowed values for this property are: "ACCELERATION", "STANDARD"


        :return: The kind of this CreateScheduledTaskDetails.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        Sets the kind of this CreateScheduledTaskDetails.
        Discriminator.


        :param kind: The kind of this CreateScheduledTaskDetails.
        :type: str
        """
        allowed_values = ["ACCELERATION", "STANDARD"]
        if not value_allowed_none_or_none_sentinel(kind, allowed_values):
            raise ValueError(
                "Invalid value for `kind`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._kind = kind

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateScheduledTaskDetails.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateScheduledTaskDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateScheduledTaskDetails.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateScheduledTaskDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateScheduledTaskDetails.
        A user-friendly name that is changeable and that does not have to be unique.
        Format: a leading alphanumeric, followed by zero or more
        alphanumerics, underscores, spaces, backslashes, or hyphens in any order).
        No trailing spaces allowed.


        :return: The display_name of this CreateScheduledTaskDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateScheduledTaskDetails.
        A user-friendly name that is changeable and that does not have to be unique.
        Format: a leading alphanumeric, followed by zero or more
        alphanumerics, underscores, spaces, backslashes, or hyphens in any order).
        No trailing spaces allowed.


        :param display_name: The display_name of this CreateScheduledTaskDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateScheduledTaskDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateScheduledTaskDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateScheduledTaskDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateScheduledTaskDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateScheduledTaskDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateScheduledTaskDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateScheduledTaskDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateScheduledTaskDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
