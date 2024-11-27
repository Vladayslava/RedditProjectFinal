from django.utils import timezone
from django.core.management.base import BaseCommand
from random import choice, randint, sample
from django.contrib.auth.models import User
from news.models import Category, Post, Comment, Vote, Profile
from faker import Faker

class Command(BaseCommand):
    help = 'Fills the database with realistic data in English language'

    def handle(self, *args, **kwargs):
        fake = Faker('en')
        
        posts_data = [
            ('Innovations in Technology: What to Expect in 2024', 'Technology',
             'Technological innovations open up new opportunities for societal development. In 2024, we expect new achievements in the fields of artificial intelligence and robotics.'),
            ('Science and Education: New Approaches to Learning', 'Education',
             'Modern education must adapt to a rapidly changing world. New approaches, such as distance learning, are becoming increasingly popular.'),
            ('Environmental Challenges of Today', 'Ecology',
             'Environmental challenges, such as climate change and pollution, require urgent solutions and global cooperation.'),
            ('Transformation of the Economy: Digital Solutions', 'Economy',
             'Digital technologies are transforming the economy by implementing new business models and improving productivity.'),
            ('Space Exploration: New Horizons', 'Space',
             'Space exploration opens new horizons for humanity. New missions to Mars and other planets could change our understanding of the Universe.'),
            ('Cybersecurity: How to Protect Your Data', 'Cybersecurity',
             'Data protection is becoming increasingly complex. Cybercriminals continuously improve their methods, making it important to take measures to protect personal information.'),
            ('The Future of Medicine: New Treatment Technologies', 'Medicine',
             'New technologies in medicine, such as telemedicine and genetic therapy, promise to revolutionize the treatment of diseases.'),
            ('Social Networks: Impact on Society', 'Society',
             '''Social networks have a significant impact on modern society, shaping people's opinions and behaviors.'''),
            ('Transport of the Future: Eco-Friendly Solutions', 'Ecology',
             'Eco-friendly initiatives in transport, such as electric vehicles, are becoming increasingly popular, helping to reduce carbon emissions.'),
            ('Environmental Protection: Initiatives and Solutions', 'Ecology',
             'Environmental protection is a shared responsibility. Initiatives aimed at reducing waste and conserving resources are gaining popularity.'),
            ('Intelligent Systems: Impact on Business', 'Economy',
             'Intelligent systems are becoming increasingly important for businesses as they help optimize processes and make better decisions.'),
            ('Climate Change: Challenges and Opportunities', 'Ecology',
             'Climate change is causing growing concern, and it is important to find ways to adapt and mitigate its effects.'),
            ('Virtual Reality: New Horizons for Entertainment', 'Technology',
             'Virtual reality opens up new possibilities for entertainment and learning, providing a unique experience for users.'),
            ('Ethics of Artificial Intelligence: Important Questions', 'Technology',
             'The ethics of artificial intelligence are coming to the forefront as concerns grow about its impact on society and privacy.'),
            ('Technologies in Medicine: Advantages and Risks', 'Medicine',
             'Technologies in medicine are changing the ways of treatment; however, their implementation comes with risks and ethical issues.'),
            ('Education During the Pandemic: Lessons for the Future', 'Education',
             'Education during the pandemic showed how important it is to have adaptive learning methods and readiness for change.'),
            ('Environmental Startups: Innovations for Sustainable Development', 'Ecology',
             'Environmental startups are becoming important players in the market, offering innovative solutions for sustainable development.'),
            ('Smart Cities: Technologies for Improving Life', 'Technology',
             'Smart cities use technology to improve the quality of life for residents and reduce emissions.'),
            ('Cryptocurrencies: What Investors Need to Know', 'Economy',
             'Cryptocurrencies are becoming increasingly popular among investors, but it is important to be aware of the associated risks.'),
            ('The Future of Work: Which Professions Will Disappear, and Which Will Arise?', 'Economy',
             'The future of work is changing: some professions will disappear while others will become in demand.')
        ]

        comments = [
            'Very interesting article, thank you!',
            'It is important to pay attention to these issues.',
            'Can I learn more about this topic?',
            'Great information, thank you!',
            'This is indeed relevant in our time.',
            'I agree with your opinion!',
            'More research is needed in this area.',
            'I wonder what the consequences will be?',
            'Can I read more on this topic?',
            'That’s a great question; I hope an answer will be found!',
            'I like that you brought up this topic.',
            'I am looking forward to new articles!',
            'Very useful information, thank you for your time.',
            'I believe this is important to discuss.',
            'This really requires more attention from society.',
            'I hope this project will be successful.',
            'I’m interested to hear other readers’ opinions.',
            'This is a problem we face every day.',
            'You raised an important question, thank you for the article.',
            'I would like to learn more about your sources of information.'
        ]

        self.stdout.write('Creating users...')
        for _ in range(20):
            username = fake.unique.user_name()
            email = fake.unique.email()
            User.objects.create_user(username=username, email=email, password=fake.password())

        self.stdout.write('Creating categories...')
        categories = [
            'Technology', 'Science', 'Economy', 'Education', 'Ecology', 
            'Medicine', 'Space', 'Cybersecurity', 'Transport', 'Society'
        ]
        for name in categories:
            Category.objects.create(name=name, creator=User.objects.order_by('?').first())

        self.stdout.write('Creating posts...')
        for title, category_name, content in posts_data:
            category = Category.objects.get(name=category_name)  
            Post.objects.create(title=title, 
                                content=content, 
                                category=category, 
                                author=User.objects.order_by('?').first(), 
                                created_at=fake.date_time_between(start_date='-6m', end_date='now', tzinfo=timezone.get_current_timezone())
                                )

        self.stdout.write('Adding comments to posts...')
        posts = Post.objects.all()
        for post in posts:
            for _ in range(randint(1, 5)):  
                comment_text = choice(comments)
                Comment.objects.create(post=post, 
                                       content=comment_text, 
                                       author=User.objects.order_by('?').first(), 
                                       created_at=fake.date_time_between(start_date=post.created_at, end_date='now', tzinfo=timezone.get_current_timezone())
                                       )

        self.stdout.write('Creating votes...')
        for post in Post.objects.all():
            users = sample(list(User.objects.all()), k=randint(5, 15))
            for user in users:
                Vote.objects.create(
                    post=post,
                    user=user,
                    value=choice([-1, 1])
                )

        self.stdout.write(self.style.SUCCESS('The database has been successfully filled!'))
