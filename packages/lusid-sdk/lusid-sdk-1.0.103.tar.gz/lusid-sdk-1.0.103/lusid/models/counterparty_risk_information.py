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


class CounterpartyRiskInformation(object):
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
        'country_of_risk': 'str',
        'credit_ratings': 'list[CreditRating]',
        'industry_classifiers': 'list[IndustryClassifier]'
    }

    attribute_map = {
        'country_of_risk': 'countryOfRisk',
        'credit_ratings': 'creditRatings',
        'industry_classifiers': 'industryClassifiers'
    }

    required_map = {
        'country_of_risk': 'required',
        'credit_ratings': 'required',
        'industry_classifiers': 'required'
    }

    def __init__(self, country_of_risk=None, credit_ratings=None, industry_classifiers=None, local_vars_configuration=None):  # noqa: E501
        """CounterpartyRiskInformation - a model defined in OpenAPI"
        
        :param country_of_risk:  The country to which one would naturally ascribe risk, typically the legal entity's country of registration. This can be used to infer funding currency and related market data in the absence of a specific preference. (required)
        :type country_of_risk: str
        :param credit_ratings:  (required)
        :type credit_ratings: list[lusid.CreditRating]
        :param industry_classifiers:  (required)
        :type industry_classifiers: list[lusid.IndustryClassifier]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._country_of_risk = None
        self._credit_ratings = None
        self._industry_classifiers = None
        self.discriminator = None

        self.country_of_risk = country_of_risk
        self.credit_ratings = credit_ratings
        self.industry_classifiers = industry_classifiers

    @property
    def country_of_risk(self):
        """Gets the country_of_risk of this CounterpartyRiskInformation.  # noqa: E501

        The country to which one would naturally ascribe risk, typically the legal entity's country of registration. This can be used to infer funding currency and related market data in the absence of a specific preference.  # noqa: E501

        :return: The country_of_risk of this CounterpartyRiskInformation.  # noqa: E501
        :rtype: str
        """
        return self._country_of_risk

    @country_of_risk.setter
    def country_of_risk(self, country_of_risk):
        """Sets the country_of_risk of this CounterpartyRiskInformation.

        The country to which one would naturally ascribe risk, typically the legal entity's country of registration. This can be used to infer funding currency and related market data in the absence of a specific preference.  # noqa: E501

        :param country_of_risk: The country_of_risk of this CounterpartyRiskInformation.  # noqa: E501
        :type country_of_risk: str
        """
        if self.local_vars_configuration.client_side_validation and country_of_risk is None:  # noqa: E501
            raise ValueError("Invalid value for `country_of_risk`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                country_of_risk is not None and len(country_of_risk) > 64):
            raise ValueError("Invalid value for `country_of_risk`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                country_of_risk is not None and len(country_of_risk) < 1):
            raise ValueError("Invalid value for `country_of_risk`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                country_of_risk is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', country_of_risk)):  # noqa: E501
            raise ValueError(r"Invalid value for `country_of_risk`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._country_of_risk = country_of_risk

    @property
    def credit_ratings(self):
        """Gets the credit_ratings of this CounterpartyRiskInformation.  # noqa: E501


        :return: The credit_ratings of this CounterpartyRiskInformation.  # noqa: E501
        :rtype: list[lusid.CreditRating]
        """
        return self._credit_ratings

    @credit_ratings.setter
    def credit_ratings(self, credit_ratings):
        """Sets the credit_ratings of this CounterpartyRiskInformation.


        :param credit_ratings: The credit_ratings of this CounterpartyRiskInformation.  # noqa: E501
        :type credit_ratings: list[lusid.CreditRating]
        """
        if self.local_vars_configuration.client_side_validation and credit_ratings is None:  # noqa: E501
            raise ValueError("Invalid value for `credit_ratings`, must not be `None`")  # noqa: E501

        self._credit_ratings = credit_ratings

    @property
    def industry_classifiers(self):
        """Gets the industry_classifiers of this CounterpartyRiskInformation.  # noqa: E501


        :return: The industry_classifiers of this CounterpartyRiskInformation.  # noqa: E501
        :rtype: list[lusid.IndustryClassifier]
        """
        return self._industry_classifiers

    @industry_classifiers.setter
    def industry_classifiers(self, industry_classifiers):
        """Sets the industry_classifiers of this CounterpartyRiskInformation.


        :param industry_classifiers: The industry_classifiers of this CounterpartyRiskInformation.  # noqa: E501
        :type industry_classifiers: list[lusid.IndustryClassifier]
        """
        if self.local_vars_configuration.client_side_validation and industry_classifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `industry_classifiers`, must not be `None`")  # noqa: E501

        self._industry_classifiers = industry_classifiers

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
        if not isinstance(other, CounterpartyRiskInformation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CounterpartyRiskInformation):
            return True

        return self.to_dict() != other.to_dict()
