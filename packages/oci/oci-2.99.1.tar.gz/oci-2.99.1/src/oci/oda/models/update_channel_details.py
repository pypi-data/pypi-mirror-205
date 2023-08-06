# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateChannelDetails(object):
    """
    Properties to update a Channel.
    """

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "ANDROID"
    TYPE_ANDROID = "ANDROID"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "APPEVENT"
    TYPE_APPEVENT = "APPEVENT"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "APPLICATION"
    TYPE_APPLICATION = "APPLICATION"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "CORTANA"
    TYPE_CORTANA = "CORTANA"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "FACEBOOK"
    TYPE_FACEBOOK = "FACEBOOK"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "IOS"
    TYPE_IOS = "IOS"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "MSTEAMS"
    TYPE_MSTEAMS = "MSTEAMS"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "OSS"
    TYPE_OSS = "OSS"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "OSVC"
    TYPE_OSVC = "OSVC"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "SERVICECLOUD"
    TYPE_SERVICECLOUD = "SERVICECLOUD"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "SLACK"
    TYPE_SLACK = "SLACK"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "TEST"
    TYPE_TEST = "TEST"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "TWILIO"
    TYPE_TWILIO = "TWILIO"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "WEB"
    TYPE_WEB = "WEB"

    #: A constant which can be used with the type property of a UpdateChannelDetails.
    #: This constant has a value of "WEBHOOK"
    TYPE_WEBHOOK = "WEBHOOK"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateChannelDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.oda.models.UpdateOsvcChannelDetails`
        * :class:`~oci.oda.models.UpdateOSSChannelDetails`
        * :class:`~oci.oda.models.UpdateAndroidChannelDetails`
        * :class:`~oci.oda.models.UpdateMSTeamsChannelDetails`
        * :class:`~oci.oda.models.UpdateAppEventChannelDetails`
        * :class:`~oci.oda.models.UpdateWebChannelDetails`
        * :class:`~oci.oda.models.UpdateIosChannelDetails`
        * :class:`~oci.oda.models.UpdateSlackChannelDetails`
        * :class:`~oci.oda.models.UpdateServiceCloudChannelDetails`
        * :class:`~oci.oda.models.UpdateTwilioChannelDetails`
        * :class:`~oci.oda.models.UpdateWebhookChannelDetails`
        * :class:`~oci.oda.models.UpdateApplicationChannelDetails`
        * :class:`~oci.oda.models.UpdateFacebookChannelDetails`
        * :class:`~oci.oda.models.UpdateCortanaChannelDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this UpdateChannelDetails.
        :type name: str

        :param description:
            The value to assign to the description property of this UpdateChannelDetails.
        :type description: str

        :param type:
            The value to assign to the type property of this UpdateChannelDetails.
            Allowed values for this property are: "ANDROID", "APPEVENT", "APPLICATION", "CORTANA", "FACEBOOK", "IOS", "MSTEAMS", "OSS", "OSVC", "SERVICECLOUD", "SLACK", "TEST", "TWILIO", "WEB", "WEBHOOK"
        :type type: str

        :param session_expiry_duration_in_milliseconds:
            The value to assign to the session_expiry_duration_in_milliseconds property of this UpdateChannelDetails.
        :type session_expiry_duration_in_milliseconds: int

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateChannelDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateChannelDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'type': 'str',
            'session_expiry_duration_in_milliseconds': 'int',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'type': 'type',
            'session_expiry_duration_in_milliseconds': 'sessionExpiryDurationInMilliseconds',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._name = None
        self._description = None
        self._type = None
        self._session_expiry_duration_in_milliseconds = None
        self._freeform_tags = None
        self._defined_tags = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'OSVC':
            return 'UpdateOsvcChannelDetails'

        if type == 'OSS':
            return 'UpdateOSSChannelDetails'

        if type == 'ANDROID':
            return 'UpdateAndroidChannelDetails'

        if type == 'MSTEAMS':
            return 'UpdateMSTeamsChannelDetails'

        if type == 'APPEVENT':
            return 'UpdateAppEventChannelDetails'

        if type == 'WEB':
            return 'UpdateWebChannelDetails'

        if type == 'IOS':
            return 'UpdateIosChannelDetails'

        if type == 'SLACK':
            return 'UpdateSlackChannelDetails'

        if type == 'SERVICECLOUD':
            return 'UpdateServiceCloudChannelDetails'

        if type == 'TWILIO':
            return 'UpdateTwilioChannelDetails'

        if type == 'WEBHOOK':
            return 'UpdateWebhookChannelDetails'

        if type == 'APPLICATION':
            return 'UpdateApplicationChannelDetails'

        if type == 'FACEBOOK':
            return 'UpdateFacebookChannelDetails'

        if type == 'CORTANA':
            return 'UpdateCortanaChannelDetails'
        else:
            return 'UpdateChannelDetails'

    @property
    def name(self):
        """
        Gets the name of this UpdateChannelDetails.
        The Channel's name. The name can contain only letters, numbers, periods, and underscores. The name must begin with a letter.


        :return: The name of this UpdateChannelDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UpdateChannelDetails.
        The Channel's name. The name can contain only letters, numbers, periods, and underscores. The name must begin with a letter.


        :param name: The name of this UpdateChannelDetails.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this UpdateChannelDetails.
        A short description of the Channel.


        :return: The description of this UpdateChannelDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateChannelDetails.
        A short description of the Channel.


        :param description: The description of this UpdateChannelDetails.
        :type: str
        """
        self._description = description

    @property
    def type(self):
        """
        **[Required]** Gets the type of this UpdateChannelDetails.
        The Channel type.

        Allowed values for this property are: "ANDROID", "APPEVENT", "APPLICATION", "CORTANA", "FACEBOOK", "IOS", "MSTEAMS", "OSS", "OSVC", "SERVICECLOUD", "SLACK", "TEST", "TWILIO", "WEB", "WEBHOOK"


        :return: The type of this UpdateChannelDetails.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UpdateChannelDetails.
        The Channel type.


        :param type: The type of this UpdateChannelDetails.
        :type: str
        """
        allowed_values = ["ANDROID", "APPEVENT", "APPLICATION", "CORTANA", "FACEBOOK", "IOS", "MSTEAMS", "OSS", "OSVC", "SERVICECLOUD", "SLACK", "TEST", "TWILIO", "WEB", "WEBHOOK"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            raise ValueError(
                "Invalid value for `type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._type = type

    @property
    def session_expiry_duration_in_milliseconds(self):
        """
        Gets the session_expiry_duration_in_milliseconds of this UpdateChannelDetails.
        The number of milliseconds before a session expires.


        :return: The session_expiry_duration_in_milliseconds of this UpdateChannelDetails.
        :rtype: int
        """
        return self._session_expiry_duration_in_milliseconds

    @session_expiry_duration_in_milliseconds.setter
    def session_expiry_duration_in_milliseconds(self, session_expiry_duration_in_milliseconds):
        """
        Sets the session_expiry_duration_in_milliseconds of this UpdateChannelDetails.
        The number of milliseconds before a session expires.


        :param session_expiry_duration_in_milliseconds: The session_expiry_duration_in_milliseconds of this UpdateChannelDetails.
        :type: int
        """
        self._session_expiry_duration_in_milliseconds = session_expiry_duration_in_milliseconds

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateChannelDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateChannelDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateChannelDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateChannelDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateChannelDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateChannelDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateChannelDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateChannelDetails.
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
