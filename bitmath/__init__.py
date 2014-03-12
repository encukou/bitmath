# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright © 2014 Tim Bielawa <timbielawa@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Reference material:

Prefixes for binary multiples:
http://physics.nist.gov/cuu/Units/binary.html

decimal and binary prefixes:
man 7 units (from the Linux Documentation Project 'man-pages' package)
"""


import numbers

__all__ = ['Byte', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB']

SI_PREFIXES = ['k', 'K', 'M', 'G', 'T', 'P', 'E']
NIST_PREFIXES = ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei']
# OR all of those NIST prefixes together
# TODO:
# nist_prefix_str = '(' + '|'.join(NIST_PREFIXES) + ')'
# NIST_REGEX = re.compile(r"^(?P<integer_value>\d*)(?P<binary_prefix>%s)?(?P<base_unit>[bB])$" % nist_prefix_str)
# Ki->Ei maps to xrange(1,7), which is the exponent part of the NIST
# calculations. For each prefix, i, multiply it by 10 and raise 2 to
# that power (2**(i*10)). These steps represent the size of each
# successive order of magnitude.
NIST_STEPS = {
    'Byte': 1,
    'Ki': 1024,
    'Mi': 1048576,
    'Gi': 1073741824,
    'Ti': 1099511627776,
    'Pi': 1125899906842624,
    'Ei': 1152921504606846976
}


class Byte(object):
    """The base class for all the other prefix classes"""
    def __init__(self, value=0, bytes=None, bits=None):
        """Instantiate with the `value` by the unit, or in straight
