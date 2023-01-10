"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation='{fullname}', name=None, diameter=float('nan'), hazardous='', approaches=[]):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = str(designation)
        if not bool(name):
            self.name = None
        else:
            self.name = name

        self._diameter = {'diameter': ''}
        if diameter == '':
            self.diameter = float('nan')
            self._diameter['diameter'] = '{diameter}'

        else:
            self.diameter = float(diameter)
            self._diameter['diameter'] = self.diameter
        self.str_hazardous = ''

        self.hazardous = False
        if hazardous == 'Y' or hazardous == 'y':
            self.str_hazardous = 'is'
            self.hazardous = True
        elif hazardous == 'N' or hazardous == 'N' or hazardous == '':
            self.str_hazardous = 'is not'
        else:
            raise ValueError("non supported input value for hazardous!")

        # Create an empty initial collection of linked approaches.
        self.approaches = approaches

    @property
    def fullname(self):
        """Get fullname method."""
        if not bool(self.name):
            return self.designation
        return self.designation + ' (' + self.name + ')'

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} has a diameter of {self._diameter['diameter']:.3f} km " \
               f"and {self.str_hazardous} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation='', time='', distance=float('nan'), velocity=float('nan'), neo=NearEarthObject()):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = designation
        self.time = None
        self.neo = neo
        if time:
            self.time = cd_to_datetime(time)

        self._distance = {'distance': ''}
        if distance == '':
            self.distance = float('nan')
            self._distance['distance'] = '{distance}'

        else:
            self.distance = float(distance)
            self._distance['distance'] = self.distance

        self._velocity = {'velocity': ''}
        if velocity == '':
            self.velocity = float('nan')
            self._velocity['velocity'] = '{velocity}'

        else:
            self.velocity = float(velocity)
            self._velocity['velocity'] = self.velocity

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        if not bool(self.time):
            return '{time_str}'
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"on {self.time_str!r} {self.neo.fullname} approaches Earth at a distance of " \
               f"{self._distance['distance']:.2f} au and " \
               f"velocity of {self._velocity['velocity']:.2f} km/s"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f} au, " \
               f"and a velocity of {self.velocity:.2f})"