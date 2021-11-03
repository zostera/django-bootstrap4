from django.test import TestCase


class VersionTest(TestCase):
    """Test presence of package version."""

    def test_version(self):
        import bootstrap4

        version = bootstrap4.__version__
        version_parts = version.split(".")
        self.assertEqual(len(version_parts), 2)
