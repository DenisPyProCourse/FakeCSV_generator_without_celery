from celery import shared_task

from PLANEKS_Challange.celery import app
from .models import Schema, DataSet


@shared_task(bind=True)
def create_csv(self, schem=None, rows=None):
    """
    Create a csv file
    :param self: to get the celery.task.id
    :param schem: get it from Ajax request
    :param rows: get it from Ajax request
    """
    schema = Schema.objects.get(pk=int(schem))
    csv_pk = self.request.id
    dataset = DataSet.objects.create(schema=schema, task_id=csv_pk, status='Processing', rows=rows)
    dataset.save()
    try:
        result = schema.generate_data_set(rows=rows, url_id=csv_pk)
        if result:
            dataset.load_lnk = result
            dataset.status = 'Ready'
            dataset.save()
        return True

    except:
        dataset.status = 'Error'
        dataset.save()
        raise
