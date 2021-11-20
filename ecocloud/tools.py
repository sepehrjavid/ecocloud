from counselor.models import *
import pandas as pd
from ecocloud.settings import CSV_LOCATION


def load_csv():
    file = pd.read_csv(CSV_LOCATION, header=0, delimiter=';', index_col=False)

    for row in file.iterrows():
        region_object = Region.objects.filter(name='-'.join([row[1][0], row[1][1]]))
        if not region_object.exists():
            Region.objects.create(name='-'.join([row[1][0], row[1][1]]), co_foot_print=row[1][3])


def get_region_rank(regions) -> list:
    pass
