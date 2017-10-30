# coding: utf-8

from __future__ import absolute_import
from api_server.entities.base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from api_server.util import deserialize_model


class ProbabilityResponseItem(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, probability: float=None, hotels: List[int]=None):
        """
        ProbabilityResponseItem - a model defined in Swagger

        :param probability: The probability of this ProbabilityResponseItem.
        :type probability: float
        :param hotels: The hotels of this ProbabilityResponseItem.
        :type hotels: List[int]
        """
        self.swagger_types = {
            'probability': float,
            'hotels': List[int]
        }

        self.attribute_map = {
            'probability': 'probability',
            'hotels': 'hotels'
        }

        self._probability = probability
        self._hotels = hotels

    @classmethod
    def from_dict(cls, dikt) -> 'ProbabilityResponseItem':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The probabilityResponseItem of this ProbabilityResponseItem.
        :rtype: ProbabilityResponseItem
        """
        return deserialize_model(dikt, cls)

    @property
    def probability(self) -> float:
        """
        Gets the probability of this ProbabilityResponseItem.

        :return: The probability of this ProbabilityResponseItem.
        :rtype: float
        """
        return self._probability

    @probability.setter
    def probability(self, probability: float):
        """
        Sets the probability of this ProbabilityResponseItem.

        :param probability: The probability of this ProbabilityResponseItem.
        :type probability: float
        """

        self._probability = probability

    @property
    def hotels(self) -> List[int]:
        """
        Gets the hotels of this ProbabilityResponseItem.

        :return: The hotels of this ProbabilityResponseItem.
        :rtype: List[int]
        """
        return self._hotels

    @hotels.setter
    def hotels(self, hotels: List[int]):
        """
        Sets the hotels of this ProbabilityResponseItem.

        :param hotels: The hotels of this ProbabilityResponseItem.
        :type hotels: List[int]
        """

        self._hotels = hotels
