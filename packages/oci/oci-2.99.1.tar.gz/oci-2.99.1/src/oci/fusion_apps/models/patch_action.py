# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .action import Action
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PatchAction(Action):
    """
    Monthly patch details.
    """

    #: A constant which can be used with the mode property of a PatchAction.
    #: This constant has a value of "HOT"
    MODE_HOT = "HOT"

    #: A constant which can be used with the mode property of a PatchAction.
    #: This constant has a value of "COLD"
    MODE_COLD = "COLD"

    #: A constant which can be used with the category property of a PatchAction.
    #: This constant has a value of "MONTHLY"
    CATEGORY_MONTHLY = "MONTHLY"

    #: A constant which can be used with the category property of a PatchAction.
    #: This constant has a value of "WEEKLY"
    CATEGORY_WEEKLY = "WEEKLY"

    #: A constant which can be used with the category property of a PatchAction.
    #: This constant has a value of "ONEOFF"
    CATEGORY_ONEOFF = "ONEOFF"

    def __init__(self, **kwargs):
        """
        Initializes a new PatchAction object with values from keyword arguments. The default value of the :py:attr:`~oci.fusion_apps.models.PatchAction.action_type` attribute
        of this class is ``PATCH`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param reference_key:
            The value to assign to the reference_key property of this PatchAction.
        :type reference_key: str

        :param action_type:
            The value to assign to the action_type property of this PatchAction.
            Allowed values for this property are: "QUARTERLY_UPGRADE", "PATCH", "VERTEX", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action_type: str

        :param state:
            The value to assign to the state property of this PatchAction.
            Allowed values for this property are: "ACCEPTED", "IN_PROGRESS", "SUCCEEDED", "FAILED", "CANCELED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type state: str

        :param description:
            The value to assign to the description property of this PatchAction.
        :type description: str

        :param mode:
            The value to assign to the mode property of this PatchAction.
            Allowed values for this property are: "HOT", "COLD", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type mode: str

        :param category:
            The value to assign to the category property of this PatchAction.
            Allowed values for this property are: "MONTHLY", "WEEKLY", "ONEOFF", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type category: str

        :param artifact:
            The value to assign to the artifact property of this PatchAction.
        :type artifact: str

        """
        self.swagger_types = {
            'reference_key': 'str',
            'action_type': 'str',
            'state': 'str',
            'description': 'str',
            'mode': 'str',
            'category': 'str',
            'artifact': 'str'
        }

        self.attribute_map = {
            'reference_key': 'referenceKey',
            'action_type': 'actionType',
            'state': 'state',
            'description': 'description',
            'mode': 'mode',
            'category': 'category',
            'artifact': 'artifact'
        }

        self._reference_key = None
        self._action_type = None
        self._state = None
        self._description = None
        self._mode = None
        self._category = None
        self._artifact = None
        self._action_type = 'PATCH'

    @property
    def mode(self):
        """
        Gets the mode of this PatchAction.
        A string that describeds whether the change is applied hot or cold

        Allowed values for this property are: "HOT", "COLD", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The mode of this PatchAction.
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the mode of this PatchAction.
        A string that describeds whether the change is applied hot or cold


        :param mode: The mode of this PatchAction.
        :type: str
        """
        allowed_values = ["HOT", "COLD"]
        if not value_allowed_none_or_none_sentinel(mode, allowed_values):
            mode = 'UNKNOWN_ENUM_VALUE'
        self._mode = mode

    @property
    def category(self):
        """
        Gets the category of this PatchAction.
        patch artifact category

        Allowed values for this property are: "MONTHLY", "WEEKLY", "ONEOFF", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The category of this PatchAction.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this PatchAction.
        patch artifact category


        :param category: The category of this PatchAction.
        :type: str
        """
        allowed_values = ["MONTHLY", "WEEKLY", "ONEOFF"]
        if not value_allowed_none_or_none_sentinel(category, allowed_values):
            category = 'UNKNOWN_ENUM_VALUE'
        self._category = category

    @property
    def artifact(self):
        """
        Gets the artifact of this PatchAction.
        patch bundle name


        :return: The artifact of this PatchAction.
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """
        Sets the artifact of this PatchAction.
        patch bundle name


        :param artifact: The artifact of this PatchAction.
        :type: str
        """
        self._artifact = artifact

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
