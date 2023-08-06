# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RestrictedOperation(object):
    """
    Summary of a restricted operation for a Digital Assistant instance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RestrictedOperation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param operation_name:
            The value to assign to the operation_name property of this RestrictedOperation.
        :type operation_name: str

        :param restricting_service:
            The value to assign to the restricting_service property of this RestrictedOperation.
        :type restricting_service: str

        """
        self.swagger_types = {
            'operation_name': 'str',
            'restricting_service': 'str'
        }

        self.attribute_map = {
            'operation_name': 'operationName',
            'restricting_service': 'restrictingService'
        }

        self._operation_name = None
        self._restricting_service = None

    @property
    def operation_name(self):
        """
        **[Required]** Gets the operation_name of this RestrictedOperation.
        Name of the restricted operation.


        :return: The operation_name of this RestrictedOperation.
        :rtype: str
        """
        return self._operation_name

    @operation_name.setter
    def operation_name(self, operation_name):
        """
        Sets the operation_name of this RestrictedOperation.
        Name of the restricted operation.


        :param operation_name: The operation_name of this RestrictedOperation.
        :type: str
        """
        self._operation_name = operation_name

    @property
    def restricting_service(self):
        """
        **[Required]** Gets the restricting_service of this RestrictedOperation.
        Name of the service restricting the operation.


        :return: The restricting_service of this RestrictedOperation.
        :rtype: str
        """
        return self._restricting_service

    @restricting_service.setter
    def restricting_service(self, restricting_service):
        """
        Sets the restricting_service of this RestrictedOperation.
        Name of the service restricting the operation.


        :param restricting_service: The restricting_service of this RestrictedOperation.
        :type: str
        """
        self._restricting_service = restricting_service

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
