# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CustomProtectionRule(object):
    """
    The details of a custom protection rule.
    """

    #: A constant which can be used with the lifecycle_state property of a CustomProtectionRule.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a CustomProtectionRule.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a CustomProtectionRule.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a CustomProtectionRule.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a CustomProtectionRule.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a CustomProtectionRule.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new CustomProtectionRule object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this CustomProtectionRule.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CustomProtectionRule.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CustomProtectionRule.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CustomProtectionRule.
        :type description: str

        :param mod_security_rule_ids:
            The value to assign to the mod_security_rule_ids property of this CustomProtectionRule.
        :type mod_security_rule_ids: list[str]

        :param template:
            The value to assign to the template property of this CustomProtectionRule.
        :type template: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this CustomProtectionRule.
            Allowed values for this property are: "CREATING", "ACTIVE", "FAILED", "UPDATING", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this CustomProtectionRule.
        :type time_created: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CustomProtectionRule.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CustomProtectionRule.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'mod_security_rule_ids': 'list[str]',
            'template': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'mod_security_rule_ids': 'modSecurityRuleIds',
            'template': 'template',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._mod_security_rule_ids = None
        self._template = None
        self._lifecycle_state = None
        self._time_created = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        Gets the id of this CustomProtectionRule.
        The `OCID`__ of the custom protection rule.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this CustomProtectionRule.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CustomProtectionRule.
        The `OCID`__ of the custom protection rule.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this CustomProtectionRule.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this CustomProtectionRule.
        The `OCID`__ of the custom protection rule's compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CustomProtectionRule.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CustomProtectionRule.
        The `OCID`__ of the custom protection rule's compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CustomProtectionRule.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CustomProtectionRule.
        The user-friendly name of the custom protection rule.


        :return: The display_name of this CustomProtectionRule.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CustomProtectionRule.
        The user-friendly name of the custom protection rule.


        :param display_name: The display_name of this CustomProtectionRule.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this CustomProtectionRule.
        The description of the custom protection rule.


        :return: The description of this CustomProtectionRule.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CustomProtectionRule.
        The description of the custom protection rule.


        :param description: The description of this CustomProtectionRule.
        :type: str
        """
        self._description = description

    @property
    def mod_security_rule_ids(self):
        """
        Gets the mod_security_rule_ids of this CustomProtectionRule.
        The auto-generated ID for the custom protection rule. These IDs are referenced in logs.


        :return: The mod_security_rule_ids of this CustomProtectionRule.
        :rtype: list[str]
        """
        return self._mod_security_rule_ids

    @mod_security_rule_ids.setter
    def mod_security_rule_ids(self, mod_security_rule_ids):
        """
        Sets the mod_security_rule_ids of this CustomProtectionRule.
        The auto-generated ID for the custom protection rule. These IDs are referenced in logs.


        :param mod_security_rule_ids: The mod_security_rule_ids of this CustomProtectionRule.
        :type: list[str]
        """
        self._mod_security_rule_ids = mod_security_rule_ids

    @property
    def template(self):
        """
        Gets the template of this CustomProtectionRule.
        The template text of the custom protection rule. All custom protection rules are expressed in ModSecurity Rule Language.

        Additionally, each rule must include two placeholder variables that are updated by the WAF service upon publication of the rule.

        `id: {{id_1}}` - This field is populated with a unique rule ID generated by the WAF service which identifies a `SecRule`. More than one `SecRule` can be defined in the `template` field of a CreateCustomSecurityRule call. The value of the first `SecRule` must be `id: {{id_1}}` and the `id` field of each subsequent `SecRule` should increase by one, as shown in the example.

        `ctl:ruleEngine={{mode}}` - The action to be taken when the criteria of the `SecRule` are met, either `OFF`, `DETECT` or `BLOCK`. This field is automatically populated with the corresponding value of the `action` field of the `CustomProtectionRuleSetting` schema when the `WafConfig` is updated.

        *Example:*
          ```
          SecRule REQUEST_COOKIES \"regex matching SQL injection - part 1/2\" \\
                  \"phase:2,                                                 \\
                  msg:'Detects chained SQL injection attempts 1/2.',        \\
                  id: {{id_1}},                                             \\
                  ctl:ruleEngine={{mode}},                                  \\
                  deny\"
          SecRule REQUEST_COOKIES \"regex matching SQL injection - part 2/2\" \\
                  \"phase:2,                                                 \\
                  msg:'Detects chained SQL injection attempts 2/2.',        \\
                  id: {{id_2}},                                             \\
                  ctl:ruleEngine={{mode}},                                  \\
                  deny\"
          ```


        The example contains two `SecRules` each having distinct regex expression to match the `Cookie` header value during the second input analysis phase.

        For more information about custom protection rules, see `Custom Protection Rules`__.

        For more information about ModSecurity syntax, see `Making Rules: The Basic Syntax`__.

        For more information about ModSecurity's open source WAF rules, see `Mod Security's OWASP Core Rule Set documentation`__.

        __ https://docs.cloud.oracle.com/Content/WAF/Tasks/customprotectionrules.htm
        __ https://www.modsecurity.org/CRS/Documentation/making.html
        __ https://www.modsecurity.org/CRS/Documentation/index.html


        :return: The template of this CustomProtectionRule.
        :rtype: str
        """
        return self._template

    @template.setter
    def template(self, template):
        """
        Sets the template of this CustomProtectionRule.
        The template text of the custom protection rule. All custom protection rules are expressed in ModSecurity Rule Language.

        Additionally, each rule must include two placeholder variables that are updated by the WAF service upon publication of the rule.

        `id: {{id_1}}` - This field is populated with a unique rule ID generated by the WAF service which identifies a `SecRule`. More than one `SecRule` can be defined in the `template` field of a CreateCustomSecurityRule call. The value of the first `SecRule` must be `id: {{id_1}}` and the `id` field of each subsequent `SecRule` should increase by one, as shown in the example.

        `ctl:ruleEngine={{mode}}` - The action to be taken when the criteria of the `SecRule` are met, either `OFF`, `DETECT` or `BLOCK`. This field is automatically populated with the corresponding value of the `action` field of the `CustomProtectionRuleSetting` schema when the `WafConfig` is updated.

        *Example:*
          ```
          SecRule REQUEST_COOKIES \"regex matching SQL injection - part 1/2\" \\
                  \"phase:2,                                                 \\
                  msg:'Detects chained SQL injection attempts 1/2.',        \\
                  id: {{id_1}},                                             \\
                  ctl:ruleEngine={{mode}},                                  \\
                  deny\"
          SecRule REQUEST_COOKIES \"regex matching SQL injection - part 2/2\" \\
                  \"phase:2,                                                 \\
                  msg:'Detects chained SQL injection attempts 2/2.',        \\
                  id: {{id_2}},                                             \\
                  ctl:ruleEngine={{mode}},                                  \\
                  deny\"
          ```


        The example contains two `SecRules` each having distinct regex expression to match the `Cookie` header value during the second input analysis phase.

        For more information about custom protection rules, see `Custom Protection Rules`__.

        For more information about ModSecurity syntax, see `Making Rules: The Basic Syntax`__.

        For more information about ModSecurity's open source WAF rules, see `Mod Security's OWASP Core Rule Set documentation`__.

        __ https://docs.cloud.oracle.com/Content/WAF/Tasks/customprotectionrules.htm
        __ https://www.modsecurity.org/CRS/Documentation/making.html
        __ https://www.modsecurity.org/CRS/Documentation/index.html


        :param template: The template of this CustomProtectionRule.
        :type: str
        """
        self._template = template

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this CustomProtectionRule.
        The current lifecycle state of the custom protection rule.

        Allowed values for this property are: "CREATING", "ACTIVE", "FAILED", "UPDATING", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this CustomProtectionRule.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this CustomProtectionRule.
        The current lifecycle state of the custom protection rule.


        :param lifecycle_state: The lifecycle_state of this CustomProtectionRule.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "FAILED", "UPDATING", "DELETING", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        Gets the time_created of this CustomProtectionRule.
        The date and time the protection rule was created, expressed in RFC 3339 timestamp format.


        :return: The time_created of this CustomProtectionRule.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this CustomProtectionRule.
        The date and time the protection rule was created, expressed in RFC 3339 timestamp format.


        :param time_created: The time_created of this CustomProtectionRule.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CustomProtectionRule.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CustomProtectionRule.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CustomProtectionRule.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CustomProtectionRule.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CustomProtectionRule.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CustomProtectionRule.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CustomProtectionRule.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CustomProtectionRule.
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
