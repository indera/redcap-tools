from configurable_test_case import ConfigurableTestCase

class FormA1Test(ConfigurableTestCase):

    def test_form(self):
        # execute parent's logic with custom data
        self.run_test()
