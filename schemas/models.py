import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.db import models
from faker import Faker

UserModel = get_user_model()


class Schema(models.Model):

    class ColumnSeparator(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        Comma = ',', 'Comma (,)'
        Dot = '.', 'Dot (.)'
        Hyphen = '-', 'Hyphen (-)'
        Colon = ':', 'Colon (:)'
        Semicolon = ';', 'Semicolon (;)'

    class StringCharacter(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        Quotes = "'", 'Quotes ('')'
        Double_quotes = '"', 'Double quotes ("")'
        Blank = ' ', 'Blank ( )'

    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_schem"
    )
    title = models.CharField(max_length=100)
    sep = models.CharField(
        max_length=20,
        choices=ColumnSeparator.choices,
        default=ColumnSeparator.Comma
    )
    str_char = models.CharField(
        max_length=20,
        choices=StringCharacter.choices,
        default=StringCharacter.Double_quotes
    )
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def generate_data_set(self, rows=5, url_id=None):
        """
        Method to generate dataset from schema
        Using csv module and Faker
        Create url links for csv files

        """

        faker = Faker()

        def fake_data(data_type: str, val_range=(0, 100)):
            # TODO: lower limit on sentences
            faker_methods = {
                'Full name': faker.name(),
                'Job': faker.job(),
                'Email': faker.safe_email(),
                'Domain_name': faker.domain_name(),
                'Phone number': faker.phone_number(),
                'Company name': faker.company(),
                'Text': faker.paragraph(
                    nb_sentences=val_range[1], variable_nb_sentences=False
                ),
                'Integer': faker.random_int(*val_range),
                'Address': faker.address(),
                'Date': faker.date(),
            }
            return faker_methods[data_type]

        import csv
        csv.register_dialect(
            "my",
            delimiter=str(self.sep),
            quotechar=str(self.str_char),
            quoting=csv.QUOTE_ALL,
        )

        columns = self.has_column.all().values()
        fieldnames = []
        for i in columns:
            fieldnames.append(i["column"])

        try:
            os.mkdir(settings.MEDIA_ROOT)
        except OSError:
            # print("folder creating error")
            pass

        with default_storage.open(str(settings.MEDIA_ROOT) + f"/{url_id}.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='my')
            writer.writeheader()
            for i in range(int(rows)):
                row = {}
                for col in columns:
                    column = col["column"]
                    if (
                            col["from_int"]
                            and col["to_int"]
                            and col["cl_type"] in ('Text', 'Integer')
                    ):
                        value = fake_data(
                            col["cl_type"],
                            val_range=(col["from_int"], col["to_int"]),
                        )
                    else:
                        value = fake_data(col["cl_type"])
                    row[column] = value
                writer.writerow(row)
        return f"{settings.MEDIA_URL}{url_id}.csv"


class Columns(models.Model):

    class TypeChoices(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        Full_Name = 'Full name', 'Full name'
        Job = 'Job', 'Job'
        Email = 'Email', 'Email'
        Domain_name = 'Domain name', 'Domain name'
        Phone_number = 'Phone number', 'Phone number'
        Company_name = 'Company name', 'Company name'
        Text = 'Text', 'Text'
        Integer = 'Integer', 'Integer'
        Address = 'Address', 'Address'
        Date = 'Date', 'Date'

    column = models.CharField(max_length=50)
    cl_type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.Integer
    )
    schem = models.ForeignKey(Schema, related_name="has_column", on_delete=models.CASCADE)
    cl_ord = models.PositiveIntegerField()
    from_int = models.PositiveIntegerField(null=True, blank=True)
    to_int = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        if not self.cl_ord:
            try:
                self.cl_ord = (
                        Columns.objects.filter(
                            target_schema=self.schem
                        ).count()
                        + 1
                )
            except ObjectDoesNotExist:
                pass

    class Meta:
        ordering = ("cl_ord",)


class DataSet(models.Model):

    class DataSetStatus(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        Ready = 'Ready', 'Ready'
        Processing = 'Processing', 'Processing'
        Error = 'Error', 'Error'

    status = models.CharField(
        max_length=20,
        choices=DataSetStatus.choices,
        default=DataSetStatus.Processing
    )
    rows = models.PositiveIntegerField(null=True, blank=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=True, null=True, related_name='has_dataset')
    load_lnk = models.URLField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    task_id = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-created']
