"""PII masking functions."""

import re


def mask_email(email: str) -> str:
    """Mask email address.
    
    Format: ab***@ex***.com
    - Shows first 2 characters of username
    - Masks rest of username with ***
    - Shows first 2 characters of domain
    - Masks rest of domain with ***
    - Preserves TLD
    
    Args:
        email: Email address to mask
        
    Returns:
        Masked email address
    """
    if not email or '@' not in email:
        return "***@***.***"
    
    username, domain = email.split('@', 1)
    
    # Mask username
    if len(username) <= 2:
        masked_username = "***"
    else:
        masked_username = username[:2] + "***"
    
    # Mask domain
    if '.' in domain:
        domain_name, tld = domain.rsplit('.', 1)
        if len(domain_name) <= 2:
            masked_domain = "***"
        else:
            masked_domain = domain_name[:2] + "***"
        masked_email = f"{masked_username}@{masked_domain}.{tld}"
    else:
        masked_email = f"{masked_username}@***"
    
    return masked_email


def mask_phone(phone: str) -> str:
    """Mask phone number.
    
    Format: ***-***-1234 (shows last 4 digits)
    
    Args:
        phone: Phone number to mask
        
    Returns:
        Masked phone number
    """
    # Extract digits
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 0:
        return "***-***-****"
    elif len(digits) <= 4:
        return "***-***-" + digits
    else:
        return "***-***-" + digits[-4:]


def mask_national_id(national_id: str) -> str:
    """Mask national ID (SSN).
    
    Format: ***-**-1234 (shows last 4 digits)
    
    Args:
        national_id: National ID to mask
        
    Returns:
        Masked national ID
    """
    # Extract digits
    digits = re.sub(r'\D', '', national_id)
    
    if len(digits) == 0:
        return "***-**-****"
    elif len(digits) <= 4:
        return "***-**-" + digits
    else:
        return "***-**-" + digits[-4:]


def mask_name(name: str) -> str:
    """Mask person's name.
    
    Format: J*** D*** (first letter of each word + ***)
    
    Args:
        name: Full name to mask
        
    Returns:
        Masked name
    """
    if not name or not name.strip():
        return "***"
    
    words = name.split()
    masked_words = []
    
    for word in words:
        if len(word) == 0:
            continue
        elif len(word) == 1:
            masked_words.append(word[0] + "***")
        else:
            masked_words.append(word[0] + "***")
    
    return " ".join(masked_words) if masked_words else "***"


def mask_address(address: str) -> str:
    """Mask street address.
    
    Format: *** *** *** (complete masking)
    
    Args:
        address: Street address to mask
        
    Returns:
        Masked address
    """
    return "*** *** ***"


def mask_date_of_birth(dob: str) -> str:
    """Mask date of birth.
    
    Format: **/**/1990 (shows only year)
    
    Args:
        dob: Date of birth to mask
        
    Returns:
        Masked date of birth
    """
    # Try to extract year - look for 4 consecutive digits anywhere in the string
    year_match = re.search(r'(\d{4})', dob)
    
    if year_match:
        year = year_match.group(1)
        return f"**/**/{year}"
    else:
        return "**/**/****"


def mask_field(field_name: str, value: str) -> str:
    """Mask field based on field name.
    
    Args:
        field_name: Name of the field
        value: Value to mask
        
    Returns:
        Masked value
    """
    field_lower = field_name.lower()
    
    if 'email' in field_lower:
        return mask_email(value)
    elif 'phone' in field_lower:
        return mask_phone(value)
    elif 'ssn' in field_lower or 'national_id' in field_lower:
        return mask_national_id(value)
    elif 'name' in field_lower:
        return mask_name(value)
    elif 'address' in field_lower:
        return mask_address(value)
    elif 'dob' in field_lower or 'birth' in field_lower:
        return mask_date_of_birth(value)
    else:
        return "***"
