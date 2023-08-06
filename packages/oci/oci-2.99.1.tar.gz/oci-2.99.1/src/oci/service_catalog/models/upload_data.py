# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UploadData(object):
    """
    The model for uploaded binary data, like logos and images.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UploadData object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UploadData.
        :type display_name: str

        :param content_url:
            The value to assign to the content_url property of this UploadData.
        :type content_url: str

        :param mime_type:
            The value to assign to the mime_type property of this UploadData.
        :type mime_type: str

        """
        self.swagger_types = {
            'display_name': 'str',
            'content_url': 'str',
            'mime_type': 'str'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'content_url': 'contentUrl',
            'mime_type': 'mimeType'
        }

        self._display_name = None
        self._content_url = None
        self._mime_type = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UploadData.
        The name used to refer to the uploaded data.


        :return: The display_name of this UploadData.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UploadData.
        The name used to refer to the uploaded data.


        :param display_name: The display_name of this UploadData.
        :type: str
        """
        self._display_name = display_name

    @property
    def content_url(self):
        """
        Gets the content_url of this UploadData.
        The content URL of the uploaded data.


        :return: The content_url of this UploadData.
        :rtype: str
        """
        return self._content_url

    @content_url.setter
    def content_url(self, content_url):
        """
        Sets the content_url of this UploadData.
        The content URL of the uploaded data.


        :param content_url: The content_url of this UploadData.
        :type: str
        """
        self._content_url = content_url

    @property
    def mime_type(self):
        """
        Gets the mime_type of this UploadData.
        The MIME type of the uploaded data.


        :return: The mime_type of this UploadData.
        :rtype: str
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type):
        """
        Sets the mime_type of this UploadData.
        The MIME type of the uploaded data.


        :param mime_type: The mime_type of this UploadData.
        :type: str
        """
        self._mime_type = mime_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
