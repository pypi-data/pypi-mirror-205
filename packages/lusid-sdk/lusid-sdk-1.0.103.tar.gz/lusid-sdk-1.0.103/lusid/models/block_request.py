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


class BlockRequest(object):
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
        'id': 'ResourceId',
        'order_ids': 'list[ResourceId]',
        'properties': 'dict(str, PerpetualProperty)',
        'instrument_identifiers': 'dict(str, str)',
        'quantity': 'float',
        'side': 'str',
        'type': 'str',
        'time_in_force': 'str',
        'created_date': 'datetime',
        'limit_price': 'CurrencyAndAmount',
        'stop_price': 'CurrencyAndAmount'
    }

    attribute_map = {
        'id': 'id',
        'order_ids': 'orderIds',
        'properties': 'properties',
        'instrument_identifiers': 'instrumentIdentifiers',
        'quantity': 'quantity',
        'side': 'side',
        'type': 'type',
        'time_in_force': 'timeInForce',
        'created_date': 'createdDate',
        'limit_price': 'limitPrice',
        'stop_price': 'stopPrice'
    }

    required_map = {
        'id': 'required',
        'order_ids': 'required',
        'properties': 'optional',
        'instrument_identifiers': 'required',
        'quantity': 'required',
        'side': 'required',
        'type': 'required',
        'time_in_force': 'required',
        'created_date': 'required',
        'limit_price': 'optional',
        'stop_price': 'optional'
    }

    def __init__(self, id=None, order_ids=None, properties=None, instrument_identifiers=None, quantity=None, side=None, type=None, time_in_force=None, created_date=None, limit_price=None, stop_price=None, local_vars_configuration=None):  # noqa: E501
        """BlockRequest - a model defined in OpenAPI"
        
        :param id:  (required)
        :type id: lusid.ResourceId
        :param order_ids:  The related order ids. (required)
        :type order_ids: list[lusid.ResourceId]
        :param properties:  Client-defined properties associated with this block.
        :type properties: dict[str, lusid.PerpetualProperty]
        :param instrument_identifiers:  The instrument ordered. (required)
        :type instrument_identifiers: dict(str, str)
        :param quantity:  The total quantity of given instrument ordered. (required)
        :type quantity: float
        :param side:  The client's representation of the block's side (buy, sell, short, etc) (required)
        :type side: str
        :param type:  The block order's type (examples: Limit, Market, ...) (required)
        :type type: str
        :param time_in_force:  The block orders' time in force (examples: Day, GoodTilCancel, ...) (required)
        :type time_in_force: str
        :param created_date:  The date on which the block was made (required)
        :type created_date: datetime
        :param limit_price: 
        :type limit_price: lusid.CurrencyAndAmount
        :param stop_price: 
        :type stop_price: lusid.CurrencyAndAmount

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._order_ids = None
        self._properties = None
        self._instrument_identifiers = None
        self._quantity = None
        self._side = None
        self._type = None
        self._time_in_force = None
        self._created_date = None
        self._limit_price = None
        self._stop_price = None
        self.discriminator = None

        self.id = id
        self.order_ids = order_ids
        self.properties = properties
        self.instrument_identifiers = instrument_identifiers
        self.quantity = quantity
        self.side = side
        self.type = type
        self.time_in_force = time_in_force
        self.created_date = created_date
        if limit_price is not None:
            self.limit_price = limit_price
        if stop_price is not None:
            self.stop_price = stop_price

    @property
    def id(self):
        """Gets the id of this BlockRequest.  # noqa: E501


        :return: The id of this BlockRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BlockRequest.


        :param id: The id of this BlockRequest.  # noqa: E501
        :type id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def order_ids(self):
        """Gets the order_ids of this BlockRequest.  # noqa: E501

        The related order ids.  # noqa: E501

        :return: The order_ids of this BlockRequest.  # noqa: E501
        :rtype: list[lusid.ResourceId]
        """
        return self._order_ids

    @order_ids.setter
    def order_ids(self, order_ids):
        """Sets the order_ids of this BlockRequest.

        The related order ids.  # noqa: E501

        :param order_ids: The order_ids of this BlockRequest.  # noqa: E501
        :type order_ids: list[lusid.ResourceId]
        """
        if self.local_vars_configuration.client_side_validation and order_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `order_ids`, must not be `None`")  # noqa: E501

        self._order_ids = order_ids

    @property
    def properties(self):
        """Gets the properties of this BlockRequest.  # noqa: E501

        Client-defined properties associated with this block.  # noqa: E501

        :return: The properties of this BlockRequest.  # noqa: E501
        :rtype: dict[str, lusid.PerpetualProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this BlockRequest.

        Client-defined properties associated with this block.  # noqa: E501

        :param properties: The properties of this BlockRequest.  # noqa: E501
        :type properties: dict[str, lusid.PerpetualProperty]
        """

        self._properties = properties

    @property
    def instrument_identifiers(self):
        """Gets the instrument_identifiers of this BlockRequest.  # noqa: E501

        The instrument ordered.  # noqa: E501

        :return: The instrument_identifiers of this BlockRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._instrument_identifiers

    @instrument_identifiers.setter
    def instrument_identifiers(self, instrument_identifiers):
        """Sets the instrument_identifiers of this BlockRequest.

        The instrument ordered.  # noqa: E501

        :param instrument_identifiers: The instrument_identifiers of this BlockRequest.  # noqa: E501
        :type instrument_identifiers: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and instrument_identifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_identifiers`, must not be `None`")  # noqa: E501

        self._instrument_identifiers = instrument_identifiers

    @property
    def quantity(self):
        """Gets the quantity of this BlockRequest.  # noqa: E501

        The total quantity of given instrument ordered.  # noqa: E501

        :return: The quantity of this BlockRequest.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this BlockRequest.

        The total quantity of given instrument ordered.  # noqa: E501

        :param quantity: The quantity of this BlockRequest.  # noqa: E501
        :type quantity: float
        """
        if self.local_vars_configuration.client_side_validation and quantity is None:  # noqa: E501
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

    @property
    def side(self):
        """Gets the side of this BlockRequest.  # noqa: E501

        The client's representation of the block's side (buy, sell, short, etc)  # noqa: E501

        :return: The side of this BlockRequest.  # noqa: E501
        :rtype: str
        """
        return self._side

    @side.setter
    def side(self, side):
        """Sets the side of this BlockRequest.

        The client's representation of the block's side (buy, sell, short, etc)  # noqa: E501

        :param side: The side of this BlockRequest.  # noqa: E501
        :type side: str
        """
        if self.local_vars_configuration.client_side_validation and side is None:  # noqa: E501
            raise ValueError("Invalid value for `side`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                side is not None and len(side) < 1):
            raise ValueError("Invalid value for `side`, length must be greater than or equal to `1`")  # noqa: E501

        self._side = side

    @property
    def type(self):
        """Gets the type of this BlockRequest.  # noqa: E501

        The block order's type (examples: Limit, Market, ...)  # noqa: E501

        :return: The type of this BlockRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BlockRequest.

        The block order's type (examples: Limit, Market, ...)  # noqa: E501

        :param type: The type of this BlockRequest.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 1):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `1`")  # noqa: E501

        self._type = type

    @property
    def time_in_force(self):
        """Gets the time_in_force of this BlockRequest.  # noqa: E501

        The block orders' time in force (examples: Day, GoodTilCancel, ...)  # noqa: E501

        :return: The time_in_force of this BlockRequest.  # noqa: E501
        :rtype: str
        """
        return self._time_in_force

    @time_in_force.setter
    def time_in_force(self, time_in_force):
        """Sets the time_in_force of this BlockRequest.

        The block orders' time in force (examples: Day, GoodTilCancel, ...)  # noqa: E501

        :param time_in_force: The time_in_force of this BlockRequest.  # noqa: E501
        :type time_in_force: str
        """
        if self.local_vars_configuration.client_side_validation and time_in_force is None:  # noqa: E501
            raise ValueError("Invalid value for `time_in_force`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                time_in_force is not None and len(time_in_force) < 1):
            raise ValueError("Invalid value for `time_in_force`, length must be greater than or equal to `1`")  # noqa: E501

        self._time_in_force = time_in_force

    @property
    def created_date(self):
        """Gets the created_date of this BlockRequest.  # noqa: E501

        The date on which the block was made  # noqa: E501

        :return: The created_date of this BlockRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this BlockRequest.

        The date on which the block was made  # noqa: E501

        :param created_date: The created_date of this BlockRequest.  # noqa: E501
        :type created_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_date is None:  # noqa: E501
            raise ValueError("Invalid value for `created_date`, must not be `None`")  # noqa: E501

        self._created_date = created_date

    @property
    def limit_price(self):
        """Gets the limit_price of this BlockRequest.  # noqa: E501


        :return: The limit_price of this BlockRequest.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._limit_price

    @limit_price.setter
    def limit_price(self, limit_price):
        """Sets the limit_price of this BlockRequest.


        :param limit_price: The limit_price of this BlockRequest.  # noqa: E501
        :type limit_price: lusid.CurrencyAndAmount
        """

        self._limit_price = limit_price

    @property
    def stop_price(self):
        """Gets the stop_price of this BlockRequest.  # noqa: E501


        :return: The stop_price of this BlockRequest.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._stop_price

    @stop_price.setter
    def stop_price(self, stop_price):
        """Sets the stop_price of this BlockRequest.


        :param stop_price: The stop_price of this BlockRequest.  # noqa: E501
        :type stop_price: lusid.CurrencyAndAmount
        """

        self._stop_price = stop_price

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
        if not isinstance(other, BlockRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BlockRequest):
            return True

        return self.to_dict() != other.to_dict()
