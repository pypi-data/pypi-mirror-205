# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DocumentDetails(object):
    """
    The details of a document to analyze.
    """

    #: A constant which can be used with the source property of a DocumentDetails.
    #: This constant has a value of "INLINE"
    SOURCE_INLINE = "INLINE"

    #: A constant which can be used with the source property of a DocumentDetails.
    #: This constant has a value of "OBJECT_STORAGE"
    SOURCE_OBJECT_STORAGE = "OBJECT_STORAGE"

    def __init__(self, **kwargs):
        """
        Initializes a new DocumentDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.ai_vision.models.ObjectStorageDocumentDetails`
        * :class:`~oci.ai_vision.models.InlineDocumentDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source:
            The value to assign to the source property of this DocumentDetails.
            Allowed values for this property are: "INLINE", "OBJECT_STORAGE"
        :type source: str

        """
        self.swagger_types = {
            'source': 'str'
        }

        self.attribute_map = {
            'source': 'source'
        }

        self._source = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['source']

        if type == 'OBJECT_STORAGE':
            return 'ObjectStorageDocumentDetails'

        if type == 'INLINE':
            return 'InlineDocumentDetails'
        else:
            return 'DocumentDetails'

    @property
    def source(self):
        """
        **[Required]** Gets the source of this DocumentDetails.
        The location of the document data.
        The allowed values are:
        - `INLINE`: The data is included directly in the request payload.
        - `OBJECT_STORAGE`: The document is in OCI Object Storage.

        Allowed values for this property are: "INLINE", "OBJECT_STORAGE"


        :return: The source of this DocumentDetails.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this DocumentDetails.
        The location of the document data.
        The allowed values are:
        - `INLINE`: The data is included directly in the request payload.
        - `OBJECT_STORAGE`: The document is in OCI Object Storage.


        :param source: The source of this DocumentDetails.
        :type: str
        """
        allowed_values = ["INLINE", "OBJECT_STORAGE"]
        if not value_allowed_none_or_none_sentinel(source, allowed_values):
            raise ValueError(
                "Invalid value for `source`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._source = source

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
