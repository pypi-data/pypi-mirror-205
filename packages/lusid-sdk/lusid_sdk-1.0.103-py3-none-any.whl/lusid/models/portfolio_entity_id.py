# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.103
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class PortfolioEntityId(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'scope': 'str',
        'code': 'str',
        'portfolio_entity_type': 'str'
    }

    attribute_map = {
        'scope': 'scope',
        'code': 'code',
        'portfolio_entity_type': 'portfolioEntityType'
    }

    required_map = {
        'scope': 'optional',
        'code': 'optional',
        'portfolio_entity_type': 'optional'
    }

    def __init__(self, scope=None, code=None, portfolio_entity_type=None, local_vars_configuration=None):  # noqa: E501
        """PortfolioEntityId - a model defined in OpenAPI"
        
        :param scope:  The scope within which the portfolio or portfolio group lives.
        :type scope: str
        :param code:  Portfolio name or code.
        :type code: str
        :param portfolio_entity_type:  String identifier for portfolio e.g. \"SinglePortfolio\" and \"GroupPortfolio\". If not specified, it is assumed to be a single portfolio.
        :type portfolio_entity_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._scope = None
        self._code = None
        self._portfolio_entity_type = None
        self.discriminator = None

        self.scope = scope
        self.code = code
        self.portfolio_entity_type = portfolio_entity_type

    @property
    def scope(self):
        """Gets the scope of this PortfolioEntityId.  # noqa: E501

        The scope within which the portfolio or portfolio group lives.  # noqa: E501

        :return: The scope of this PortfolioEntityId.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this PortfolioEntityId.

        The scope within which the portfolio or portfolio group lives.  # noqa: E501

        :param scope: The scope of this PortfolioEntityId.  # noqa: E501
        :type scope: str
        """
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) > 256):
            raise ValueError("Invalid value for `scope`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) < 1):
            raise ValueError("Invalid value for `scope`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', scope)):  # noqa: E501
            raise ValueError(r"Invalid value for `scope`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._scope = scope

    @property
    def code(self):
        """Gets the code of this PortfolioEntityId.  # noqa: E501

        Portfolio name or code.  # noqa: E501

        :return: The code of this PortfolioEntityId.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this PortfolioEntityId.

        Portfolio name or code.  # noqa: E501

        :param code: The code of this PortfolioEntityId.  # noqa: E501
        :type code: str
        """
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) > 256):
            raise ValueError("Invalid value for `code`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) < 1):
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', code)):  # noqa: E501
            raise ValueError(r"Invalid value for `code`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._code = code

    @property
    def portfolio_entity_type(self):
        """Gets the portfolio_entity_type of this PortfolioEntityId.  # noqa: E501

        String identifier for portfolio e.g. \"SinglePortfolio\" and \"GroupPortfolio\". If not specified, it is assumed to be a single portfolio.  # noqa: E501

        :return: The portfolio_entity_type of this PortfolioEntityId.  # noqa: E501
        :rtype: str
        """
        return self._portfolio_entity_type

    @portfolio_entity_type.setter
    def portfolio_entity_type(self, portfolio_entity_type):
        """Sets the portfolio_entity_type of this PortfolioEntityId.

        String identifier for portfolio e.g. \"SinglePortfolio\" and \"GroupPortfolio\". If not specified, it is assumed to be a single portfolio.  # noqa: E501

        :param portfolio_entity_type: The portfolio_entity_type of this PortfolioEntityId.  # noqa: E501
        :type portfolio_entity_type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                portfolio_entity_type is not None and len(portfolio_entity_type) > 128):
            raise ValueError("Invalid value for `portfolio_entity_type`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                portfolio_entity_type is not None and len(portfolio_entity_type) < 0):
            raise ValueError("Invalid value for `portfolio_entity_type`, length must be greater than or equal to `0`")  # noqa: E501

        self._portfolio_entity_type = portfolio_entity_type

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PortfolioEntityId):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PortfolioEntityId):
            return True

        return self.to_dict() != other.to_dict()
