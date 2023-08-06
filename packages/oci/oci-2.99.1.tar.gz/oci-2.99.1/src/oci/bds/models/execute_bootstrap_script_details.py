# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExecuteBootstrapScriptDetails(object):
    """
    The information about the bootstrap script to be executed.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExecuteBootstrapScriptDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param cluster_admin_password:
            The value to assign to the cluster_admin_password property of this ExecuteBootstrapScriptDetails.
        :type cluster_admin_password: str

        :param bootstrap_script_url:
            The value to assign to the bootstrap_script_url property of this ExecuteBootstrapScriptDetails.
        :type bootstrap_script_url: str

        """
        self.swagger_types = {
            'cluster_admin_password': 'str',
            'bootstrap_script_url': 'str'
        }

        self.attribute_map = {
            'cluster_admin_password': 'clusterAdminPassword',
            'bootstrap_script_url': 'bootstrapScriptUrl'
        }

        self._cluster_admin_password = None
        self._bootstrap_script_url = None

    @property
    def cluster_admin_password(self):
        """
        **[Required]** Gets the cluster_admin_password of this ExecuteBootstrapScriptDetails.
        Base-64 encoded password for the cluster admin user.


        :return: The cluster_admin_password of this ExecuteBootstrapScriptDetails.
        :rtype: str
        """
        return self._cluster_admin_password

    @cluster_admin_password.setter
    def cluster_admin_password(self, cluster_admin_password):
        """
        Sets the cluster_admin_password of this ExecuteBootstrapScriptDetails.
        Base-64 encoded password for the cluster admin user.


        :param cluster_admin_password: The cluster_admin_password of this ExecuteBootstrapScriptDetails.
        :type: str
        """
        self._cluster_admin_password = cluster_admin_password

    @property
    def bootstrap_script_url(self):
        """
        Gets the bootstrap_script_url of this ExecuteBootstrapScriptDetails.
        pre-authenticated URL of the bootstrap script in Object Store that can be downloaded and executed.


        :return: The bootstrap_script_url of this ExecuteBootstrapScriptDetails.
        :rtype: str
        """
        return self._bootstrap_script_url

    @bootstrap_script_url.setter
    def bootstrap_script_url(self, bootstrap_script_url):
        """
        Sets the bootstrap_script_url of this ExecuteBootstrapScriptDetails.
        pre-authenticated URL of the bootstrap script in Object Store that can be downloaded and executed.


        :param bootstrap_script_url: The bootstrap_script_url of this ExecuteBootstrapScriptDetails.
        :type: str
        """
        self._bootstrap_script_url = bootstrap_script_url

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
