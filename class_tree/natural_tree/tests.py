import math
import progressbar
import random
import time

from django.test import TestCase
from .models import *


class StressTestRelatedObject(TestCase):
    """
    The intent of this test is to monitor the run time of finding related objects.
    """
    fixtures = ["natural_tree_ro_dump.json"]

    def test_sanity(self):
        facility = Collection.objects.get(type="facility")
        self.assertEqual(facility.get_descendants().count() + Role.objects.count(), 3050)  # Magic number comes from make_tree cmd
        self.assertEqual(RelatedObject.objects.count(), 120598)

    def setUp(self):
        self.users = list(User.objects.all())

    def test_timing(self):
        count = 0
        times = []
        bar = progressbar.ProgressBar()
        for user in bar(self.users):
            start = time.time()
            list(RelatedObject.all_that_user_has_perms_for(user))  # Force evaluation
            end = time.time()
            count += 1
            times.append(end-start)

        avg_time = sum(times)/count
        print('*'*40)
        print("Average time (s) for `natural_tree` app's \n\t`RelatedObject.all_that_user_has_perms_for` "
              "method: {}".format(avg_time))
        std_dev = math.sqrt(sum([(t - avg_time)**2 for t in times])/count)
        print("Standard deviation is {}".format(std_dev))
        print('*'*40)

    def test_user_group_timing(self):
        count = 0
        times = []
        bar = progressbar.ProgressBar()
        for _ in bar(range(0, len(self.users))):
            user_group = random.sample(self.users, 100)

            start = time.time()
            list(RelatedObject.objects.filter(user__in=user_group))  # Force evaluation
            end = time.time()

            count += 1
            times.append(end-start)

        avg_time = sum(times)/count
        print('*'*40)
        print("Average time (s) for `natural_tree` app's \n\t`RelatedObject` "
              "filtering by User group: {}".format(avg_time))
        std_dev = math.sqrt(sum([(t - avg_time)**2 for t in times])/count)
        print("Standard deviation is {}".format(std_dev))
        print('*'*40)

    def test_single_timing(self):
        count = 0
        times = []
        bar = progressbar.ProgressBar()
        for user in bar(self.users):
            start = time.time()
            list(RelatedObject.objects.filter(user=user))  # Force evaluation
            end = time.time()

            count += 1
            times.append(end-start)

        avg_time = sum(times)/count
        print('*'*40)
        print("Average time (s) for `natural_tree` app's \n\t`RelatedObject` "
              "filtering by single User: {}".format(avg_time))
        std_dev = math.sqrt(sum([(t - avg_time)**2 for t in times])/count)
        print("Standard deviation is {}".format(std_dev))
        print('*'*40)


class TestRelatedObject(TestCase):

    def setUp(self):
        classroom = Collection.objects.create(type="classroom")
        coach_user, learner_user = self.coach_user, self.learner_user = User.objects.create(), User.objects.create()
        lg = Collection.objects.create(type="learner_group", parent=classroom)

        coach_role = Role.objects.create(user=coach_user, collection=classroom, type="coach")
        learner_role = Role.objects.create(user=learner_user, collection=lg, type="learner")

        self.related_object = RelatedObject.objects.create(user=learner_user)

    def test_coach_perms(self):
        self.assertEqual(self.related_object, RelatedObject.all_that_user_has_perms_for(self.coach_user).first())

    def test_learner_perms(self):
        self.assertFalse(RelatedObject.all_that_user_has_perms_for(self.learner_user))


class TestSanity(TestCase):
    """
    Just checks that the User.is_learner_in_class_of method works as expected.
    """
    def setUp(self):
        classroom = Collection.objects.create(type="classroom")
        lg = Collection.objects.create(type="learner_group", parent=classroom)
        coach_user, learner_user = self.coach, self.learner = User.objects.create(), User.objects.create()

        coach_role = Role.objects.create(user=coach_user, collection=classroom, type="coach")
        learner_role = Role.objects.create(user=learner_user, collection=lg, type="learner")

    def test_true(self):
        self.assertTrue(self.learner.is_learner_in_class_of(self.coach))

    def test_false(self):
        self.assertFalse(self.coach.is_learner_in_class_of(self.learner))


class TestBenchmark(TestCase):
    fixtures = ["treedump.json"]

    def test_sanity(self):
        facility = Collection.objects.get(type="facility")
        self.assertEqual(facility.get_descendants().count() + Role.objects.count(), 6100)  # Magic number comes from make_tree cmd


    def test_is_learner_timing(self):
        random.seed(42)
        users = list(User.objects.all())
        coaches = users
        tot_time = 0
        count = 0

        bar = progressbar.ProgressBar()
        for coach in bar(coaches):
            learners = random.sample(users, 50)
            for learner in learners:
                start = time.time()
                learner.is_learner_in_class_of(coach)
                end = time.time()
                count += 1
                tot_time += (end-start)

        avg_time = tot_time/count
        print("Average time (s) for `natural_tree` app's \n\t`User.is_learner_in_class_of` method: {}".format(avg_time))
