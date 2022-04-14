# Datasets
compas = {
    'tag': 'compas',
    'name': 'ProPublica recidivism',
    'filename': 'propublica-recidivism_numerical-binsensitive_slim.csv',
    'Y': 'two_year_recid',
    'numerical_attributes': ['age', 'juv_fel_count', 'juv_misd_count', 'juv_other_count', 'priors_count']
}
german = {
    'tag': 'german',
    'name': 'German credit',
    'filename': 'german_numerical-binsensitive.csv',
    'Y': 'credit',
    'numerical_attributes': ['month', 'credit_amount', 'investment_as_income_percentage', 'residence_since', 'number_of_credits', 'people_liable_for']
}

adult = {
    'tag': 'adult',
    'name': 'Adult income',
    'filename': 'adult_numerical-binsensitive.csv',
    'Y': 'income-per-year',
    'numerical_attributes': ['age', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
}

chosen_dataset = german