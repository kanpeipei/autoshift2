from django import forms


class YearMonthForm(forms.Form):
    year = forms.ChoiceField(
        choices=(
            (2019, '2019'),
            (2020, '2020'),
            (2021, '2021'),
            (2022, '2022'),
            (2023, '2023'),
            (2024, '2024'),
            (2025, '2025'),
            (2026, '2026'),
            (2027, '2027'),
            (2028, '2028'),
            (2029, '2029'),
        ),
        required=True
    )

    month = forms.ChoiceField(
        choices=(
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, 11),
            (12, 12),
        ),
        required=True
    )