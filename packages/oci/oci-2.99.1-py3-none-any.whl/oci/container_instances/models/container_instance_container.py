# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ContainerInstanceContainer(object):
    """
    A container on a Container Instance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ContainerInstanceContainer object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param container_id:
            The value to assign to the container_id property of this ContainerInstanceContainer.
        :type container_id: str

        :param display_name:
            The value to assign to the display_name property of this ContainerInstanceContainer.
        :type display_name: str

        """
        self.swagger_types = {
            'container_id': 'str',
            'display_name': 'str'
        }

        self.attribute_map = {
            'container_id': 'containerId',
            'display_name': 'displayName'
        }

        self._container_id = None
        self._display_name = None

    @property
    def container_id(self):
        """
        **[Required]** Gets the container_id of this ContainerInstanceContainer.
        The ID of the Container on this Instance.


        :return: The container_id of this ContainerInstanceContainer.
        :rtype: str
        """
        return self._container_id

    @container_id.setter
    def container_id(self, container_id):
        """
        Sets the container_id of this ContainerInstanceContainer.
        The ID of the Container on this Instance.


        :param container_id: The container_id of this ContainerInstanceContainer.
        :type: str
        """
        self._container_id = container_id

    @property
    def display_name(self):
        """
        Gets the display_name of this ContainerInstanceContainer.
        Display name for the Container.


        :return: The display_name of this ContainerInstanceContainer.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ContainerInstanceContainer.
        Display name for the Container.


        :param display_name: The display_name of this ContainerInstanceContainer.
        :type: str
        """
        self._display_name = display_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
