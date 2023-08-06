# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateVcnDetails(object):
    """
    CreateVcnDetails model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateVcnDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param cidr_block:
            The value to assign to the cidr_block property of this CreateVcnDetails.
        :type cidr_block: str

        :param cidr_blocks:
            The value to assign to the cidr_blocks property of this CreateVcnDetails.
        :type cidr_blocks: list[str]

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateVcnDetails.
        :type compartment_id: str

        :param ipv6_private_cidr_blocks:
            The value to assign to the ipv6_private_cidr_blocks property of this CreateVcnDetails.
        :type ipv6_private_cidr_blocks: list[str]

        :param is_oracle_gua_allocation_enabled:
            The value to assign to the is_oracle_gua_allocation_enabled property of this CreateVcnDetails.
        :type is_oracle_gua_allocation_enabled: bool

        :param byoipv6_cidr_details:
            The value to assign to the byoipv6_cidr_details property of this CreateVcnDetails.
        :type byoipv6_cidr_details: list[oci.core.models.Byoipv6CidrDetails]

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateVcnDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this CreateVcnDetails.
        :type display_name: str

        :param dns_label:
            The value to assign to the dns_label property of this CreateVcnDetails.
        :type dns_label: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateVcnDetails.
        :type freeform_tags: dict(str, str)

        :param is_ipv6_enabled:
            The value to assign to the is_ipv6_enabled property of this CreateVcnDetails.
        :type is_ipv6_enabled: bool

        """
        self.swagger_types = {
            'cidr_block': 'str',
            'cidr_blocks': 'list[str]',
            'compartment_id': 'str',
            'ipv6_private_cidr_blocks': 'list[str]',
            'is_oracle_gua_allocation_enabled': 'bool',
            'byoipv6_cidr_details': 'list[Byoipv6CidrDetails]',
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'dns_label': 'str',
            'freeform_tags': 'dict(str, str)',
            'is_ipv6_enabled': 'bool'
        }

        self.attribute_map = {
            'cidr_block': 'cidrBlock',
            'cidr_blocks': 'cidrBlocks',
            'compartment_id': 'compartmentId',
            'ipv6_private_cidr_blocks': 'ipv6PrivateCidrBlocks',
            'is_oracle_gua_allocation_enabled': 'isOracleGuaAllocationEnabled',
            'byoipv6_cidr_details': 'byoipv6CidrDetails',
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'dns_label': 'dnsLabel',
            'freeform_tags': 'freeformTags',
            'is_ipv6_enabled': 'isIpv6Enabled'
        }

        self._cidr_block = None
        self._cidr_blocks = None
        self._compartment_id = None
        self._ipv6_private_cidr_blocks = None
        self._is_oracle_gua_allocation_enabled = None
        self._byoipv6_cidr_details = None
        self._defined_tags = None
        self._display_name = None
        self._dns_label = None
        self._freeform_tags = None
        self._is_ipv6_enabled = None

    @property
    def cidr_block(self):
        """
        Gets the cidr_block of this CreateVcnDetails.
        **Deprecated.** Do *not* set this value. Use `cidrBlocks` instead.
        Example: `10.0.0.0/16`


        :return: The cidr_block of this CreateVcnDetails.
        :rtype: str
        """
        return self._cidr_block

    @cidr_block.setter
    def cidr_block(self, cidr_block):
        """
        Sets the cidr_block of this CreateVcnDetails.
        **Deprecated.** Do *not* set this value. Use `cidrBlocks` instead.
        Example: `10.0.0.0/16`


        :param cidr_block: The cidr_block of this CreateVcnDetails.
        :type: str
        """
        self._cidr_block = cidr_block

    @property
    def cidr_blocks(self):
        """
        Gets the cidr_blocks of this CreateVcnDetails.
        The list of one or more IPv4 CIDR blocks for the VCN that meet the following criteria:
        - The CIDR blocks must be valid.
        - They must not overlap with each other or with the on-premises network CIDR block.
        - The number of CIDR blocks must not exceed the limit of CIDR blocks allowed per VCN.

        **Important:** Do *not* specify a value for `cidrBlock`. Use this parameter instead.


        :return: The cidr_blocks of this CreateVcnDetails.
        :rtype: list[str]
        """
        return self._cidr_blocks

    @cidr_blocks.setter
    def cidr_blocks(self, cidr_blocks):
        """
        Sets the cidr_blocks of this CreateVcnDetails.
        The list of one or more IPv4 CIDR blocks for the VCN that meet the following criteria:
        - The CIDR blocks must be valid.
        - They must not overlap with each other or with the on-premises network CIDR block.
        - The number of CIDR blocks must not exceed the limit of CIDR blocks allowed per VCN.

        **Important:** Do *not* specify a value for `cidrBlock`. Use this parameter instead.


        :param cidr_blocks: The cidr_blocks of this CreateVcnDetails.
        :type: list[str]
        """
        self._cidr_blocks = cidr_blocks

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateVcnDetails.
        The `OCID`__ of the compartment to contain the VCN.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateVcnDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateVcnDetails.
        The `OCID`__ of the compartment to contain the VCN.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateVcnDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def ipv6_private_cidr_blocks(self):
        """
        Gets the ipv6_private_cidr_blocks of this CreateVcnDetails.
        The list of one or more ULA or Private IPv6 CIDR blocks for the vcn that meets the following criteria:
        - The CIDR blocks must be valid.
        - Multiple CIDR blocks must not overlap each other or the on-premises network CIDR block.
        - The number of CIDR blocks must not exceed the limit of IPv6 CIDR blocks allowed to a vcn.

        **Important:** Do *not* specify a value for `ipv6CidrBlock`. Use this parameter instead.


        :return: The ipv6_private_cidr_blocks of this CreateVcnDetails.
        :rtype: list[str]
        """
        return self._ipv6_private_cidr_blocks

    @ipv6_private_cidr_blocks.setter
    def ipv6_private_cidr_blocks(self, ipv6_private_cidr_blocks):
        """
        Sets the ipv6_private_cidr_blocks of this CreateVcnDetails.
        The list of one or more ULA or Private IPv6 CIDR blocks for the vcn that meets the following criteria:
        - The CIDR blocks must be valid.
        - Multiple CIDR blocks must not overlap each other or the on-premises network CIDR block.
        - The number of CIDR blocks must not exceed the limit of IPv6 CIDR blocks allowed to a vcn.

        **Important:** Do *not* specify a value for `ipv6CidrBlock`. Use this parameter instead.


        :param ipv6_private_cidr_blocks: The ipv6_private_cidr_blocks of this CreateVcnDetails.
        :type: list[str]
        """
        self._ipv6_private_cidr_blocks = ipv6_private_cidr_blocks

    @property
    def is_oracle_gua_allocation_enabled(self):
        """
        Gets the is_oracle_gua_allocation_enabled of this CreateVcnDetails.
        Specifies whether to skip Oracle allocated IPv6 GUA. By default, Oracle will allocate one GUA of /56
        size for an IPv6 enabled VCN.


        :return: The is_oracle_gua_allocation_enabled of this CreateVcnDetails.
        :rtype: bool
        """
        return self._is_oracle_gua_allocation_enabled

    @is_oracle_gua_allocation_enabled.setter
    def is_oracle_gua_allocation_enabled(self, is_oracle_gua_allocation_enabled):
        """
        Sets the is_oracle_gua_allocation_enabled of this CreateVcnDetails.
        Specifies whether to skip Oracle allocated IPv6 GUA. By default, Oracle will allocate one GUA of /56
        size for an IPv6 enabled VCN.


        :param is_oracle_gua_allocation_enabled: The is_oracle_gua_allocation_enabled of this CreateVcnDetails.
        :type: bool
        """
        self._is_oracle_gua_allocation_enabled = is_oracle_gua_allocation_enabled

    @property
    def byoipv6_cidr_details(self):
        """
        Gets the byoipv6_cidr_details of this CreateVcnDetails.
        The list of BYOIPv6 OCIDs and BYOIPv6 CIDR blocks required to create a VCN that uses BYOIPv6 ranges.


        :return: The byoipv6_cidr_details of this CreateVcnDetails.
        :rtype: list[oci.core.models.Byoipv6CidrDetails]
        """
        return self._byoipv6_cidr_details

    @byoipv6_cidr_details.setter
    def byoipv6_cidr_details(self, byoipv6_cidr_details):
        """
        Sets the byoipv6_cidr_details of this CreateVcnDetails.
        The list of BYOIPv6 OCIDs and BYOIPv6 CIDR blocks required to create a VCN that uses BYOIPv6 ranges.


        :param byoipv6_cidr_details: The byoipv6_cidr_details of this CreateVcnDetails.
        :type: list[oci.core.models.Byoipv6CidrDetails]
        """
        self._byoipv6_cidr_details = byoipv6_cidr_details

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateVcnDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateVcnDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateVcnDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateVcnDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateVcnDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :return: The display_name of this CreateVcnDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateVcnDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :param display_name: The display_name of this CreateVcnDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def dns_label(self):
        """
        Gets the dns_label of this CreateVcnDetails.
        A DNS label for the VCN, used in conjunction with the VNIC's hostname and
        subnet's DNS label to form a fully qualified domain name (FQDN) for each VNIC
        within this subnet (for example, `bminstance1.subnet123.vcn1.oraclevcn.com`).
        Not required to be unique, but it's a best practice to set unique DNS labels
        for VCNs in your tenancy. Must be an alphanumeric string that begins with a letter.
        The value cannot be changed.

        You must set this value if you want instances to be able to use hostnames to
        resolve other instances in the VCN. Otherwise the Internet and VCN Resolver
        will not work.

        For more information, see
        `DNS in Your Virtual Cloud Network`__.

        Example: `vcn1`

        __ https://docs.cloud.oracle.com/iaas/Content/Network/Concepts/dns.htm


        :return: The dns_label of this CreateVcnDetails.
        :rtype: str
        """
        return self._dns_label

    @dns_label.setter
    def dns_label(self, dns_label):
        """
        Sets the dns_label of this CreateVcnDetails.
        A DNS label for the VCN, used in conjunction with the VNIC's hostname and
        subnet's DNS label to form a fully qualified domain name (FQDN) for each VNIC
        within this subnet (for example, `bminstance1.subnet123.vcn1.oraclevcn.com`).
        Not required to be unique, but it's a best practice to set unique DNS labels
        for VCNs in your tenancy. Must be an alphanumeric string that begins with a letter.
        The value cannot be changed.

        You must set this value if you want instances to be able to use hostnames to
        resolve other instances in the VCN. Otherwise the Internet and VCN Resolver
        will not work.

        For more information, see
        `DNS in Your Virtual Cloud Network`__.

        Example: `vcn1`

        __ https://docs.cloud.oracle.com/iaas/Content/Network/Concepts/dns.htm


        :param dns_label: The dns_label of this CreateVcnDetails.
        :type: str
        """
        self._dns_label = dns_label

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateVcnDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateVcnDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateVcnDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateVcnDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def is_ipv6_enabled(self):
        """
        Gets the is_ipv6_enabled of this CreateVcnDetails.
        Whether IPv6 is enabled for the VCN. Default is `false`.
        If enabled, Oracle will assign the VCN a IPv6 /56 CIDR block.
        You may skip having Oracle allocate the VCN a IPv6 /56 CIDR block by setting isOracleGuaAllocationEnabled to `false`.
        For important details about IPv6 addressing in a VCN, see `IPv6 Addresses`__.

        Example: `true`

        __ https://docs.cloud.oracle.com/iaas/Content/Network/Concepts/ipv6.htm


        :return: The is_ipv6_enabled of this CreateVcnDetails.
        :rtype: bool
        """
        return self._is_ipv6_enabled

    @is_ipv6_enabled.setter
    def is_ipv6_enabled(self, is_ipv6_enabled):
        """
        Sets the is_ipv6_enabled of this CreateVcnDetails.
        Whether IPv6 is enabled for the VCN. Default is `false`.
        If enabled, Oracle will assign the VCN a IPv6 /56 CIDR block.
        You may skip having Oracle allocate the VCN a IPv6 /56 CIDR block by setting isOracleGuaAllocationEnabled to `false`.
        For important details about IPv6 addressing in a VCN, see `IPv6 Addresses`__.

        Example: `true`

        __ https://docs.cloud.oracle.com/iaas/Content/Network/Concepts/ipv6.htm


        :param is_ipv6_enabled: The is_ipv6_enabled of this CreateVcnDetails.
        :type: bool
        """
        self._is_ipv6_enabled = is_ipv6_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
