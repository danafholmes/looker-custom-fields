import json
import looker_sdk

def build_dim_list(items):
    all_fields = []
    for item in items:
        try:
            category = item['category']
        except KeyError:
            if 'table_calculation' in item.keys():
                category = 'table_calculation'
            if 'dimension' in item.keys():
                category = 'dimension'
            if 'measure' in item.keys():
                category = 'measure'
        expression = item['expression']
        label = item['label']
        try:
            based_on = item['based_on']
        except KeyError:
            based_on = None
        try:
            item_type = item['type']
        except KeyError:
            item_type = None
        try:
            filters = item ['filters']
        except KeyError:
            filters = None

        tile_fields = {'category': category,
             'expression': expression,
             'label': label,
             'based_on': based_on,
             'type': item_type,
             'filters': filters
            }
        all_fields.append(tile_fields)
    return all_fields

def get_custom_dashboard_dims(sdk, dashid):
    elements = sdk.dashboard_dashboard_elements(dashboard_id=str(dashid), fields="query, title")

    tiles = []

    for element in elements:
        title = element["title"]
        try:
            model = element["query"]["model"]
        except TypeError:
            model = None
        try:
            explore = element["query"]["view"]
        except TypeError:
            explore = None
        try:
            custom_fields = json.loads(element["query"]["dynamic_fields"])
        except TypeError:
            custom_fields = None
        fields_dict = {"tile_title": title,
          "model": model,
          "explore": explore,
          "custom_fields": custom_fields }
        tiles.append(fields_dict)

#     tiles = [{"tile_title": element["title"],
#       "model": element["query"]["model"],
#       "explore": element["query"]["view"],
#       "custom_fields": json.loads(element["query"]["dynamic_fields"])
#      } for element in elements if element["query"]["dynamic_fields"] != None ]

    for tile in tiles:
        if tile['custom_fields'] != None:
            tile['custom_fields'] = build_dim_list(tile['custom_fields'])
        else:
            continue

    return(tiles)

def get_custom_look_dims(sdk, lookid):
    elements = sdk.look(look_id=str(lookid), fields="query, title")

    try:
        title = elements["title"]
    except TypeError:
        title = None
    try:
        model = elements["query"]["model"]
    except TypeError:
        model = None
    try:
        explore = elements["query"]["view"]
    except TypeError:
        explore = None
    try:
        custom_fields = json.loads(elements["query"]["dynamic_fields"])
    except TypeError:
        custom_fields = None

    tiles = [{"tile_title": title,
      "model": model,
      "explore": explore,
      "custom_fields": custom_fields
     }]

    for tile in tiles:
        if tile['custom_fields'] != None:
            tile['custom_fields'] = build_dim_list(tile['custom_fields'])
        else:
            tile['custom_fields'] = None

    return(tiles)

def get_all_dash_custom(sdk):
    dashboards = sdk.all_dashboards(fields="id, model, folder, user_id, title")
    dashboards = [{key: value for key, value in dashboard.items()} for dashboard in dashboards]
    for dashboard in dashboards:
        dashboard['custom_fields'] = get_custom_dashboard_dims(sdk, dashboard['id'])
    return dashboards

def get_all_look_custom(sdk):
    looks = response = sdk.all_looks(fields="id, model, folder, user_id, title")
    looks = [{key: value for key, value in look.items()} for look in looks]
    for look in looks:
        look['custom_fields'] = get_custom_look_dims(sdk, look['id'])
    return looks
