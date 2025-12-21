"""Tests for PII masking functions."""

import pytest

from src.day2.pii_protection.masking import (
    mask_email,
    mask_phone,
    mask_national_id,
    mask_name,
    mask_address,
    mask_date_of_birth,
    mask_field
)


class TestMaskEmail:
    """Test email masking."""
    
    def test_standard_email(self):
        """Test masking of standard email."""
        result = mask_email("john.doe@example.com")
        assert result == "jo***@ex***.com"
    
    def test_short_username(self):
        """Test email with short username."""
        result = mask_email("ab@example.com")
        assert result == "***@ex***.com"
    
    def test_short_domain(self):
        """Test email with short domain."""
        result = mask_email("john@ab.com")
        assert result == "jo***@***.com"
    
    def test_invalid_email(self):
        """Test invalid email format."""
        result = mask_email("notanemail")
        assert result == "***@***.***"


class TestMaskPhone:
    """Test phone number masking."""
    
    def test_standard_phone(self):
        """Test masking of standard phone number."""
        result = mask_phone("555-123-4567")
        assert result == "***-***-4567"
    
    def test_phone_with_parens(self):
        """Test phone number with parentheses."""
        result = mask_phone("(555) 123-4567")
        assert result == "***-***-4567"
    
    def test_phone_no_formatting(self):
        """Test phone number without formatting."""
        result = mask_phone("5551234567")
        assert result == "***-***-4567"
    
    def test_short_phone(self):
        """Test short phone number."""
        result = mask_phone("1234")
        assert result == "***-***-1234"


class TestMaskNationalId:
    """Test national ID (SSN) masking."""
    
    def test_standard_ssn(self):
        """Test masking of standard SSN."""
        result = mask_national_id("123-45-6789")
        assert result == "***-**-6789"
    
    def test_ssn_no_formatting(self):
        """Test SSN without formatting."""
        result = mask_national_id("123456789")
        assert result == "***-**-6789"
    
    def test_short_ssn(self):
        """Test short SSN."""
        result = mask_national_id("6789")
        assert result == "***-**-6789"


class TestMaskName:
    """Test name masking."""
    
    def test_full_name(self):
        """Test masking of full name."""
        result = mask_name("John Doe")
        assert result == "J*** D***"
    
    def test_single_name(self):
        """Test masking of single name."""
        result = mask_name("Madonna")
        assert result == "M***"
    
    def test_three_part_name(self):
        """Test masking of three-part name."""
        result = mask_name("John Paul Jones")
        assert result == "J*** P*** J***"
    
    def test_empty_name(self):
        """Test empty name."""
        result = mask_name("")
        assert result == "***"


class TestMaskAddress:
    """Test address masking."""
    
    def test_standard_address(self):
        """Test masking of standard address."""
        result = mask_address("123 Main St, Apt 4B")
        assert result == "*** *** ***"
    
    def test_empty_address(self):
        """Test empty address."""
        result = mask_address("")
        assert result == "*** *** ***"


class TestMaskDateOfBirth:
    """Test date of birth masking."""
    
    def test_standard_dob(self):
        """Test masking of standard DOB."""
        result = mask_date_of_birth("1985-03-15")
        assert result == "**/**/1985"
    
    def test_slash_format_dob(self):
        """Test DOB with slash format."""
        result = mask_date_of_birth("03/15/1985")
        assert result == "**/**/1985"
    
    def test_invalid_dob(self):
        """Test invalid DOB format."""
        result = mask_date_of_birth("invalid")
        assert result == "**/**/****"


class TestMaskField:
    """Test field-based masking."""
    
    def test_email_field(self):
        """Test masking based on email field name."""
        result = mask_field("email", "john@example.com")
        assert "***" in result
        assert "@" in result
    
    def test_phone_field(self):
        """Test masking based on phone field name."""
        result = mask_field("phone", "555-123-4567")
        assert result == "***-***-4567"
    
    def test_ssn_field(self):
        """Test masking based on SSN field name."""
        result = mask_field("ssn", "123-45-6789")
        assert result == "***-**-6789"
    
    def test_name_field(self):
        """Test masking based on name field name."""
        result = mask_field("full_name", "John Doe")
        assert result == "J*** D***"
    
    def test_address_field(self):
        """Test masking based on address field name."""
        result = mask_field("address", "123 Main St")
        assert result == "*** *** ***"
    
    def test_dob_field(self):
        """Test masking based on DOB field name."""
        result = mask_field("date_of_birth", "1985-03-15")
        assert result == "**/**/1985"
    
    def test_unknown_field(self):
        """Test masking of unknown field type."""
        result = mask_field("unknown_field", "some value")
        assert result == "***"
