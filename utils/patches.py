import uuid

import dash_leaflet as dl


def unique_map():
    """
    This patch injects an uuid as map id, if no id is provided. This ensures that all map instances are seen as
    "unique" from React. Without this "hack", an attempt will be made to update the existing map container instead
    of initializing a new one (which is what we want).
    :return:
    """

    class UniqueMap(dl.Map):
        def __init__(self, *args, **kwargs):
            if "id" not in kwargs:
                kwargs["id"] = str(uuid.uuid4())
            super(UniqueMap, self).__init__(*args, **kwargs)

    dl.Map = UniqueMap
