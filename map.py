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
        elif 0 <= self.income <= 250:
            self.accommodation = 'Public Housing'
        else:
            self.accommodation = 'Undefined'

def create_persons_and_plot(num_persons, education_probs, employment_probs, income_probs, social_status_probs, relatives_abroad_prob):
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
        income = random.choices([100, 350, 1000], income_probs)[0]
        social_status = random.choices(['Single', 'Family'], social_status_probs)[0]
        relatives_abroad = random.choices(['Yes', 'No'], [relatives_abroad_prob, 1 - relatives_abroad_prob])[0]

        person = Person(age, gender, education, employment, income, social_status, relatives_abroad)
        person.choose_accommodation()
        accommodation_counts[person.accommodation] += 1
        persons.append(person)

    labels = list(accommodation_counts.keys())
    counts = list(accommodation_counts.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, counts, color=['blue', 'green', 'red', 'purple', 'orange', 'gray'])
    ax.set_xlabel('Accommodation Type')
    ax.set_ylabel('Number of People')
    ax.set_title(f'Accommodation Choices of {num_persons} Persons')
    
    # Add text annotations on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    st.pyplot(fig)

    return persons, accommodation_counts

def plot_resource_usage(resource, usage_counts, labels):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, usage_counts, color=['blue', 'green', 'red', 'purple', 'orange', 'gray'])
    ax.set_xlabel('Accommodation Type')
    ax.set_ylabel(f'{resource} Usage')
    ax.set_title(f'{resource} Usage by Accommodation Type')
    
    # Add text annotations on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    st.pyplot(fig)

def calculate_resource_usage(persons):
    # Parameters for resource usage
    accommodation_needs = {
        'Luxury Apartment': {
            'water': 567.81,  # liters per person per day
            'electricity': 15,  # kWh per person per day
            'heating': 63.09,  # MJ per sqm per day
            'cooling': 31.55,  # MJ per sqm per day
            'land': 65  # sqm per person
        },
        'House': {
            'water': 454.25,
            'electricity': 12,
            'heating': 52.57,
            'cooling': 26.28,
            'land': 55
        },
        'Standard Apartment': {
            'water': 378.54,
            'electricity': 10,
            'heating': 42.05,
            'cooling': 21.03,
            'land': 46
        },
        'Shared Housing': {
            'water': 302.83,
            'electricity': 8,
            'heating': 31.54,
            'cooling': 15.78,
            'land': 37
        },
        'Public Housing': {
            'water': 227.12,
            'electricity': 6,
            'heating': 21.03,
            'cooling': 10.52,
            'land': 28
        },
        'Undefined': {
            'water': 0,
            'electricity': 0,
            'heating': 0,
            'cooling': 0,
            'land': 0
        }
    }

    # Initialize totals
    total_water_usage = 0
    total_electricity_usage = 0
    total_heating_mj = 0
    total_cooling_mj = 0
    total_land = 0

    # Initialize accommodation-specific counts
    accommodation_water = {key: 0 for key in accommodation_needs}
    accommodation_electricity = {key: 0 for key in accommodation_needs}
    accommodation_heating = {key: 0 for key in accommodation_needs}
    accommodation_cooling = {key: 0 for key in accommodation_needs}
    accommodation_land = {key: 0 for key in accommodation_needs}

    # Calculate resource needs based on accommodation type
    for person in persons:
        needs = accommodation_needs[person.accommodation]
        accommodation_water[person.accommodation] += needs['water']
        accommodation_electricity[person.accommodation] += needs['electricity']
        accommodation_heating[person.accommodation] += needs['heating']
        accommodation_cooling[person.accommodation] += needs['cooling']
        accommodation_land[person.accommodation] += needs['land']

    return accommodation_water, accommodation_electricity, accommodation_heating, accommodation_cooling, accommodation_land

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

income_probs = [
    st.slider('Income $0-250 Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.1),
    st.slider('Income $250-500 Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.4),
    st.slider('Income $500+ Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.5)
]

social_status_probs = [
    st.slider('Single Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.51),
    st.slider('Family Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.47)
]

relatives_abroad_prob = st.slider('Relatives Abroad Probability', min_value=0.0, max_value=1.0, step=0.01, value=0.18)

if st.button('Run Model'):
    persons, accommodation_counts = create_persons_and_plot(num_persons, education_probs, employment_probs, income_probs, social_status_probs, relatives_abroad_prob)

    accommodation_water, accommodation_electricity, accommodation_heating, accommodation_cooling, accommodation_land = calculate_resource_usage(persons)

    plot_resource_usage('Water (liters)', list(accommodation_water.values()), list(accommodation_water.keys()))
    plot_resource_usage('Electricity (kWh)', list(accommodation_electricity.values()), list(accommodation_electricity.keys()))
    plot_resource_usage('Heating (MJ)', list(accommodation_heating.values()), list(accommodation_heating.keys()))
    plot_resource_usage('Cooling (MJ)', list(accommodation_cooling.values()), list(accommodation_cooling.keys()))
    plot_resource_usage('Land (sqm)', list(accommodation_land.values()), list(accommodation_land.keys()))

    # Display the results
    st.write(f"Total Water Usage: {sum(accommodation_water.values()):.2f} liters per day")
    st.write(f"Total Electricity Usage: {sum(accommodation_electricity.values()):.2f} kWh per day")
    st.write(f"Total Heating Requirement: {sum(accommodation_heating.values()):.2f} MJ per day")
    st.write(f"Total Cooling Requirement: {sum(accommodation_cooling.values()):.2f} MJ per day")
    st.write(f"Total Land Required: {sum(accommodation_land.values()):.2f} sqm")
