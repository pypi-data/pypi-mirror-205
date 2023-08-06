# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .build_runner_shape_config import BuildRunnerShapeConfig
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DefaultBuildRunnerShapeConfig(BuildRunnerShapeConfig):
    """
    Specifies the default build runner shape config.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DefaultBuildRunnerShapeConfig object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.DefaultBuildRunnerShapeConfig.build_runner_type` attribute
        of this class is ``DEFAULT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param build_runner_type:
            The value to assign to the build_runner_type property of this DefaultBuildRunnerShapeConfig.
            Allowed values for this property are: "CUSTOM", "DEFAULT"
        :type build_runner_type: str

        """
        self.swagger_types = {
            'build_runner_type': 'str'
        }

        self.attribute_map = {
            'build_runner_type': 'buildRunnerType'
        }

        self._build_runner_type = None
        self._build_runner_type = 'DEFAULT'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
