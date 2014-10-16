import json
import requests
import re
import bar_common

def search(arg):

    # We search only on locus identifiers
    locus = arg['locus']
    locus = locus.upper()
    
    # Format the query into BAR's idiomatic scheme
    request_param = '[{%22gene%22:%22' + locus + '%22}]'
    svc_url = bar_common.base_url() + '/get_expressologs.php?request=' + request_param
    r = requests.get(svc_url)
    # Iterate over expressolog records and transform them to locus_relationship
    # Each record will return 
    p = re.compile('dataSource=([\d\w]+)')
    for record in r.json()[locus]:
		
		# Extract the source data set out of the eFPWeb URI
        efp_link = record['efp_link']
        source = p.search(efp_link)        
        if source: 
            source = source.group(1)
        else:
            source = 'unknown'
        
        transformed_cc = {
    	    'class': 'locus_relationship',
    	    'reference': 'TAIR10',
            'locus': locus,
            'related_entity': record['gene_B'],
            'relationships': [ {'type': 'coexpression', 'direction': 'undirected',
                                'scores': [ 
                                    {'correlation_coefficient' : record['correlation_coefficient'] }
                                ]},
                                {'type': 'sequence_similarity', 'direction': 'undirected', 'scores': [
                                    {'percentage': record['seq_similarity']}] }],
            'other_data': {'dataSource': source, 'efp_link': efp_link, 'probeset_A': record['probeset_A'], 'probeset_B': record['probeset_B'] }
        }
            
        print json.dumps(transformed_cc)
        print '---'

def list(arg):
    # We don't support a list context for this service
    pass
