"""Provide filters for querying close approaches and limit the results.

The `create_filters` function produces a collection of objects
that is used by the `query` method to generate a stream of `CloseApproach`
objects that match all of the desired criteria. The arguments to
`create_filters` are provided bythe main module and originate from
the user's command-line options.

This function can be thought to return a collection of instances
of subclassesof `AttributeFilter` - a 1-argument callable (on a
`CloseApproach`) constructedfrom a comparator (from the `operator`
module), a reference value, and a classmethod `get` that subclasses
can override to fetch an attribute of interest fromthe supplied
`CloseApproach`.

The `limit` function simply limits the maximum number of values
produced by aniterator.
"""

import operator
import itertools


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing
    someattribute of a close approach (or its attached NEO) to a reference
    value. Itessentially functions as a callable predicate for whether
    a `CloseApproach`object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value,
    andcalling the filter (with __call__) executes `get(approach) OP
    value` (ininfix notation).

    Concrete subclasses can override the `get` classmethod to provide
    custombehavior to fetch a desired attribute from the given
    `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from binary and reference values.

        The reference value will be supplied as the second (right-hand
        side) argument to the operator function. For example, an
        `AttributeFilter` with `op=operator.le` and `value=10` will,
        when called on an approach, evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute
        of interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this
        filter. :return: The value of an attribute of interest, comparable
        to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Create a representation of the Attribute object."""
        return f"""{self.__class__.__name__}
                    (op=operator.{self.op.__name__}, value={self.value})"""


class DateFilter(AttributeFilter):
    """Custom subclass of AttributeFilter to filter on date of the approach."""

    def get(cls, approach):
        """Extract the time attribute and convert it to a date.

        :param approach: A `CloseApproach` on which to evaluate this
        filter.
        :return: The value of an attribute of interest, comparable
        to `self.value` via `self.op`.
        """
        return approach.time.date()


class ApproachFilter(AttributeFilter):
    """Custom subclass of AttributeFilter for non date approach attributes."""

    def __init__(self, op, value, attr):
        """Super class initialization as well as a specified attribute.

        In addition to the standard initialization of the super class,
        take in the `attr` which represents the attribute to access from
        the approach object.

        :param attr: A string representing the attribute we want to access
        when initializing this object.
        """
        super().__init__(op, value)
        self.attr = attr

    def get(self, approach):
        """Extract the attribute `attr` passed on initialization.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to
        `self.value` via `self.op`.
        """
        return getattr(approach, self.attr)


class NeoFilter(AttributeFilter):
    """Subclass of AttributeFilter to filter on associated attributes."""

    def __init__(self, op, value, attr):
        """Super class initialization as well as a specified attribute.

        In addition to the standard initialization of the super class,
        take in the `attr` which represents the attribute to access from
        the approach object.

        :param attr: A string representing the attribute we want to access when
        initializing this object.
        """
        super().__init__(op, value)
        self.attr = attr

    def get(self, approach):
        """Extract the attribute `attr` from the approach's neo object.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to
        `self.value` via `self.op`.
        """
        return getattr(approach.neo, self.attr)


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a
    value from the user's options at the command line. Each one corresponds
    to a different type of filter. For example, the `--date` option
    corresponds to the `date` argument, and represents a filter that
    selects close approaches that occured on exactly that given date.
    Similarly, the `--min-distance` option corresponds to the `distance_min`
    argument, and represents a filter that selects close approaches
    whose nominal approach distance is at least that far away from
    Earth. Each option is `None` if not specified at the command line
    (in particular, this means that the `--not-hazardous` flag results
    in `hazardous=False`, not to be confused with `hazardous=None`).

    This returns a variable length list of filter objects  (DateFilter,
    ApproachFilter or NeoFilter) to the database.query function which,
    which calls each filter for each CloseApproach in the database
    to check if  the approach matches the filters passed as arguments.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach`
    occurs.
    :param end_date: A `date` on or before which a matching
    `CloseApproach` occurs.
    :param distance_min: A minimum nominal
    approach distance for a matching `CloseApproach`.
    :param distance_max:
    A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for
    a matching `CloseApproach`.
    :param velocity_max: A maximum relative
    approach velocity for a matching `CloseApproach`.
    :param diameter_min:
    A minimum diameter of the NEO of a matching `CloseApproach`. :param
    diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach`
    is potentially hazardous.
    :return: A list of filters for use with `query`.
    """
    filters = []
    # Add the operator as a second piece since we need that later
    # Make this a list of (callable) objects to call for the given approach
    # Only add arguments that are not None
    if date is not None:
        filters.append(DateFilter(operator.eq, date))
    if start_date is not None:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date is not None:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min is not None:
        filters.append(ApproachFilter(operator.ge,
                                      distance_min,
                                      'distance'))
    if distance_max is not None:
        filters.append(ApproachFilter(operator.le,
                                      distance_max,
                                      'distance'))
    if velocity_min is not None:
        filters.append(ApproachFilter(operator.ge,
                                      velocity_min,
                                      'velocity'))
    if velocity_max is not None:
        filters.append(ApproachFilter(operator.le,
                                      velocity_max,
                                      'velocity'))
    if diameter_min is not None:
        filters.append(NeoFilter(operator.ge,
                                 diameter_min,
                                 'diameter'))
    if diameter_max is not None:
        filters.append(NeoFilter(operator.le,
                                 diameter_max,
                                 'diameter'))
    if hazardous is not None:
        filters.append(NeoFilter(operator.eq,
                                 hazardous,
                                 'hazardous'))
    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n == 0 or n is None:
        return iterator
    else:
        return itertools.islice(iterator, n)
