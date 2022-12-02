from django.test import TestCase
from datetime import date
from actors.models import Actor, Bio
from django.db import IntegrityError
from films.models import Film, ProductionCompany
from actors.models import Actor


class ActorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.first_name = "John"
        cls.last_name = "Doe"
        cls.birthdate = date.fromisoformat("1990-01-01")
        cls.retire = False

        cls.actor = Actor.objects.create(
            first_name=cls.first_name,
            last_name=cls.last_name,
            birthdate=cls.birthdate,
            retire=cls.retire,
        )

        cls.description_bio = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua."""

    def test_if_the_actor_can_have_a_biography(self):
        created_bio = Bio.objects.create(description=self.description_bio)

        self.actor.bio = created_bio
        self.actor.save()

        self.assertIs(self.actor.bio, created_bio)
        self.assertIs(self.actor, created_bio.actor)

    def test_if_raise_error_when_bio_already_have_an_actor(self):
        created_bio = Bio.objects.create(description=self.description_bio)

        self.actor.bio = created_bio
        self.actor.save()

        with self.assertRaises(IntegrityError):
            actor_two = Actor.objects.create(
                first_name="Max",
                last_name="Green",
                birthdate=date.fromisoformat("1995-12-01"),
                retire=False,
            )

            actor_two.bio = created_bio
            actor_two.save()

    class FilmModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            cls.films = [Film.objects.create(cache=500000) for _ in range(20)]

            cls.production_company = ProductionCompany.objects.create(
                name="Kenzie Studios"
            )

        def test_production_company_may_contain_multiple_films(self):

            for film in self.films:
                film.company = self.production_company
                film.save()

            self.assertEquals(len(self.films), self.production_company.films.count())

            for film in self.films:
                self.assertIs(film.company, self.production_company)

        def test_film_cannot_belong_to_more_than_one_production_company(self):
            for film in self.films:
                film.company = self.production_company
                film.save()

            production_company_two = ProductionCompany.objects.create(
                name="Outra Produtora"
            )

            for film in self.films:
                film.company = production_company_two
                film.save()

            for film in self.films:
                self.assertNoIn(film, self.production_company.films.all())
                self.assertIn(film, production_company_two.films.all())

    class ActorAndFilmsModelTest(TestCase):
        @classmethod
        def serUpTestData(cls):
            cls.first_name = "John"
            cls.last_name = "Doe"
            cls.birthdate = date.fromisoformat("1990-01-01")
            cls.retire = False
            cls.actor = Actor.objects.create(
                first_name=cls.first_name,
                last_name=cls.last_name,
                birthdate=cls.birthdate,
                retire=cls.retire,
            )

            cls.films = [Film.objects.create(cache=500000) for _ in range(20)]

        def test_actor_can_be_attached_to_multiple_films(self):

            for film in self.films:
                self.actor.films.add(film)

            self.assertEquals(len(self.films), self.actor.films.count())

            for film in self.films:
                self.assertIn(self.actor, film.actors.all())
