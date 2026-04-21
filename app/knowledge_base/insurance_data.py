"""
Life Insurance Knowledge Base
Contains comprehensive information about life insurance policies, coverage, and procedures.
"""

LIFE_INSURANCE_KNOWLEDGE = [
    # Policy Types
    {
        "category": "policy_types",
        "content": """Term Life Insurance: Provides coverage for a specific period (10, 20, or 30 years).
        It's the most affordable type of life insurance. If the insured dies during the term, beneficiaries
        receive the death benefit. No cash value accumulation. Best for temporary needs like mortgage protection
        or income replacement during working years."""
    },
    {
        "category": "policy_types",
        "content": """Whole Life Insurance: Permanent life insurance that provides coverage for your entire lifetime.
        It includes a cash value component that grows over time at a guaranteed rate. Premiums are fixed and
        higher than term life. The policy builds cash value that you can borrow against or withdraw.
        Good for estate planning and long-term financial goals."""
    },
    {
        "category": "policy_types",
        "content": """Universal Life Insurance: A flexible permanent life insurance policy. You can adjust premiums
        and death benefits within certain limits. The cash value earns interest based on market rates.
        More complex than whole life but offers greater flexibility. Suitable for those who want permanent
        coverage with investment options."""
    },
    {
        "category": "policy_types",
        "content": """Variable Life Insurance: Permanent insurance where the cash value is invested in sub-accounts
        similar to mutual funds. The death benefit and cash value can fluctuate based on investment performance.
        Higher risk but potential for higher returns. Requires active management and understanding of investments."""
    },

    # Coverage and Benefits
    {
        "category": "benefits",
        "content": """Death Benefit: The primary benefit of life insurance is the tax-free lump sum paid to
        beneficiaries upon the insured's death. This money can be used for funeral expenses, debt repayment,
        mortgage payments, education costs, or income replacement. The amount should typically be 10-12 times
        your annual income."""
    },
    {
        "category": "benefits",
        "content": """Cash Value Accumulation: Permanent life insurance policies build cash value over time.
        This functions as a savings component that grows tax-deferred. You can borrow against it, withdraw it,
        or use it to pay premiums. The cash value reduces the death benefit if not repaid."""
    },
    {
        "category": "benefits",
        "content": """Living Benefits (Accelerated Death Benefits): Many policies allow you to access a portion
        of the death benefit if diagnosed with a terminal illness (typically 12-24 months to live). This can
        help cover medical expenses or end-of-life care. The amount accessed reduces the final death benefit."""
    },
    {
        "category": "benefits",
        "content": """Policy Loans: Permanent life insurance allows you to borrow against the cash value at
        competitive interest rates. The loan doesn't require credit checks or repayment schedules. However,
        unpaid loans with interest reduce the death benefit. If the loan exceeds cash value, the policy may lapse."""
    },

    # Eligibility
    {
        "category": "eligibility",
        "content": """Age Requirements: Most life insurance policies are available for individuals aged 18-75.
        Term life insurance typically has age limits of 65-75 for new policies. Whole life and permanent policies
        may be available up to age 85. Premiums increase significantly with age."""
    },
    {
        "category": "eligibility",
        "content": """Health Underwriting: Life insurance requires a medical evaluation. Factors considered include:
        current health conditions (diabetes, heart disease, cancer history), family medical history,
        lifestyle habits (smoking, alcohol use), height/weight ratio (BMI), and prescription medications.
        Better health equals lower premiums."""
    },
    {
        "category": "eligibility",
        "content": """Occupation and Lifestyle: High-risk occupations (pilots, construction workers, miners)
        or dangerous hobbies (skydiving, rock climbing, racing) may result in higher premiums or exclusions.
        Some insurers specialize in high-risk individuals. Disclosure is mandatory to avoid claim denials."""
    },
    {
        "category": "eligibility",
        "content": """Financial Underwriting: Insurers assess your income and net worth to determine appropriate
        coverage amounts. You typically need to demonstrate insurable interest and financial justification for
        the death benefit amount. Very high coverage amounts (over $1 million) require detailed financial documentation."""
    },

    # Claims Process
    {
        "category": "claims",
        "content": """Filing a Death Claim: Beneficiaries must contact the insurance company and submit a
        certified death certificate, completed claim form, and policy document. Most claims are processed
        within 30-60 days. Multiple beneficiaries split proceeds according to the policy designation."""
    },
    {
        "category": "claims",
        "content": """Contestability Period: The first two years of a policy are the contestability period.
        During this time, insurers can investigate and potentially deny claims if they discover material
        misrepresentation on the application. After two years, claims are generally incontestable except
        for non-payment of premiums."""
    },
    {
        "category": "claims",
        "content": """Common Claim Denial Reasons: Claims may be denied for: suicide within the first two years
        (suicide clause), death during illegal activities, material misrepresentation on the application,
        lapsed policy due to non-payment, or death from excluded causes. Beneficiaries can appeal denials."""
    },
    {
        "category": "claims",
        "content": """Claim Payment Options: Beneficiaries can receive death benefits as a lump sum,
        installment payments over time, life income (annuity), interest-only payments (retaining principal),
        or a combination. Lump sum is most common. Installments can provide steady income for financial security."""
    },

    # Premium and Costs
    {
        "category": "costs",
        "content": """Premium Factors: Life insurance premiums are based on age (older = higher cost),
        gender (women typically pay less), health status, smoking status (smokers pay 2-3x more),
        coverage amount, policy term/type, and family medical history. Premiums for term life are fixed
        for the term period."""
    },
    {
        "category": "costs",
        "content": """Cost Comparison: Term life is cheapest - a healthy 30-year-old might pay $20-30/month
        for $500,000 in 20-year coverage. Whole life costs 5-15 times more for the same death benefit.
        Universal and variable life fall in between. Get quotes from multiple insurers as rates vary significantly."""
    },
    {
        "category": "costs",
        "content": """Ways to Lower Premiums: Improve health before applying (lose weight, quit smoking for 12+ months,
        manage chronic conditions), buy coverage while young, choose term over permanent insurance,
        pay annually instead of monthly, consider a longer term for term life, and compare multiple insurers."""
    },

    # Policy Management
    {
        "category": "management",
        "content": """Changing Beneficiaries: You can change beneficiaries at any time unless designated as
        irrevocable. Complete a change of beneficiary form with the insurer. Common during life events like
        marriage, divorce, birth of children, or death of a beneficiary. Always name contingent beneficiaries."""
    },
    {
        "category": "management",
        "content": """Converting Term to Permanent: Most term life policies include a conversion option allowing
        you to convert to permanent insurance without medical underwriting. This must be done before the
        conversion deadline (typically before age 65 or before term ends). Useful if health has declined."""
    },
    {
        "category": "management",
        "content": """Policy Lapse and Reinstatement: Policies lapse if premiums aren't paid within the grace
        period (typically 30 days). Term policies usually can't be reinstated. Permanent policies may be
        reinstated within 3-5 years by paying back premiums with interest and providing evidence of insurability."""
    },
    {
        "category": "management",
        "content": """Surrendering a Policy: You can surrender (cancel) permanent life insurance and receive
        the cash surrender value. Surrender charges apply in early years. Surrendering ends coverage and
        may have tax consequences if cash value exceeds premiums paid. Consider alternatives like policy loans first."""
    },
]


def get_knowledge_base() -> list[dict]:
    """Returns the complete life insurance knowledge base."""
    return LIFE_INSURANCE_KNOWLEDGE


def get_categories() -> list[str]:
    """Returns all available knowledge categories."""
    return list(set(item["category"] for item in LIFE_INSURANCE_KNOWLEDGE))
