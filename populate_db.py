"""
Database population script with test data
Usage: python manage.py shell < populate_db.py
"""

import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')
django.setup()

from catalog.models import Redactor, Topic, Article

# Clear existing data (optional)
print("Clearing existing data...")
Article.objects.all().delete()
Topic.objects.all().delete()
Redactor.objects.all().delete()

print("Creating redactors...")

# Create superuser
if not Redactor.objects.filter(username='admin').exists():
    Redactor.objects.create_superuser(
        username='admin',
        email='admin@newspaper.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        years_of_experience=20
    )
    print("✓ Created superuser: admin / admin123")

# Create redactors
redactors_data = [
    {
        'username': 'john_smith',
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john.smith@newspaper.com',
        'years_of_experience': 10
    },
    {
        'username': 'emily_johnson',
        'first_name': 'Emily',
        'last_name': 'Johnson',
        'email': 'emily.johnson@newspaper.com',
        'years_of_experience': 7
    },
    {
        'username': 'michael_brown',
        'first_name': 'Michael',
        'last_name': 'Brown',
        'email': 'michael.brown@newspaper.com',
        'years_of_experience': 15
    },
    {
        'username': 'sarah_davis',
        'first_name': 'Sarah',
        'last_name': 'Davis',
        'email': 'sarah.davis@newspaper.com',
        'years_of_experience': 5
    },
    {
        'username': 'david_wilson',
        'first_name': 'David',
        'last_name': 'Wilson',
        'email': 'david.wilson@newspaper.com',
        'years_of_experience': 12
    },
]

redactors = []
for data in redactors_data:
    redactor = Redactor.objects.create_user(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password='password123',
        years_of_experience=data['years_of_experience']
    )
    redactors.append(redactor)
    print(f"✓ Created redactor: {redactor.first_name} {redactor.last_name} ({data['years_of_experience']} years of experience)")

print("\nCreating topics...")

# Create topics
topics_data = [
    'Technology',
    'Politics',
    'Economy',
    'Science',
    'Sports',
    'Culture',
    'Health',
    'Travel',
    'Environment',
    'Education'
]

topics = []
for name in topics_data:
    topic = Topic.objects.create(name=name)
    topics.append(topic)
    print(f"✓ Created topic: {topic.name}")

print("\nCreating articles...")

# Helper function to generate dates
def random_date(start_days_ago=60, end_days_ago=0):
    days_ago = random.randint(end_days_ago, start_days_ago)
    return date.today() - timedelta(days=days_ago)

