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
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether
    it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        Assign arguments to the objects properties and supply a default value
        if the argument isn't passed.  For name also replace empty names
        with None.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """

        try:
            self.designation = str(info['designation'])
        except(KeyError):
            self.designation = None

        try:
            if info['name'] == '':
                self.name = None
            else:
                self.name = info['name']
        except(KeyError):
            self.name = None

        try:
            self.diameter = float(info['diameter'])
        except(KeyError, ValueError):
            self.diameter = float('nan')

        try:
            self.hazardous = info['hazardous'] == 'Y'
        except(KeyError):
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation + ' ' + str(self.name)

    def __str__(self):
        """Return `str(self)`."""
        return ' '.join(f"""A NearEarthObject with designation
                        {self.designation!r},
                        name {self.name!r},
                        diameter {self.diameter:.3f},
                        hazardous status of {self.hazardous!r},
                        and {len(self.approaches)} associated approaches
                        """.split())

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of
        this object."""
        return (f"NearEarthObject(designation={self.designation!r}, ",
                f"name={self.name!r}, ",
                f"diameter={self.diameter:.2f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative approach
    velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        Pass all of the argments to, and give a default value if the
        argument is missing.  Also convert the NASA supplied datetime to
        a python datetime object.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """
        try:
            self._designation = str(info['designation'])
        except(KeyError):
            self.designation = None

        try:
            self.time = cd_to_datetime(info['time'])
        except(KeyError):
            self.time = None

        try:
            self.distance = float(info['distance'])
        except(KeyError):
            self.distance = None

        try:
            self.velocity = float(info['velocity'])
        except(KeyError, TypeError):
            self.velocity = None

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s
        approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return ' '.join(f"""NEO {self._designation!r},
                        with a diameter {self.distance:.2f},
                        approached earth at {self.time_str!r} traveling at a
                        velocity of {self.velocity}
                        at a distance of {self.distance:.2f}  """.split())

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of
        this object."""
        return (f"CloseApproach(time={self.time_str!r}, ",
                f" distance={self.distance:.2f}, ",
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
