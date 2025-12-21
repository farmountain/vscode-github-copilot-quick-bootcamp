"""Tests for PII tokenization functions."""

import pytest

from src.day2.pii_protection.tokenization import (
    generate_token,
    tokenize_field,
    tokenize_record,
    verify_token_determinism
)


class TestGenerateToken:
    """Test token generation."""
    
    def test_token_generation(self):
        """Test basic token generation."""
        token = generate_token("test@example.com", "secret")
        assert token.startswith("TOKEN_")
        assert len(token) > 10
    
    def test_deterministic_token(self):
        """Test that same input produces same token."""
        token1 = generate_token("test@example.com", "secret")
        token2 = generate_token("test@example.com", "secret")
        assert token1 == token2
    
    def test_different_values_different_tokens(self):
        """Test that different values produce different tokens."""
        token1 = generate_token("test1@example.com", "secret")
        token2 = generate_token("test2@example.com", "secret")
        assert token1 != token2
    
    def test_different_keys_different_tokens(self):
        """Test that different keys produce different tokens."""
        token1 = generate_token("test@example.com", "secret1")
        token2 = generate_token("test@example.com", "secret2")
        assert token1 != token2
    
    def test_empty_value(self):
        """Test token generation for empty value."""
        token = generate_token("", "secret")
        assert token == "TOKEN_EMPTY"


class TestTokenizeField:
    """Test field tokenization."""
    
    def test_tokenize_email(self):
        """Test tokenizing email field."""
        token = tokenize_field("email", "john@example.com", "secret")
        assert token.startswith("TOKEN_")
    
    def test_tokenize_phone(self):
        """Test tokenizing phone field."""
        token = tokenize_field("phone", "555-123-4567", "secret")
        assert token.startswith("TOKEN_")
    
    def test_same_field_same_value_deterministic(self):
        """Test that same field and value produce same token."""
        token1 = tokenize_field("email", "john@example.com", "secret")
        token2 = tokenize_field("email", "john@example.com", "secret")
        assert token1 == token2
    
    def test_different_fields_same_value_different_tokens(self):
        """Test that different fields with same value produce different tokens."""
        token1 = tokenize_field("email", "john@example.com", "secret")
        token2 = tokenize_field("username", "john@example.com", "secret")
        assert token1 != token2


class TestTokenizeRecord:
    """Test record tokenization."""
    
    def test_tokenize_single_field(self):
        """Test tokenizing single field in record."""
        record = {
            "customer_id": "CUST001",
            "email": "john@example.com",
            "name": "John Doe"
        }
        tokenized = tokenize_record(record, {"email"}, "secret")
        
        assert tokenized["customer_id"] == "CUST001"
        assert tokenized["name"] == "John Doe"
        assert tokenized["email"].startswith("TOKEN_")
        assert tokenized["email"] != "john@example.com"
    
    def test_tokenize_multiple_fields(self):
        """Test tokenizing multiple fields in record."""
        record = {
            "customer_id": "CUST001",
            "email": "john@example.com",
            "phone": "555-123-4567",
            "name": "John Doe"
        }
        tokenized = tokenize_record(record, {"email", "phone"}, "secret")
        
        assert tokenized["customer_id"] == "CUST001"
        assert tokenized["name"] == "John Doe"
        assert tokenized["email"].startswith("TOKEN_")
        assert tokenized["phone"].startswith("TOKEN_")
    
    def test_tokenize_nonexistent_field(self):
        """Test tokenizing field that doesn't exist in record."""
        record = {
            "customer_id": "CUST001",
            "name": "John Doe"
        }
        tokenized = tokenize_record(record, {"email"}, "secret")
        
        # Should not raise error, just skip missing fields
        assert tokenized["customer_id"] == "CUST001"
        assert tokenized["name"] == "John Doe"
        assert "email" not in tokenized


class TestVerifyTokenDeterminism:
    """Test token determinism verification."""
    
    def test_verify_valid_token(self):
        """Test verification of valid token."""
        value = "john@example.com"
        token = tokenize_field("email", value, "secret")
        is_valid = verify_token_determinism(value, token, "email", "secret")
        assert is_valid is True
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        value = "john@example.com"
        token = "TOKEN_INVALID"
        is_valid = verify_token_determinism(value, token, "email", "secret")
        assert is_valid is False
    
    def test_verify_token_with_wrong_key(self):
        """Test verification fails with wrong key."""
        value = "john@example.com"
        token = tokenize_field("email", value, "secret1")
        is_valid = verify_token_determinism(value, token, "email", "secret2")
        assert is_valid is False


class TestTokenDeterminismProperty:
    """Test determinism property of tokenization."""
    
    def test_determinism_across_multiple_calls(self):
        """Test that tokenization is deterministic across multiple calls."""
        value = "sensitive@data.com"
        field = "email"
        secret = "secret-key"
        
        tokens = [tokenize_field(field, value, secret) for _ in range(10)]
        
        # All tokens should be identical
        assert len(set(tokens)) == 1
    
    def test_different_values_unique_tokens(self):
        """Test that different values produce unique tokens."""
        field = "email"
        secret = "secret-key"
        
        values = [
            "user1@example.com",
            "user2@example.com",
            "user3@example.com"
        ]
        
        tokens = [tokenize_field(field, value, secret) for value in values]
        
        # All tokens should be unique
        assert len(set(tokens)) == len(values)