# Create articles
articles_data = [
    {
        'title': 'Artificial Intelligence Reshaping the Tech Industry',
        'content': '''Artificial intelligence continues to revolutionize the technology sector. 
        New machine learning models demonstrate impressive results in natural language processing,
        computer vision, and process automation. Experts predict that in the coming years, AI will become
        an integral part of people's daily lives, transforming industries from healthcare to finance.''',
        'topic': topics[0],  # Technology
        'published_date': random_date(30, 15),
        'redactors': [redactors[0], redactors[1]]
    },
    {
        'title': 'Quantum Computers: A Breakthrough in Computing',
        'content': '''Researchers have reached a new milestone in quantum computer development.
        The new architecture allows for a significant increase in the number of qubits and reduction in error rates.
        This opens the way to solving complex problems in cryptography, molecular modeling, and optimization.
        Major tech companies are investing billions in quantum computing research.''',
        'topic': topics[3],  # Science
        'published_date': random_date(25, 10),
        'redactors': [redactors[2]]
    },
    {
        'title': 'Global Economy: Trends for 2025',
        'content': '''Analysts note steady growth in the global economy in 2025.
        The main growth drivers are the technology sector and renewable energy.
        However, risks remain related to geopolitical tensions and inflation.
        Emerging markets show particularly strong performance this quarter.''',
        'topic': topics[2],  # Economy
        'published_date': random_date(20, 5),
        'redactors': [redactors[3]]
    },
    {
        'title': 'Olympic Games: New Records and Achievements',
        'content': '''At the Olympic Games, numerous new world records were set.
        Athletes demonstrate outstanding results thanks to modern training methods
        and sports technologies. Particularly impressive were achievements in athletics and swimming.
        The host nation celebrates unprecedented medal success.''',
        'topic': topics[4],  # Sports
        'published_date': random_date(15, 1),
        'redactors': [redactors[0], redactors[4]]
    },
    {
        'title': 'New Contemporary Art Exhibition Opens at Museum',
        'content': '''A large-scale contemporary art exhibition has opened at the city museum.
        The exhibition presents works by more than 50 artists from different countries.
        Visitors can explore various movements: from abstractionism to digital art.
        Interactive installations allow audience participation in the creative process.''',
        'topic': topics[5],  # Culture
        'published_date': random_date(40, 25),
        'redactors': [redactors[1], redactors[3]]
    },
    {
        'title': 'Breakthrough in Cancer Treatment Research',
        'content': '''Scientists have developed a new immunotherapy method for cancer treatment.
        Clinical trials showed high effectiveness of the new approach with minimal side effects.
        This gives hope to millions of patients worldwide. The treatment targets specific cancer cells
        while preserving healthy tissue, marking a significant advancement in oncology.''',
        'topic': topics[6],  # Health
        'published_date': random_date(35, 20),
        'redactors': [redactors[2], redactors[4]]
    },
    {
        'title': 'Top 10 Travel Destinations for 2025',
        'content': '''Travel industry experts have compiled a ranking of the most popular destinations.
        The list includes both traditional tourist routes and new exotic locations.
        Special attention is paid to eco-tourism and authentic experiences.
        Sustainable travel practices are becoming increasingly important to modern travelers.''',
        'topic': topics[7],  # Travel
        'published_date': random_date(50, 35),
        'redactors': [redactors[0], redactors[1]]
    },
    {
        'title': 'Climate Change: Challenges and Solutions',
        'content': '''The international climate summit has developed new strategies to combat global warming.
        Countries agreed to accelerate the transition to renewable energy sources
        and reduce greenhouse gas emissions. Experts consider these measures critically important
        for the planet's future. New technologies in carbon capture show promising results.''',
        'topic': topics[8],  # Environment
        'published_date': random_date(45, 30),
        'redactors': [redactors[2], redactors[3]]
    },
    {
        'title': 'Digital Transformation in Business',
        'content': '''Companies worldwide are actively implementing digital technologies.
        Cloud solutions, big data, and process automation are becoming the standard for modern business.
        This allows for increased efficiency and competitiveness. Small businesses are also
        embracing digital tools, leveling the playing field with larger corporations.''',
        'topic': topics[0],  # Technology
        'published_date': random_date(28, 12),
        'redactors': [redactors[1], redactors[4]]
    },
    {
        'title': 'Education System Reform Announced',
        'content': '''The government has announced a large-scale reform of the educational system.
        The main focus is on developing critical thinking and practical skills.
        Plans also include strengthening the role of digital technologies in the educational process.
        Teachers will receive additional training in modern pedagogical methods.''',
        'topic': topics[9],  # Education
        'published_date': random_date(22, 8),
        'redactors': [redactors[3], redactors[4]]
    },
    {
        'title': 'Cybersecurity Threats on the Rise',
        'content': '''Cybersecurity experts warn of increasing sophistication in cyberattacks.
        Organizations must implement robust security measures and employee training programs.
        The rise of AI-powered attacks requires equally advanced defensive strategies.
        Investment in cybersecurity infrastructure has become critical for all businesses.''',
        'topic': topics[0],  # Technology
        'published_date': random_date(18, 5),
        'redactors': [redactors[2]]
    },
    {
        'title': 'Renewable Energy Reaches New Milestone',
        'content': '''Renewable energy sources now account for over 40% of global electricity generation.
        Solar and wind power costs continue to decline, making them competitive with fossil fuels.
        Battery storage technology improvements enable 24/7 renewable power supply.
        Governments worldwide are setting ambitious clean energy targets for 2030.''',
        'topic': topics[8],  # Environment
        'published_date': random_date(32, 18),
        'redactors': [redactors[0], redactors[2]]
    },
    {
        'title': 'Global Food Security Initiative Launched',
        'content': '''International organizations launch comprehensive food security program.
        The initiative focuses on sustainable agriculture and reducing food waste.
        Innovative farming techniques promise to increase yields while protecting the environment.
        Collaboration between developed and developing nations is key to program success.''',
        'topic': topics[2],  # Economy
        'published_date': random_date(38, 22),
        'redactors': [redactors[3], redactors[4]]
    },
    {
        'title': 'Mental Health Awareness Campaign Goes Viral',
        'content': '''A new mental health awareness campaign has reached millions worldwide.
        The initiative aims to reduce stigma and encourage people to seek help.
        Mental health professionals report increased demand for services.
        Workplace wellness programs are becoming standard practice in major corporations.''',
        'topic': topics[6],  # Health
        'published_date': random_date(26, 10),
        'redactors': [redactors[1], redactors[2]]
    },
    {
        'title': 'Championship Finals Draw Record Viewership',
        'content': '''The championship finals attracted the largest television audience in history.
        Spectacular performances and dramatic moments captivated viewers globally.
        Social media engagement broke all previous records during the event.
        The economic impact on the host city exceeded initial projections.''',
        'topic': topics[4],  # Sports
        'published_date': random_date(12, 2),
        'redactors': [redactors[0]]
    },
]

for data in articles_data:
    redactors_list = data.pop('redactors')
    article = Article.objects.create(**data)
    article.redactors.set(redactors_list)
    redactors_names = ', '.join([f"{r.first_name} {r.last_name}" for r in redactors_list])
    print(f"✓ Created article: '{article.title}' (Redactors: {redactors_names})")

print("\n" + "="*60)
print("Database successfully populated!")
print("="*60)
print("\nStatistics:")
print(f"Redactors: {Redactor.objects.count()}")
print(f"Topics: {Topic.objects.count()}")
print(f"Articles: {Article.objects.count()}")
print("\nLogin credentials:")
print("Superuser: admin / admin123")
print("Redactors: username / password123")
print("  - john_smith")
print("  - emily_johnson")
print("  - michael_brown")
print("  - sarah_davis")
print("  - david_wilson")