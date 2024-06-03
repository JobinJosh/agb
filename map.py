import random
import matplotlib.pyplot as plt
import streamlit as st

class Person:
    def __init__(self, age, gender, education, employment, income, social_status, relatives_abroad):
        self.age = age
        self.gender = gender
        self.education = education
        self.employment = employment
        self.income = income
        self.social_status = social_status
        self.relatives_abroad = relatives_abroad
        self.accommodation = None

    def choose_accommodation(self):
        if self.income > 130 and self.education in ['Undergraduate', 'Postgraduate']:
            self.accommodation = 'Luxury Apartment'
        elif 50 <= self.income <= 130:
            self.accommodation = 'Standard Apartment'
        elif self.income < 50 and self.social_status == 'Single':
            self.accommodation = 'Shared Housing'
        elif self.social_status == 'Family' and self.income >= 50:
            self.accommodation = 'House'
        elif self.income < 50 and self.social_status == 'Family':
            self.accommodation = 'Public Housing'
        else:
            self.accommodation = 'Undefined'

def create_persons_and_plot(num_persons, education_probs, employment_probs, income_levels, social_status_probs, relatives_abroad_prob):
    persons = []
    accommodation_counts = {
        'Luxury Apartment': 0,
        'Standard Apartment': 0,
        'Shared Housing': 0,
        'House': 0,
        'Public Housing': 0,
        'Undefined': 0
    }

    for _ in range(num_persons):
        age = random.choices(['18-34', '35-50'], [0.66, 0.34])[0]
        gender = random.choices(['Female', 'Male'], [0.49, 0.51])[0]
        education = random.choices(
            ['No education', 'Primary', 'Secondary', 'Technical', 'Undergraduate', 'Postgraduate'],
            education_probs if gender == 'Female' else education_probs
        )[0]
        employment = random.choices(['Employed', 'Unemployed'], employment_probs)[0]
        income = random.choices(income_levels, [0.1, 0.4, 0.5])[0]
        social_status = random.choices(['Single', 'Family'], social_status_probs)[0]
        relatives_abroad = random.choices(['Yes', 'No'], [relatives_abroad_prob, 1 - relatives_abroad_prob])[0]

        person = Person(age, gender, education, employment, income, social_status, relatives_abroad)
        person.choose_accommodation()
        accommodation_counts[person.accommodation] += 1
        persons.append(person)

    labels = list(accommodation_counts.keys())
    counts = list(accommodation_counts.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, counts, color=['blue', 'green', 'red', 'purple', 'orange', 'gray'])
    ax.set_xlabel('Accommodation Type')
    ax.set_ylabel('Number of People')
    ax.set_title(f'Accommodation Choices of {num_persons} Persons')
    st.pyplot(fig)

# Streamlit UI
st.title('Accommodation Choices Based on Person Attributes')

num_persons = st.slider('Number of Persons', min_value=1000, max_value=20000, step=1000, value=10000)

education_probs = [
    st.slider('No Education Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.02),
    st.slider('Primary Education Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.115),
    st.slider('Secondary Education Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.515),
    st.slider('Technical Education Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.13),
    st.slider('Undergraduate Education Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.25),
    st.slider('Postgraduate Education Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.03)
]

employment_probs = [
    st.slider('Employed Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.07),
    st.slider('Unemployed Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.93)
]

income_levels = [100, 350, 1000]

social_status_probs = [
    st.slider('Single Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.51),
    st.slider('Family Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.47)
]

relatives_abroad_prob = st.slider('Relatives Abroad Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.18)

if st.button('Run Model'):
    create_persons_and_plot(num_persons, education_probs, employment_probs, income_levels, social_status_probs, relatives_abroad_prob)
