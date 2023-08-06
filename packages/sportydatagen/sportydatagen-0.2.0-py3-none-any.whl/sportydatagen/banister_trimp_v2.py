"""Class for calculating Banister Trimp based on paper."""

from enum import Enum

import numpy as np


class Gender(Enum):

    """Gender Enum."""

    male = 1
    female = 2


class BanisterTrimpV2:

    r"""Class for calculation of Banister's TRIMP.

    Reference paper:
        Banister, Eric W. "Modeling elite athletic performance."
        Physiological testing of elite athletes 347 (1991): 403-422.


    Args:
    ----
    duration (float): total duration in seconds
    average_heart_rate (float): average heart rate in beats per minute
    min_heart_rate (float): minimum heart rate in beats per minute
    max_heart_rate (float): maximum heart rate in beats per minute
    gender (Gender enum): gender of athlete
    """

    def __init__(self: 'BanisterTrimpV2',
                 duration: float,
                 average_heart_rate: float,
                 min_heart_rate: float,
                 max_heart_rate: float,
                 gender: Gender = Gender.male,
                 ) -> None:
        """Initialize BanisterTRIMP class."""
        self.duration = duration

        self.average_heart_rate = average_heart_rate
        self.max_heart_rate = max_heart_rate
        # currently minimum heart rate,
        # since we don't have a resting heart rate
        self.rest_heart_rate = min_heart_rate

        self.gender = gender

        self.b_male = 1.92
        self.b_female = 1.67


    def calculate_delta_hr_ratio(self: 'BanisterTrimpV2') -> float:
        """Calculate the delta heart rate.

        The ratio ranges from a low to a high value (i.e., ~ 0.2 — 1.0)
        for a low or a high raw heart rate, respectively.

        Returns
        -------
            float: delta heart rate.
        """
        return (self.average_heart_rate - self.rest_heart_rate) / \
            (self.max_heart_rate - self.rest_heart_rate)


    def calculate_weighting_factor(self: 'BanisterTrimpV2',
                                   delta_hr_ratio: float,
                                   ) -> float:
        """Calculate the weighting factor.

        Returns
        -------
            float: weighting factor (Y).
        """
        # x due to the fact that the paper uses x instead of delta_hr_ratio
        x = delta_hr_ratio

        # b defaults to b_male since only males contributed to the dataset
        b = self.b_female if self.gender is Gender.female else self.b_male

        return np.power(np.e,(b * x))


    def calculate_trimp(self: 'BanisterTrimpV2') -> float:
        """Calculate TRIMP.

        Returns
        -------
            float: Banister TRIMP value.
        """
        duration_minutes = self.duration / 60
        delta_hr_ratio = self.calculate_delta_hr_ratio()
        weighting_factor = self.calculate_weighting_factor(delta_hr_ratio)

        return duration_minutes * delta_hr_ratio * weighting_factor
