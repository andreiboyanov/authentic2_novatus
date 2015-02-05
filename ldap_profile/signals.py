from authentic2.attribute_aggregator.signals import \
    listed_attributes_with_source_call, any_attributes_call,\
    listed_attributes_call

import models


def init_signals():
    any_attributes_call.connect(models.get_attribute_aggregator_attributes)
    listed_attributes_call.connect(models.get_attribute_aggregator_attributes)
    listed_attributes_with_source_call.\
        connect(models.get_attribute_aggregator_attributes)
