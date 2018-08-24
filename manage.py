#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    settings = "tests.app.settings" if "test" in sys.argv else "demo.app.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
