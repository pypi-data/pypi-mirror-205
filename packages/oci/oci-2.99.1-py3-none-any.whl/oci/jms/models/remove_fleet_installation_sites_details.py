# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RemoveFleetInstallationSitesDetails(object):
    """
    The list of Java installation sites to remove.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RemoveFleetInstallationSitesDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param installation_sites:
            The value to assign to the installation_sites property of this RemoveFleetInstallationSitesDetails.
        :type installation_sites: list[oci.jms.models.ExistingInstallationSiteId]

        """
        self.swagger_types = {
            'installation_sites': 'list[ExistingInstallationSiteId]'
        }

        self.attribute_map = {
            'installation_sites': 'installationSites'
        }

        self._installation_sites = None

    @property
    def installation_sites(self):
        """
        **[Required]** Gets the installation_sites of this RemoveFleetInstallationSitesDetails.
        The list of installation sites to remove.


        :return: The installation_sites of this RemoveFleetInstallationSitesDetails.
        :rtype: list[oci.jms.models.ExistingInstallationSiteId]
        """
        return self._installation_sites

    @installation_sites.setter
    def installation_sites(self, installation_sites):
        """
        Sets the installation_sites of this RemoveFleetInstallationSitesDetails.
        The list of installation sites to remove.


        :param installation_sites: The installation_sites of this RemoveFleetInstallationSitesDetails.
        :type: list[oci.jms.models.ExistingInstallationSiteId]
        """
        self._installation_sites = installation_sites

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
