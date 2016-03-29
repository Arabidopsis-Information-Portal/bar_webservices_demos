import json
import requests
import re
import bar_common

# http://bar.utoronto.ca/webservices/efp_service/efp_service.php?request={"agi":"At1g04170","datasource":"Developmental_Map"}

def fail(message):
     # This is a simple failure message generator for generic ADAMA adapters
     # It will eventually be replaced with a system-wide fail function
     return 'text/plaintext; charset=ISO-8859-1', message

def search(arg):

# arg contains a dict with two key:values
#
# locus is gene identifier
# source is a string mapping to one of BAR eFP's data sources

	# In the future, ADAMA will check a query, map_*, or generic request against a list of mandatory
	# parameters specified for each service. For now, if we want to enforce that behavior we need to
	# implement it ourselves.
    if not (('locus' in arg) and ('source' in arg)):
        return fail('Both locus and source are required parameters')

	# Check that client has requested what looks like a valid transcript identifier
	# ADAMA will have a graceful, cross-language exception handling scheme in a future release
	# At present, we are hand-coding a fail(message) routine in the adapter. See above.
    locus = arg['locus']
    locus = locus.upper()

    p = re.compile('AT[1-5MC]G[0-9]{5,5}', re.IGNORECASE)
    if not p.search(locus):
        return fail('Please specify a valid AGI identifier for the locus parameter')

    # Check against a hard-coded list of acceptable data sources
    # ADAMA will have a graceful, cross-language exception handling scheme in a future release
    # At present, we are hand-coding a fail(message) routine in the adapter. See above.
    valid_sources = [
        'Abiotic_Stress',
        'Abiotic_Stress_II',
        'Biotic_Stress',
        'Biotic_Stress_II',
        'Chemical',
        'Development_RMA',
        'Developmental_Map',
        'Guard_Cell',
        'Hormone',
        'Lateral_Root_Initiation',
        'Light_Series',
        'Natural_Variation',
        'Regeneration',
        'Root',
        'Root_II',
        'Seed',
        'Tissue_Specific'
    ];
    source = arg['source']
    #source = source.lower()
    if not source in valid_sources:
        return fail( 'Supported values for the source parameter are ' + ', '.join(valid_sources) )

    request_param = '{"agi":"' + locus + '","datasource":"' + source + '"}'
    svc_url = bar_common.base_url() + '/efp_service/efp_service.php?request=' + request_param
    r = requests.get(svc_url)

    # Here's a new bit of error handling, unique to the generic type
    if r.ok:
		# If we get a 200 status from the remote GET, we inspect the returned Content-Type header and send
		# that back along with the content of the HTTP response. If we want to over-ride that
		# content type for some reason, we simply return a string with the appropriate MIME type
        return r.headers['Content-Type'],r.content
    else:
		# If there was an error of some kind, we try valiantly to grab any error text from the
		# remote service and return it to the client. Again, in the future ADAMA will have graceful error
		# reporting but we are waiting till we've seen a few error cases to implement it
        fail(r.text)

def list(arg):
	# We don't have a valid operation for the /list endpoint. At present, just return a nasty
	# looking stack trace from within ADAMA. At least the end client will know they did something bad
    pass
