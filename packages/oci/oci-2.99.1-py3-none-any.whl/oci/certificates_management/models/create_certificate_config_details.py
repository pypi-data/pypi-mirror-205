# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateCertificateConfigDetails(object):
    """
    The details of the contents of the certificate and certificate metadata.
    """

    #: A constant which can be used with the config_type property of a CreateCertificateConfigDetails.
    #: This constant has a value of "ISSUED_BY_INTERNAL_CA"
    CONFIG_TYPE_ISSUED_BY_INTERNAL_CA = "ISSUED_BY_INTERNAL_CA"

    #: A constant which can be used with the config_type property of a CreateCertificateConfigDetails.
    #: This constant has a value of "MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA"
    CONFIG_TYPE_MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA = "MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA"

    #: A constant which can be used with the config_type property of a CreateCertificateConfigDetails.
    #: This constant has a value of "IMPORTED"
    CONFIG_TYPE_IMPORTED = "IMPORTED"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateCertificateConfigDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.certificates_management.models.CreateCertificateManagedExternallyIssuedByInternalCaConfigDetails`
        * :class:`~oci.certificates_management.models.CreateCertificateIssuedByInternalCaConfigDetails`
        * :class:`~oci.certificates_management.models.CreateCertificateByImportingConfigDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_type:
            The value to assign to the config_type property of this CreateCertificateConfigDetails.
            Allowed values for this property are: "ISSUED_BY_INTERNAL_CA", "MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA", "IMPORTED"
        :type config_type: str

        :param version_name:
            The value to assign to the version_name property of this CreateCertificateConfigDetails.
        :type version_name: str

        """
        self.swagger_types = {
            'config_type': 'str',
            'version_name': 'str'
        }

        self.attribute_map = {
            'config_type': 'configType',
            'version_name': 'versionName'
        }

        self._config_type = None
        self._version_name = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['configType']

        if type == 'MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA':
            return 'CreateCertificateManagedExternallyIssuedByInternalCaConfigDetails'

        if type == 'ISSUED_BY_INTERNAL_CA':
            return 'CreateCertificateIssuedByInternalCaConfigDetails'

        if type == 'IMPORTED':
            return 'CreateCertificateByImportingConfigDetails'
        else:
            return 'CreateCertificateConfigDetails'

    @property
    def config_type(self):
        """
        **[Required]** Gets the config_type of this CreateCertificateConfigDetails.
        The origin of the certificate.

        Allowed values for this property are: "ISSUED_BY_INTERNAL_CA", "MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA", "IMPORTED"


        :return: The config_type of this CreateCertificateConfigDetails.
        :rtype: str
        """
        return self._config_type

    @config_type.setter
    def config_type(self, config_type):
        """
        Sets the config_type of this CreateCertificateConfigDetails.
        The origin of the certificate.


        :param config_type: The config_type of this CreateCertificateConfigDetails.
        :type: str
        """
        allowed_values = ["ISSUED_BY_INTERNAL_CA", "MANAGED_EXTERNALLY_ISSUED_BY_INTERNAL_CA", "IMPORTED"]
        if not value_allowed_none_or_none_sentinel(config_type, allowed_values):
            raise ValueError(
                "Invalid value for `config_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._config_type = config_type

    @property
    def version_name(self):
        """
        Gets the version_name of this CreateCertificateConfigDetails.
        A name for the certificate. When the value is not null, a name is unique across versions of a given certificate.


        :return: The version_name of this CreateCertificateConfigDetails.
        :rtype: str
        """
        return self._version_name

    @version_name.setter
    def version_name(self, version_name):
        """
        Sets the version_name of this CreateCertificateConfigDetails.
        A name for the certificate. When the value is not null, a name is unique across versions of a given certificate.


        :param version_name: The version_name of this CreateCertificateConfigDetails.
        :type: str
        """
        self._version_name = version_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
