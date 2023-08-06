# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateProductLicenseDetails(object):
    """
    Updates the product license object (only allows image updates).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateProductLicenseDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param images:
            The value to assign to the images property of this UpdateProductLicenseDetails.
        :type images: list[oci.license_manager.models.ImageDetails]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateProductLicenseDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateProductLicenseDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'images': 'list[ImageDetails]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'images': 'images',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._images = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def images(self):
        """
        **[Required]** Gets the images of this UpdateProductLicenseDetails.
        The image details associated with the product license.


        :return: The images of this UpdateProductLicenseDetails.
        :rtype: list[oci.license_manager.models.ImageDetails]
        """
        return self._images

    @images.setter
    def images(self, images):
        """
        Sets the images of this UpdateProductLicenseDetails.
        The image details associated with the product license.


        :param images: The images of this UpdateProductLicenseDetails.
        :type: list[oci.license_manager.models.ImageDetails]
        """
        self._images = images

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateProductLicenseDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateProductLicenseDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateProductLicenseDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateProductLicenseDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateProductLicenseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateProductLicenseDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateProductLicenseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateProductLicenseDetails.
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
