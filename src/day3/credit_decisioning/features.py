"""Feature engineering module for credit decisioning."""


def calculate_dti(monthly_debt_payments: float, annual_income: float) -> float:
    """Calculate debt-to-income ratio.
    
    Args:
        monthly_debt_payments: Monthly debt obligations
        annual_income: Annual income
    
    Returns:
        DTI ratio (monthly debt / monthly income)
    
    Example:
        >>> calculate_dti(1000, 60000)
        0.2
    """
    if annual_income <= 0:
        return float('inf')
    
    monthly_income = annual_income / 12
    return monthly_debt_payments / monthly_income


def calculate_affordability_ratio(requested_amount: float, annual_income: float) -> float:
    """Calculate credit exposure as percentage of annual income.
    
    Args:
        requested_amount: Requested credit amount
        annual_income: Annual income
    
    Returns:
        Affordability ratio (requested_amount / annual_income)
    
    Example:
        >>> calculate_affordability_ratio(15000, 60000)
        0.25
    """
    if annual_income <= 0:
        return float('inf')
    
    return requested_amount / annual_income


def derive_features(application_data: dict) -> dict:
    """Derive all features needed for scoring.
    
    Args:
        application_data: Dict with keys: annual_income, monthly_debt_payments,
                         requested_amount, employment_years, missed_payments_12m
    
    Returns:
        Dict with: dti, affordability_ratio, annual_income, requested_amount,
                  employment_years, missed_payments_12m
    
    Example:
        >>> data = {
        ...     'annual_income': 60000,
        ...     'monthly_debt_payments': 1000,
        ...     'requested_amount': 15000,
        ...     'employment_years': 5,
        ...     'missed_payments_12m': 0
        ... }
        >>> features = derive_features(data)
        >>> round(features['dti'], 2)
        0.2
        >>> features['affordability_ratio']
        0.25
    """
    annual_income = application_data['annual_income']
    monthly_debt_payments = application_data['monthly_debt_payments']
    requested_amount = application_data['requested_amount']
    employment_years = application_data['employment_years']
    missed_payments_12m = application_data['missed_payments_12m']
    
    dti = calculate_dti(monthly_debt_payments, annual_income)
    affordability_ratio = calculate_affordability_ratio(requested_amount, annual_income)
    
    return {
        'dti': dti,
        'affordability_ratio': affordability_ratio,
        'annual_income': annual_income,
        'requested_amount': requested_amount,
        'employment_years': employment_years,
        'missed_payments_12m': missed_payments_12m
    }
