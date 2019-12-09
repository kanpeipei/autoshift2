from django import forms
from .models import RequestedShifts


# class RequestedShiftsForm(forms.ModelForm):
#     class Meta:
#         model = RequestedShifts
#         exclude = ['member', 'year', 'month', 'day', 'created_at', 'updated_at']

class RequestedShiftsForm(forms.Form):
    since = forms.ChoiceField(
        choices=(
            (9, '9'),
            (10, '10'),
            (11, '11'),
            (12, '12'),
            (13, '13'),
            (14, '14'),
            (15, '15'),
            (16, '16'),
            (17, '17'),
            (18, '18'),
            (19, '19'),
            (20, '20'),
            (21, '21'),
        ),
        required=True,
    )
    to = forms.ChoiceField(
        choices=(
            (10, '10'),
            (11, '11'),
            (12, '12'),
            (13, '13'),
            (14, '14'),
            (15, '15'),
            (16, '16'),
            (17, '17'),
            (18, '18'),
            (19, '19'),
            (20, '20'),
            (21, '21'),
            (22, '22'),
        ),
        required=True,
    )
    is_absence = forms.BooleanField(required=False)


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