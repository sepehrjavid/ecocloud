import pandas as pd
from counselor.services import Spec
from ecocloud.settings import CSV_LOCATION, SPEC_POWER
from counselor.models import Region, ServiceRegionRelation

# load the data about the environmental impact of each region


def load_csv():
    file = pd.read_csv(CSV_LOCATION, header=0, delimiter=';', index_col=False)

    for row in file.iterrows():
        region_object = Region.objects.filter(
            name='-'.join([row[1][1], row[1][2]]))
        if not region_object.exists():
            Region.objects.create(name='-'.join([row[1][1], row[1][2]]),
                                  co_foot_print=float(row[1][5]),
                                  country=row[1][3],
                                  continent=row[1][4], pue=row[1][6])


# return the top 5 options that are better than the current one
def get_region_rank(regions, current_region: Region, service_plan: ServiceRegionRelation) -> tuple:
    top_regions = []

    for region in regions:
        if (region.co_foot_print * region.pue) < (current_region.co_foot_print * current_region.pue):
            top_regions.append(region)

    top_regions.sort(key=lambda x: x.co_foot_print * x.pue, reverse=True)
    return top_regions[:5], len(top_regions) + 1


# returns the monthly carbon footprint of the provided specification in the provided region
# returns the value in kilos
# pass the current cpu usage in number of percentage. Default = 50
def get_spec_co(spec: Spec, region: Region, cpu_usage=50):
    hourly_power_use = get_spec_power_use(spec, cpu_usage)
    # pue * co_foot_print gives us the effective amount of carbon needed for
    #   1kWh of electricity used by a resource
    # convert hourly power into monthly power use
    return 1000 * (hourly_power_use * 24 * 30.5) * (region.pue * region.co_foot_print)


# returns the power usage of the provided specification in kWh
# Provider is part of the spec
# Pass the current cpu usage in number of percentage. Default = 50
def get_spec_power_use(spec: Spec, cpu_usage=50):
    spec.stats = SPEC_POWER[spec.provider]
    # get the mean CPU cost for usage%
    cpu = (spec.stats["max_cpu"] - spec.stats["min_cpu"]) * \
        cpu_usage / 100 + spec.stats["min_cpu"]
    # per TB power consumption for storage
    storage = spec.stats["storage"] * spec.storage / 1024
    # per GB power consumption for memory
    memory = spec.stats["memory"] * spec.memory / 1000

    return cpu + storage + memory
