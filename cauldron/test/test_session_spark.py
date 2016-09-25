import os
import sys

from cauldron.session import spark
from cauldron.test.support import scaffolds


class TestSessionReloading(scaffolds.ResultsTest):

    def setUp(self):
        super(TestSessionReloading, self).setUp()

    def test_init_no_spark(self):
        """

        :return:
        """

        with self.assertRaises(FileNotFoundError):
            spark.initialize(self.get_temp_path('not_spark'))

    def test_init_no_spark_python(self):
        """

        :return:
        """

        fake_spark = self.get_temp_path('fake_spark')

        with self.assertRaises(FileNotFoundError):
            spark.initialize(fake_spark)

    def test_init_no_spark_pylib(self):
        """

        :return:
        """

        fake_spark = self.get_temp_path('fake_spark')
        os.makedirs(os.path.join(fake_spark, 'python'))

        with self.assertRaises(FileNotFoundError):
            spark.initialize(fake_spark)

    def test_init_works(self):
        """

        :return:
        """

        fake_spark = self.get_temp_path('fake_spark')
        lib_path = os.path.join(fake_spark, 'python', 'lib')
        os.makedirs(lib_path)

        fake_lib_zip = os.path.join(lib_path, 'fake.zip')
        with open(fake_lib_zip, 'w+') as f:
            f.write('')

        spark.initialize(fake_spark)

        self.assertIn(fake_lib_zip, sys.path)

        spark.unload()

        self.assertNotIn(fake_lib_zip, sys.path)
