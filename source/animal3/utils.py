
from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner, reorder_suite
from django.utils.unittest import defaultTestLoader, TestCase


class LocalTestRunner(DjangoTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run all tests for all specified appplications.

        If no applications are specified, run tests for all applications
        found in the LOCAL_APPS setting.
        """
        if not test_labels:
            test_labels = settings.LOCAL_APPS
        return super(LocalTestRunner, self).run_tests(
            test_labels, extra_tests, **kwargs)
