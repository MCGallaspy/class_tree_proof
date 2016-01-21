import random
import time

from django.test import TestCase
from .models import *


class TestBenchmark(TestCase):
    fixtures = ["treedump.json"]

    def test_sanity(self):
        facility = Facility.objects.all().first()
        self.assertEqual(facility.node.get_descendants().count(), 6100)  # Magic number comes from make_tree cmd

    def test_is_learner_timing(self):
        random.seed(42)
        users = list(User.objects.all())
        coaches = random.sample(users, 100)
        learners = random.sample(users, 500)

        avg_time = 0
        count = 0
        for coach in coaches:
            for learner in learners:
                start = time.time()
                learner.is_learner_in_class_of(coach)
                end = time.time()
                count += 1
                avg_time = (avg_time*(count-1) + (end-start))/count

        print("Average time (ms): {}".format(avg_time))


class TestQueries(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestQueries, cls).setUpClass()
        classroom1 = Classroom.objects.create()
        user1, user2 = User.objects.create(), User.objects.create()
        lg = LearnerGroup.objects.create()

        coach = Coach.objects.create(user=user1)
        learner = Learner.objects.create(user=user2)

        classroom1.add_coach(coach)
        classroom1.add_learner_group(lg)
        lg.add_learner(learner)

        cls.user1 = user1
        cls.user2 = user2

    def test(self):
        with self.assertNumQueries(2):
            self.assertTrue(self.user2.is_learner_in_class_of(self.user1))

        with self.assertNumQueries(1):
            self.assertFalse(self.user1.is_learner_in_class_of(self.user2))
