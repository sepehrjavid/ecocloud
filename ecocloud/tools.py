from counselor.models import *
import pandas as pd
from ecocloud.settings import CSV_LOCATION


def load_csv():
    file = pd.read_csv(CSV_LOCATION, header=0, delimiter=';', index_col=False)

    for row in file.iterrows():
        region_object = Region.objects.filter(
            name='-'.join([row[1][0], row[1][1]]))
        if not region_object.exists():
            Region.objects.create(
                name='-'.join([row[1][0], row[1][1]]), co_foot_print=row[1][3])


# return the top 5 options that are better than the current one
def get_region_rank(regions, current_region) -> tuple:
    top_regions = []

    for region in regions:
        if (region.co_foot_print * region.pue) < (current_region.co_foot_print * current_region.pue):
            top_regions.append(region)

    top_regions.sort(key=lambda x: x.co_foot_print * x.pue)

    return top_regions[:5], len(top_regions) + 1
