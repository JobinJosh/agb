import random
import matplotlib.pyplot as plt
import streamlit as st

# Class to represent a person with various attributes
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

    # Method to determine the accommodation type based on person's attributes
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

# Function to create persons, simulate accommodation choices, and plot results
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
            education_probs
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

# Function to plot resource usage
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

# Function to calculate resource usage based on accommodation types
def calculate_resource_usage(persons):
    # Parameters for resource usage based on European standards
    accommodation_needs = {
        'Luxury Apartment': {
            'water': 300,  # liters per person per day
            'electricity': 20,  # kWh per person per day
            'heating': 75,  # MJ per sqm per year, converted below
            'cooling': 37.5,  # MJ per sqm per year, converted below
            'land': 65  # sqm per person
        },
        'House': {
            'water': 250,
            'electricity': 15,
            'heating': 70,
            'cooling': 35,
            'land': 55
        },
        'Standard Apartment': {
            'water': 200,
            'electricity': 10,
            'heating': 65,
            'cooling': 32.5,
            'land': 46
        },
        'Shared Housing': {
            'water': 150,
            'electricity': 7,
            'heating': 60,
            'cooling': 30,
            'land': 37
        },
        'Public Housing': {
            'water': 100,
            'electricity': 5,
            'heating': 55,
            'cooling': 27.5,
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

    # Convert annual MJ per sqm to daily MJ per person
    days_per_year = 365
    persons_per_accommodation = {
        'Luxury Apartment': 1.5,  # assuming 1.5 persons per luxury apartment
        'House': 3,  # assuming 3 persons per house
        'Standard Apartment': 2,  # assuming 2 persons per standard apartment
        'Shared Housing': 4,  # assuming 4 persons per shared housing
        'Public Housing': 4,  # assuming 4 persons per public housing
        'Undefined': 1
    }

    for accommodation, needs in accommodation_needs.items():
        needs['heating'] = (needs['heating'] * persons_per_accommodation[accommodation]) / days_per_year
        needs['cooling'] = (needs['cooling'] * persons_per_accommodation[accommodation]) / days_per_year

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

num_persons = st.slider('Number of Persons', min_value=10, max_value=1000, value=100, step=10)
education_probs = st.slider('Education Probabilities', 0.0, 1.0, value=[0.1, 0.2, 0.2, 0.2, 0.2, 0.1])
employment_probs = st.slider('Employment Probabilities', 0.0, 1.0, value=[0.8, 0.2])
income_probs = st.slider('Income Probabilities', 0.0, 1.0, value=[0.4, 0.3, 0.3])
social_status_probs = st.slider('Social Status Probabilities', 0.0, 1.0, value=[0.6, 0.4])
relatives_abroad_prob = st.slider('Relatives Abroad Probability', 0.0, 1.0, value=0.2)

education_probs = [p/sum(education_probs) for p in education_probs]
employment_probs = [p/sum(employment_probs) for p in employment_probs]
income_probs = [p/sum(income_probs) for p in income_probs]
social_status_probs = [p/sum(social_status_probs) for p in social_status_probs]

if st.button('Generate and Plot Data'):
    persons, accommodation_counts = create_persons_and_plot(num_persons, education_probs, employment_probs, income_probs, social_status_probs, relatives_abroad_prob)
    
    accommodation_water, accommodation_electricity, accommodation_heating, accommodation_cooling, accommodation_land = calculate_resource_usage(persons)
    
    st.subheader('Resource Usage')
    
    st.write('### Water Usage')
    plot_resource_usage('Water', list(accommodation_water.values()), list(accommodation_water.keys()))
    
    st.write('### Electricity Usage')
    plot_resource_usage('Electricity', list(accommodation_electricity.values()), list(accommodation_electricity.keys()))
    
    st.write('### Heating Usage')
    plot_resource_usage('Heating', list(accommodation_heating.values()), list(accommodation_heating.keys()))
    
    st.write('### Cooling Usage')
    plot_resource_usage('Cooling', list(accommodation_cooling.values()), list(accommodation_cooling.keys()))
    
    st.write('### Land Usage')
    plot_resource_usage('Land', list(accommodation_land.values()), list(accommodation_land.keys()))
