"""API tests"""
# pylint: disable=invalid-name

from dataclasses import dataclass
from datetime import datetime
from datetime import timezone


import colemen_utils as c
import volent

# import volent.Volent as volent
from volent.Volent import Schema,Field,validators as _v
from volent.data_types import String,Integer,EncodedPrimary
import volent.validate as valid



class TestValidators:
    """TEST Schema Validation of dictionaries"""

    def test_email(self):
        """Confirm that we can validate an email address."""
        v = valid.Email()
        email = c.rand.email()
        r = v(email,"email")
        assert r == email

        email = c.rand.abstract_name()
        try:
            v(email,"email")
        except Exception as e:
            return
        assert False

    def test_equal(self):
        """Confirm that the equal validator functions properly."""
        value = c.rand.rand()
        v = valid.Equal(value)
        r = v(value,"value")
        assert r == value

        incorrect_value = c.rand.rand()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return
        assert False

    def test_future_unix_timestamp(self):
        """Confirm that we can validate a future unix timestamp."""
        ct = round(datetime.now(tz=timezone.utc).timestamp())
        value = ct + (86400 * c.rand.number(1,10))
        v = valid.FutureUnixDate(value)
        r = v(value,"value")
        assert r == value

        incorrect_value = ct - (86400 * c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return
        assert False

    def test_ip_address_ipv4(self):
        """Confirm that we can validate an ipv4 address."""
        value = c.rand.ip_address()
        v = valid.IpAddress()
        r = v(value,"value")
        assert r == value

        incorrect_value = c.rand.rand()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return
        assert False

    def test_ip_address_ipv6(self):
        """Confirm that we can validate an ipv6 address."""
        value = c.rand.ip_address_ipv6()
        v = valid.IpAddress()
        r = v(value,"value")
        assert r == value

        incorrect_value = c.rand.rand()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return
        assert False

    def test_length_range(self):
        """Confirm that we can validate that a string's length is within a range."""
        min = 12
        max = 14
        value = c.rand.rand(min)
        v = valid.Length(min,max)
        r = v(value,"value")
        assert r == value



        # -------------------------- Test below the minimum -------------------------- #
        incorrect_value = c.rand.rand(min - c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return


        # -------------------------- Test above the maximum -------------------------- #
        incorrect_value = c.rand.rand(max + c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return



        assert False

    def test_length_min(self):
        """Confirm that we can validate a strings length is greater than a minimum"""
        min = 12
        # max = 14
        value = c.rand.rand(min)
        v = valid.Length(min)
        r = v(value,"value")
        assert r == value



        # -------------------------- Test less than the minimum -------------------------- #
        incorrect_value = c.rand.rand(min - c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return



        assert False

    def test_length_max(self):
        """Confirm that we can validate a strings length is less than a maximum"""
        # min = 12
        max = 14
        value = c.rand.rand(max)
        v = valid.Length(max=max)
        r = v(value,"value")
        assert r == value



        # -------------------------- Test greater than the maximum -------------------------- #
        incorrect_value = c.rand.rand(max + c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return



        assert False

    def test_length_equal(self):
        """Confirm that we can validate a strings length is equal to a value"""
        # min = 12
        max = 8
        value = c.rand.rand(max)
        v = valid.Length(equal=max)
        r = v(value,"value")
        assert r == value



        # -------------------------- Test greater than the maximum -------------------------- #
        incorrect_value = c.rand.rand(max + c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return



        assert False


    def test_none_of(self):
        """Confirm that we can validate value does not match a preset list"""
        # min = 12
        values = ["beep","boop"]
        value = c.rand.rand()
        v = valid.NoneOf(values)
        r = v(value,"value")
        assert r == value


        incorrect_value = c.rand.option(values)
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return

        assert False

    def test_one_of(self):
        """Confirm that we can validate that a value matches in a list"""
        # min = 12
        values = ["beep","boop"]
        value = c.rand.option(values)
        v = valid.OneOf(values)
        r = v(value,"value")
        assert r == value


        incorrect_value = c.rand.rand()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return

        assert False


    def test_past_unix_timestamp(self):
        """Confirm that we can validate a past unix timestamp."""
        ct = round(datetime.now(tz=timezone.utc).timestamp())
        value = ct - (86400 * c.rand.number(1,10))
        v = valid.PastUnixDate(value)
        r = v(value,"value")
        assert r == value

        incorrect_value = ct + (86400 * c.rand.number(1,10))
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return
        assert False


    def test_phone_number(self):
        """Confirm that we can validate a phone number"""
        value = c.rand.phone()
        v = valid.PhoneNumber(value)
        r = v(value,"value")
        assert r == value


        incorrect_value = c.rand.rand()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return

        assert False

    def test_range(self):
        """Confirm that we can validate that a value is within a range."""
        min = 1
        max = 100

        value = c.rand.number(min,max)
        v = valid.Range(min,max)
        r = v(value,"value")
        assert r == value


        incorrect_value = min - c.rand.number()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            pass

        incorrect_value = max + c.rand.number()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return

        assert False

    def test_regex(self):
        """Confirm that we can validate that a value matches a regex."""
        regex = r"beep\sboop[0-9]*"

        value = "beep boop123"
        v = valid.Regex(regex)
        r = v(value,"value")
        assert r == value


        incorrect_value = c.rand.number()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return


        assert False

    def test_credit_card(self):
        """Confirm that we can validate a credit card number."""
        value = c.rand.credit_card_number()
        v = valid.CreditCardNumber()
        r = v(value,"value")
        assert r == value


        incorrect_value = c.rand.number()
        try:
            v(incorrect_value,"value")
        except Exception as e:
            return


        assert False

