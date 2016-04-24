import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safecollab.settings')

import django
django.setup()

from safecollabapp.models import Report, DataFile

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db import models
from django.core.files.storage import FileSystemStorage


def populate():

    report1 = add_report("report_1", "owner_1")

    add_datafile(report=report1,
                name="file1",
                owner="owner_2",
                encrypted=False)

    add_datafile(report=report1,
                name="fresh_lyrics",
                owner="yo_gotti",
                encrypted=True)

    report2 = add_report("report_2", "owner_2")

    add_datafile(report=report2,
                name="file2",
                owner="owner_2",
                encrypted=False)

    add_datafile(report=report2,
                name="file3",
                owner="owner_2",
                encrypted=False)

    # Print out what we have added to the user.
    for r in Report.objects.all():
        print("  {0}:".format(str(r)))
        for f in DataFile.objects.filter(report=r):
            print("     - {0}".format(str(f)))


def add_report(name, owner):
    r = Report.objects.get_or_create(name=name, owner=owner)[0]
    r.save()
    return r

def add_datafile(report, name, owner, encrypted):
    f = DataFile.objects.get_or_create(report=report, name=name, owner=owner, encrypted=encrypted)[0]
    f.save()
    return f

# Start execution here!
if __name__ == '__main__':
    print("Starting storage population script...")
    populate()