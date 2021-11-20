import pandas as pd
from counselor.services import Spec
from ecocloud.settings import CSV_LOCATION, SPEC_POWER
from counselor.models import Region


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


# returns the carbon footprint of the provided specification in the provided region
# pass the current cpu usage in number of percentage. Default = 50
def get_spec_co(spec: Spec, region: Region, cpu_usage=50):
    power = get_spec_power_use(spec, cpu_usage)
    return power * region.pue * region.co_foot_print


# returns the power usage of the provided specification. The provider is part of the spec
# pass the current cpu usage in number of percentage. Default = 50
def get_spec_power_use(spec: Spec, cpu_usage=50):
    spec.stats = SPEC_POWER[spec.provider]
    cpu = (spec.stats["max_cpu"] - spec.stats["min_cpu"]) * \
          cpu_usage / 100 + spec.stats["min_cpu"]
    storage = spec.stats["storage"] * spec.storage / 1024
    memory = spec.stats["memory"] * spec.memory

    return cpu + storage + memory
