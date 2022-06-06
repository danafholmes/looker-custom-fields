# looker-custom-fields
 Utilities for Auditing Custom Field Usage in Looker

### Description
 Some functions utilizing the Looker SDK to retrieve lists of custom dimensions used in saved Looks and Dashboards
 
### Possible use cases

- Make sure users aren't redefining fields incorrectly in Custom Dimensions/Measures
- Identify commonly used Custom Dimensions and Measures that could be moved to the LookML model
- Identify power users that create lots of custom dimensions/measures that would be good candidates for Developer training

### Using it


Initialize a Looker SDK object:

    import looker_sdk
	import json
	import custom_fields

	sdk = looker_sdk.init40()
Get a list of all the custom dimensions, measures, and table calculations for a given dashboard ID:

	custom_fields.get_custom_dashboard_dims(sdk, 48)

Returns a json object with the custom_fields for each Tile like:

	[{'tile_title': 'Number of First Purchasers',
	  'model': 'the_look_bq',
	  'explore': 'order_items',
	  'custom_fields': [{'category': 'table_calculation',
	  'expression': '10000',
      'label': 'Goal',
      'based_on': None,
      'type': None,
      'filters': None}]},

	...

For a Look ID, you'll get the same response format, but with just one item in the list:

	custom_fields.get_custom_look_dims(sdk, 857)

Get a list of all the Dashboards in the instance and their custom fields:

	custom_fields.get_all_dash_custom(sdk)

Get a list of all the Looks in the instance and their custom fields:

	custom_fields.get_all_look_custom(sdk)

If your instance is huge, use these last two at your own discretion - they'll hit the Looker API once for each Dashboard/Look in the Instance, so they may make *lots* of API calls and return *a lot* of data.

