# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateOdaInstanceAttachmentDetails(object):
    """
    Properties required to create an ODA instance attachment.
    """

    #: A constant which can be used with the attachment_type property of a CreateOdaInstanceAttachmentDetails.
    #: This constant has a value of "FUSION"
    ATTACHMENT_TYPE_FUSION = "FUSION"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateOdaInstanceAttachmentDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param attach_to_id:
            The value to assign to the attach_to_id property of this CreateOdaInstanceAttachmentDetails.
        :type attach_to_id: str

        :param attachment_type:
            The value to assign to the attachment_type property of this CreateOdaInstanceAttachmentDetails.
            Allowed values for this property are: "FUSION"
        :type attachment_type: str

        :param attachment_metadata:
            The value to assign to the attachment_metadata property of this CreateOdaInstanceAttachmentDetails.
        :type attachment_metadata: str

        :param restricted_operations:
            The value to assign to the restricted_operations property of this CreateOdaInstanceAttachmentDetails.
        :type restricted_operations: list[str]

        :param owner:
            The value to assign to the owner property of this CreateOdaInstanceAttachmentDetails.
        :type owner: oci.oda.models.OdaInstanceAttachmentOwner

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateOdaInstanceAttachmentDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateOdaInstanceAttachmentDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'attach_to_id': 'str',
            'attachment_type': 'str',
            'attachment_metadata': 'str',
            'restricted_operations': 'list[str]',
            'owner': 'OdaInstanceAttachmentOwner',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'attach_to_id': 'attachToId',
            'attachment_type': 'attachmentType',
            'attachment_metadata': 'attachmentMetadata',
            'restricted_operations': 'restrictedOperations',
            'owner': 'owner',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._attach_to_id = None
        self._attachment_type = None
        self._attachment_metadata = None
        self._restricted_operations = None
        self._owner = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def attach_to_id(self):
        """
        **[Required]** Gets the attach_to_id of this CreateOdaInstanceAttachmentDetails.
        The OCID of the target instance (which could be any other OCI PaaS/SaaS resource), to which this ODA instance is being attached.


        :return: The attach_to_id of this CreateOdaInstanceAttachmentDetails.
        :rtype: str
        """
        return self._attach_to_id

    @attach_to_id.setter
    def attach_to_id(self, attach_to_id):
        """
        Sets the attach_to_id of this CreateOdaInstanceAttachmentDetails.
        The OCID of the target instance (which could be any other OCI PaaS/SaaS resource), to which this ODA instance is being attached.


        :param attach_to_id: The attach_to_id of this CreateOdaInstanceAttachmentDetails.
        :type: str
        """
        self._attach_to_id = attach_to_id

    @property
    def attachment_type(self):
        """
        **[Required]** Gets the attachment_type of this CreateOdaInstanceAttachmentDetails.
        The type of target instance which this ODA instance is being attached.

        Allowed values for this property are: "FUSION"


        :return: The attachment_type of this CreateOdaInstanceAttachmentDetails.
        :rtype: str
        """
        return self._attachment_type

    @attachment_type.setter
    def attachment_type(self, attachment_type):
        """
        Sets the attachment_type of this CreateOdaInstanceAttachmentDetails.
        The type of target instance which this ODA instance is being attached.


        :param attachment_type: The attachment_type of this CreateOdaInstanceAttachmentDetails.
        :type: str
        """
        allowed_values = ["FUSION"]
        if not value_allowed_none_or_none_sentinel(attachment_type, allowed_values):
            raise ValueError(
                "Invalid value for `attachment_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._attachment_type = attachment_type

    @property
    def attachment_metadata(self):
        """
        Gets the attachment_metadata of this CreateOdaInstanceAttachmentDetails.
        Attachment specific metadata. Defined by the target service.


        :return: The attachment_metadata of this CreateOdaInstanceAttachmentDetails.
        :rtype: str
        """
        return self._attachment_metadata

    @attachment_metadata.setter
    def attachment_metadata(self, attachment_metadata):
        """
        Sets the attachment_metadata of this CreateOdaInstanceAttachmentDetails.
        Attachment specific metadata. Defined by the target service.


        :param attachment_metadata: The attachment_metadata of this CreateOdaInstanceAttachmentDetails.
        :type: str
        """
        self._attachment_metadata = attachment_metadata

    @property
    def restricted_operations(self):
        """
        Gets the restricted_operations of this CreateOdaInstanceAttachmentDetails.
        List of operations that are restricted while this instance is attached.


        :return: The restricted_operations of this CreateOdaInstanceAttachmentDetails.
        :rtype: list[str]
        """
        return self._restricted_operations

    @restricted_operations.setter
    def restricted_operations(self, restricted_operations):
        """
        Sets the restricted_operations of this CreateOdaInstanceAttachmentDetails.
        List of operations that are restricted while this instance is attached.


        :param restricted_operations: The restricted_operations of this CreateOdaInstanceAttachmentDetails.
        :type: list[str]
        """
        self._restricted_operations = restricted_operations

    @property
    def owner(self):
        """
        **[Required]** Gets the owner of this CreateOdaInstanceAttachmentDetails.

        :return: The owner of this CreateOdaInstanceAttachmentDetails.
        :rtype: oci.oda.models.OdaInstanceAttachmentOwner
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this CreateOdaInstanceAttachmentDetails.

        :param owner: The owner of this CreateOdaInstanceAttachmentDetails.
        :type: oci.oda.models.OdaInstanceAttachmentOwner
        """
        self._owner = owner

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateOdaInstanceAttachmentDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateOdaInstanceAttachmentDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateOdaInstanceAttachmentDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateOdaInstanceAttachmentDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateOdaInstanceAttachmentDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateOdaInstanceAttachmentDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateOdaInstanceAttachmentDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateOdaInstanceAttachmentDetails.
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
