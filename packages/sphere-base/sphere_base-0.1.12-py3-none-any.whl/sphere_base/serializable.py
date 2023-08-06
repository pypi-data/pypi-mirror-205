# -*- coding: utf-8 -*-

"""
A module containing Serializable "Interface". We pretend it is an abstract class

"""

from collections import OrderedDict


class Serializable:
    def __init__(self, item_type=None):
        """
        Default constructor automatically creates data which are common to any serializable object.
        In our case we create ``self.id`` which we use in every object in NodeEditor.
        """
        self.id = id(self)
        self.type = item_type

    def serialize(self) -> OrderedDict:
        """
        Serialization method to serialize this class data into ``OrderedDict`` which can be easily stored
        in memory or file.

        :return: data serialized in ``OrderedDict``
        :rtype: ``OrderedDict``
        """
        raise NotImplemented()

    def deserialize(self, data: dict, hashmap: dict = None, restore_id: bool = True) -> bool:
        hashmap = hashmap if hashmap else {}
        print(hashmap)
        """
        Deserialization method which take data in python ``dict`` format with helping `hashmap` containing
        references to existing entities.

        :param data: Dictionary containing serialized data
        :type data: ``dict``
        :param hashmap: Helper dictionary containing references (by id == key) to existing objects
        :type hashmap: ``dict``
        :param restore_id: True if we are creating new Sockets. False is useful when loading existing
            Sockets of which we want to keep the existing object's `id`.
        :type restore_id: bool
        :return: ``True`` if deserialization was successful, otherwise ``False``
        :rtype: ``bool``
        """
        return NotImplemented