bytes. Don't supply both."""

        self.__setup()
        if bytes:
            self.__byte_value = bytes
        elif bits:
            self.__byte_value = bits / 8
        else:
            self._byte_norm(value)
        self.__set_prefix_value()

    def __set_prefix_value(self):
        self.prefix_value = self.__to_prefix_value(self.__byte_value)

    def __to_prefix_value(self, value):
        """Return the number of bytes as they would look like if we converted
to this unit"""
        #print "converting %s bytes into the equivalent %s" % (value, str(type(self)))
        return float(value) / float(self.__unit_value)

    def _setup(self):
        return (2, 0, 'Byte')

    def __setup(self):
        """Setup basic parameters for this class"""
        """`base` is the numeric base which when raised to `power` is
equivalent to 1 unit of the corresponding prefix. I.e., base=2,
power=10 represents 2^10, which is the NIST Binary Prefix for 1 Kibibyte.

Likewise, for the SI prefix classes `base` will be 10, and the `power`
for the Kilobyte is 3."""
        (self.__base, self.__power, self.__name) = self._setup()
        self.__unit_value = self.__base ** self.__power

    def _byte_norm(self, value):
        """Normalize the input value into bytes"""
        self.__byte_value = value * self.__unit_value

    def bytes(self):
        """Return the number of bytes in a measurement"""
        return self.__byte_value

    # Reference: http://docs.python.org/2.7/reference/datamodel.html#basic-customization

    def __repr__(self):
        """Called by the repr() built-in function and by string conversions
(reverse quotes) to compute the "official" string representation of an
object. If at all possible, this should look like a valid Python
expression that could be used to recreate an object with the same
value (given an appropriate environment). If this is not possible, a
string of the form <...some useful description...> should be
returned. The return value must be a string object. If a class defines
__repr__() but not __str__(), then __repr__() is also used when an
"informal" string representation of instances of that class is
required."""
        return "%s(%s)" % \
            (self.__name, self.prefix_value)

    def __str__(self):
        """Called by the str() built-in function and by the print statement to
compute the "informal" string representation of an object. This
differs from __repr__() in that it does not have to be a valid Python
expression: a more convenient or concise representation may be used
instead. The return value must be a string object."""
        return "%s%s" % \
            (self.prefix_value, self.__name)

    def to_Byte(self):
        return Byte(self.__byte_value / float(NIST_STEPS['Byte']))

    def to_KiB(self):
        return KiB(self.__byte_value / float(NIST_STEPS['Ki']))

    def to_MiB(self):
        return MiB(self.__byte_value / float(NIST_STEPS['Mi']))

    def to_GiB(self):
        return GiB(self.__byte_value / float(NIST_STEPS['Gi']))

    def to_TiB(self):
        return TiB(self.__byte_value / float(NIST_STEPS['Ti']))

    def to_PiB(self):
        return PiB(self.__byte_value / float(NIST_STEPS['Pi']))

    def to_EiB(self):
        return EiB(self.__byte_value / float(NIST_STEPS['Ei']))

    def __lt__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value < other
        else:
            return self.__byte_value < other.bytes()

    def __le__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value <= other
        else:
            return self.__byte_value <= other.bytes()

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value == other
        else:
            return self.__byte_value == other.bytes()

    def __ne__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value != other
        else:
            return self.__byte_value != other.bytes()

    def __gt__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value > other
        else:
            return self.__byte_value > other.bytes()

    def __ge__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value >= other
        else:
            return self.__byte_value >= other.bytes()

    # Reference: http://docs.python.org/2.7/reference/datamodel.html#emulating-numeric-types

    """These methods are called to implement the binary arithmetic
operations (+, -, *, //, %, divmod(), pow(), **, <<, >>, &, ^, |). For
instance, to evaluate the expression x + y, where x is an instance of
a class that has an __add__() method, x.__add__(y) is called. The
__divmod__() method should be the equivalent to using __floordiv__()
and __mod__(); it should not be related to __truediv__() (described
below). Note that __pow__() should be defined to accept an optional
third argument if the ternary version of the built-in pow() function
is to be supported.

If one of those methods does not support the operation with the
supplied arguments, it should return NotImplemented."""

    def __add__(self, other):
        total_bytes = self.__byte_value + other.bytes()
        return (type(self))(bytes=total_bytes)

    def __sub__(self, other):
        total_bytes = self.__byte_value - other.bytes()
        return (type(self))(bytes=total_bytes)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            result = self.__byte_value * other
            return (type(self))(bytes=result)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __divmod__(self, other):
        return NotImplemented

    def __pow__(self, other, modulo=None):
        return NotImplemented

    def __lshift__(self, other):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    """The division operator (/) is implemented by these methods. The
__truediv__() method is used when __future__.division is in effect,
otherwise __div__() is used. If only one of these two methods is
defined, the object will not support division in the alternate
context; TypeError will be raised instead."""

    def __div__(self, other):
        if isinstance(other, numbers.Number):
            result = self.__byte_value / other
            return (type(self))(bytes=result)
        else:
            return self.__byte_value / float(other.bytes())

    def __truediv__(self, other):
        return self.__div__(other)

    def __neg__(self):
        return (type(self))(-abs(self.prefix_value))

    def __pos__(self):
        return (type(self))(abs(self.prefix_value))

    def __abs__(self):
        return (type(self))(bytes=abs(self.prefix_value))

    def __invert__(self):
        """Called to implement the unary arithmetic operations (-, +, abs()
        and ~)."""
        return NotImplemented

######################################################################
# NIST Prefixes


class KiB(Byte):
    def _setup(self):
        return (2, 10, 'KiB')


class MiB(Byte):
    def _setup(self):
        return (2, 20, 'MiB')


class GiB(Byte):
    def _setup(self):
        return (2, 30, 'GiB')


class TiB(Byte):
    def _setup(self):
        return (2, 40, 'TiB')


class PiB(Byte):
    def _setup(self):
        return (2, 50, 'PiB')


class EiB(Byte):
    def _setup(self):
        return (2, 60, 'EiB')


######################################################################
# SI Prefixes


class kB(Byte):
    def _setup(self):
        return (10, 3, 'kB')


class MB(Byte):
    def _setup(self):
        return (10, 6, 'MB')


class GB(Byte):
    def _setup(self):
        return (10, 9, 'GB')


class TB(Byte):
    def _setup(self):
        return (10, 12, 'TB')


class PB(Byte):
    def _setup(self):
        return (10, 15, 'PB')


class EB(Byte):
    def _setup(self):
        return (10, 18, 'EB')
