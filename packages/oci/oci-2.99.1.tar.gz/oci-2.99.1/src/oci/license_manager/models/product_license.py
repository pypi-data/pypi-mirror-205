# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ProductLicense(object):
    """
    The product license details.
    """

    #: A constant which can be used with the status property of a ProductLicense.
    #: This constant has a value of "INCOMPLETE"
    STATUS_INCOMPLETE = "INCOMPLETE"

    #: A constant which can be used with the status property of a ProductLicense.
    #: This constant has a value of "ISSUES_FOUND"
    STATUS_ISSUES_FOUND = "ISSUES_FOUND"

    #: A constant which can be used with the status property of a ProductLicense.
    #: This constant has a value of "WARNING"
    STATUS_WARNING = "WARNING"

    #: A constant which can be used with the status property of a ProductLicense.
    #: This constant has a value of "OK"
    STATUS_OK = "OK"

    #: A constant which can be used with the lifecycle_state property of a ProductLicense.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ProductLicense.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ProductLicense.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the license_unit property of a ProductLicense.
    #: This constant has a value of "OCPU"
    LICENSE_UNIT_OCPU = "OCPU"

    #: A constant which can be used with the license_unit property of a ProductLicense.
    #: This constant has a value of "NAMED_USER_PLUS"
    LICENSE_UNIT_NAMED_USER_PLUS = "NAMED_USER_PLUS"

    #: A constant which can be used with the license_unit property of a ProductLicense.
    #: This constant has a value of "PROCESSORS"
    LICENSE_UNIT_PROCESSORS = "PROCESSORS"

    def __init__(self, **kwargs):
        """
        Initializes a new ProductLicense object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ProductLicense.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ProductLicense.
        :type compartment_id: str

        :param status:
            The value to assign to the status property of this ProductLicense.
            Allowed values for this property are: "INCOMPLETE", "ISSUES_FOUND", "WARNING", "OK", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param status_description:
            The value to assign to the status_description property of this ProductLicense.
        :type status_description: str

        :param total_active_license_unit_count:
            The value to assign to the total_active_license_unit_count property of this ProductLicense.
        :type total_active_license_unit_count: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ProductLicense.
            Allowed values for this property are: "ACTIVE", "INACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param total_license_units_consumed:
            The value to assign to the total_license_units_consumed property of this ProductLicense.
        :type total_license_units_consumed: float

        :param total_license_record_count:
            The value to assign to the total_license_record_count property of this ProductLicense.
        :type total_license_record_count: int

        :param active_license_record_count:
            The value to assign to the active_license_record_count property of this ProductLicense.
        :type active_license_record_count: int

        :param license_unit:
            The value to assign to the license_unit property of this ProductLicense.
            Allowed values for this property are: "OCPU", "NAMED_USER_PLUS", "PROCESSORS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type license_unit: str

        :param is_vendor_oracle:
            The value to assign to the is_vendor_oracle property of this ProductLicense.
        :type is_vendor_oracle: bool

        :param is_over_subscribed:
            The value to assign to the is_over_subscribed property of this ProductLicense.
        :type is_over_subscribed: bool

        :param is_unlimited:
            The value to assign to the is_unlimited property of this ProductLicense.
        :type is_unlimited: bool

        :param display_name:
            The value to assign to the display_name property of this ProductLicense.
        :type display_name: str

        :param vendor_name:
            The value to assign to the vendor_name property of this ProductLicense.
        :type vendor_name: str

        :param time_created:
            The value to assign to the time_created property of this ProductLicense.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ProductLicense.
        :type time_updated: datetime

        :param images:
            The value to assign to the images property of this ProductLicense.
        :type images: list[oci.license_manager.models.ImageResponse]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ProductLicense.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ProductLicense.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this ProductLicense.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'status': 'str',
            'status_description': 'str',
            'total_active_license_unit_count': 'int',
            'lifecycle_state': 'str',
            'total_license_units_consumed': 'float',
            'total_license_record_count': 'int',
            'active_license_record_count': 'int',
            'license_unit': 'str',
            'is_vendor_oracle': 'bool',
            'is_over_subscribed': 'bool',
            'is_unlimited': 'bool',
            'display_name': 'str',
            'vendor_name': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'images': 'list[ImageResponse]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'status': 'status',
            'status_description': 'statusDescription',
            'total_active_license_unit_count': 'totalActiveLicenseUnitCount',
            'lifecycle_state': 'lifecycleState',
            'total_license_units_consumed': 'totalLicenseUnitsConsumed',
            'total_license_record_count': 'totalLicenseRecordCount',
            'active_license_record_count': 'activeLicenseRecordCount',
            'license_unit': 'licenseUnit',
            'is_vendor_oracle': 'isVendorOracle',
            'is_over_subscribed': 'isOverSubscribed',
            'is_unlimited': 'isUnlimited',
            'display_name': 'displayName',
            'vendor_name': 'vendorName',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'images': 'images',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._compartment_id = None
        self._status = None
        self._status_description = None
        self._total_active_license_unit_count = None
        self._lifecycle_state = None
        self._total_license_units_consumed = None
        self._total_license_record_count = None
        self._active_license_record_count = None
        self._license_unit = None
        self._is_vendor_oracle = None
        self._is_over_subscribed = None
        self._is_unlimited = None
        self._display_name = None
        self._vendor_name = None
        self._time_created = None
        self._time_updated = None
        self._images = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ProductLicense.
        The product license `OCID`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this ProductLicense.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProductLicense.
        The product license `OCID`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this ProductLicense.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ProductLicense.
        The compartment `OCID`__ where the product license is created.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ProductLicense.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ProductLicense.
        The compartment `OCID`__ where the product license is created.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ProductLicense.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def status(self):
        """
        **[Required]** Gets the status of this ProductLicense.
        The current product license status.

        Allowed values for this property are: "INCOMPLETE", "ISSUES_FOUND", "WARNING", "OK", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this ProductLicense.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ProductLicense.
        The current product license status.


        :param status: The status of this ProductLicense.
        :type: str
        """
        allowed_values = ["INCOMPLETE", "ISSUES_FOUND", "WARNING", "OK"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def status_description(self):
        """
        Gets the status_description of this ProductLicense.
        Status description for the current product license status.


        :return: The status_description of this ProductLicense.
        :rtype: str
        """
        return self._status_description

    @status_description.setter
    def status_description(self, status_description):
        """
        Sets the status_description of this ProductLicense.
        Status description for the current product license status.


        :param status_description: The status_description of this ProductLicense.
        :type: str
        """
        self._status_description = status_description

    @property
    def total_active_license_unit_count(self):
        """
        Gets the total_active_license_unit_count of this ProductLicense.
        The total number of licenses available for the product license, calculated by adding up all the license counts for active license records associated with the product license.


        :return: The total_active_license_unit_count of this ProductLicense.
        :rtype: int
        """
        return self._total_active_license_unit_count

    @total_active_license_unit_count.setter
    def total_active_license_unit_count(self, total_active_license_unit_count):
        """
        Sets the total_active_license_unit_count of this ProductLicense.
        The total number of licenses available for the product license, calculated by adding up all the license counts for active license records associated with the product license.


        :param total_active_license_unit_count: The total_active_license_unit_count of this ProductLicense.
        :type: int
        """
        self._total_active_license_unit_count = total_active_license_unit_count

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this ProductLicense.
        The current product license state.

        Allowed values for this property are: "ACTIVE", "INACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ProductLicense.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ProductLicense.
        The current product license state.


        :param lifecycle_state: The lifecycle_state of this ProductLicense.
        :type: str
        """
        allowed_values = ["ACTIVE", "INACTIVE", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def total_license_units_consumed(self):
        """
        Gets the total_license_units_consumed of this ProductLicense.
        The number of license units consumed. Updated after each allocation run.


        :return: The total_license_units_consumed of this ProductLicense.
        :rtype: float
        """
        return self._total_license_units_consumed

    @total_license_units_consumed.setter
    def total_license_units_consumed(self, total_license_units_consumed):
        """
        Sets the total_license_units_consumed of this ProductLicense.
        The number of license units consumed. Updated after each allocation run.


        :param total_license_units_consumed: The total_license_units_consumed of this ProductLicense.
        :type: float
        """
        self._total_license_units_consumed = total_license_units_consumed

    @property
    def total_license_record_count(self):
        """
        Gets the total_license_record_count of this ProductLicense.
        The number of license records associated with the product license.


        :return: The total_license_record_count of this ProductLicense.
        :rtype: int
        """
        return self._total_license_record_count

    @total_license_record_count.setter
    def total_license_record_count(self, total_license_record_count):
        """
        Sets the total_license_record_count of this ProductLicense.
        The number of license records associated with the product license.


        :param total_license_record_count: The total_license_record_count of this ProductLicense.
        :type: int
        """
        self._total_license_record_count = total_license_record_count

    @property
    def active_license_record_count(self):
        """
        Gets the active_license_record_count of this ProductLicense.
        The number of active license records associated with the product license.


        :return: The active_license_record_count of this ProductLicense.
        :rtype: int
        """
        return self._active_license_record_count

    @active_license_record_count.setter
    def active_license_record_count(self, active_license_record_count):
        """
        Sets the active_license_record_count of this ProductLicense.
        The number of active license records associated with the product license.


        :param active_license_record_count: The active_license_record_count of this ProductLicense.
        :type: int
        """
        self._active_license_record_count = active_license_record_count

    @property
    def license_unit(self):
        """
        **[Required]** Gets the license_unit of this ProductLicense.
        The product license unit.

        Allowed values for this property are: "OCPU", "NAMED_USER_PLUS", "PROCESSORS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The license_unit of this ProductLicense.
        :rtype: str
        """
        return self._license_unit

    @license_unit.setter
    def license_unit(self, license_unit):
        """
        Sets the license_unit of this ProductLicense.
        The product license unit.


        :param license_unit: The license_unit of this ProductLicense.
        :type: str
        """
        allowed_values = ["OCPU", "NAMED_USER_PLUS", "PROCESSORS"]
        if not value_allowed_none_or_none_sentinel(license_unit, allowed_values):
            license_unit = 'UNKNOWN_ENUM_VALUE'
        self._license_unit = license_unit

    @property
    def is_vendor_oracle(self):
        """
        **[Required]** Gets the is_vendor_oracle of this ProductLicense.
        Specifies whether the vendor is Oracle or a third party.


        :return: The is_vendor_oracle of this ProductLicense.
        :rtype: bool
        """
        return self._is_vendor_oracle

    @is_vendor_oracle.setter
    def is_vendor_oracle(self, is_vendor_oracle):
        """
        Sets the is_vendor_oracle of this ProductLicense.
        Specifies whether the vendor is Oracle or a third party.


        :param is_vendor_oracle: The is_vendor_oracle of this ProductLicense.
        :type: bool
        """
        self._is_vendor_oracle = is_vendor_oracle

    @property
    def is_over_subscribed(self):
        """
        Gets the is_over_subscribed of this ProductLicense.
        Specifies whether or not the product license is oversubscribed.


        :return: The is_over_subscribed of this ProductLicense.
        :rtype: bool
        """
        return self._is_over_subscribed

    @is_over_subscribed.setter
    def is_over_subscribed(self, is_over_subscribed):
        """
        Sets the is_over_subscribed of this ProductLicense.
        Specifies whether or not the product license is oversubscribed.


        :param is_over_subscribed: The is_over_subscribed of this ProductLicense.
        :type: bool
        """
        self._is_over_subscribed = is_over_subscribed

    @property
    def is_unlimited(self):
        """
        Gets the is_unlimited of this ProductLicense.
        Specifies if the license unit count is unlimited.


        :return: The is_unlimited of this ProductLicense.
        :rtype: bool
        """
        return self._is_unlimited

    @is_unlimited.setter
    def is_unlimited(self, is_unlimited):
        """
        Sets the is_unlimited of this ProductLicense.
        Specifies if the license unit count is unlimited.


        :param is_unlimited: The is_unlimited of this ProductLicense.
        :type: bool
        """
        self._is_unlimited = is_unlimited

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ProductLicense.
        License record name


        :return: The display_name of this ProductLicense.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ProductLicense.
        License record name


        :param display_name: The display_name of this ProductLicense.
        :type: str
        """
        self._display_name = display_name

    @property
    def vendor_name(self):
        """
        Gets the vendor_name of this ProductLicense.
        The vendor of the ProductLicense


        :return: The vendor_name of this ProductLicense.
        :rtype: str
        """
        return self._vendor_name

    @vendor_name.setter
    def vendor_name(self, vendor_name):
        """
        Sets the vendor_name of this ProductLicense.
        The vendor of the ProductLicense


        :param vendor_name: The vendor_name of this ProductLicense.
        :type: str
        """
        self._vendor_name = vendor_name

    @property
    def time_created(self):
        """
        Gets the time_created of this ProductLicense.
        The time the product license was created. An `RFC 3339`__-formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this ProductLicense.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ProductLicense.
        The time the product license was created. An `RFC 3339`__-formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this ProductLicense.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ProductLicense.
        The time the product license was updated. An `RFC 3339`__-formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this ProductLicense.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ProductLicense.
        The time the product license was updated. An `RFC 3339`__-formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this ProductLicense.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def images(self):
        """
        Gets the images of this ProductLicense.
        The images associated with the product license.


        :return: The images of this ProductLicense.
        :rtype: list[oci.license_manager.models.ImageResponse]
        """
        return self._images

    @images.setter
    def images(self, images):
        """
        Sets the images of this ProductLicense.
        The images associated with the product license.


        :param images: The images of this ProductLicense.
        :type: list[oci.license_manager.models.ImageResponse]
        """
        self._images = images

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ProductLicense.
        Simple key-value pair that is applied without any predefined name, type, or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this ProductLicense.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ProductLicense.
        Simple key-value pair that is applied without any predefined name, type, or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this ProductLicense.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ProductLicense.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this ProductLicense.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ProductLicense.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this ProductLicense.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this ProductLicense.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this ProductLicense.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this ProductLicense.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this ProductLicense.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
