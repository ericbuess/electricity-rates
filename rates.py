import os
import json

max_term_length = 6

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj,sort_keys=True,indent=4)
    print(text)
    
def sort_by_average_price(options):
	options_with_avg_price = []
	for option in options:
		plan = option['plan']
		rates = plan['rates']
		price_for_500_1000_2000 = rates[0]['price'] + rates[1]['price'] + rates[2]['price']
		avg_price = price_for_500_1000_2000 / 3
		#plan.update({'avg_price': avg_price})
		plan.pop('rates')
		options_with_avg_price.append({
			'avg_price': str(avg_price),
			'plan': plan
		})
		
	options_with_avg_price_sorted = sorted(options_with_avg_price, key=lambda k: k['avg_price'], reverse=True)
	return options_with_avg_price_sorted

#os.chdir("/Users/ericbuess/Git/electricity-rates")
#os.getcwd()
#directory = os.fsencode(os.getcwd())

file_name = "choose-texas-power.json"

with open(file_name, 'r') as file:
    file_data = file.read()
    data = json.loads(file_data)['data']
    utilities = data['utilities']
    options = []

    for utility in utilities:
        plans = utility['plans']
        for plan in plans:
        		term_length = plan['term']['length']
        		etf = -1
        		if not term_length:
        			term_length = -1
        		tiered = False
        		name = plan['name']
        		rates = plan['rates']
        		for rate in rates:
        			type = rate['type']
        			if type == 'Tier2' or type == 'Tier3':
        				price = rate['price']
        				if price > 0:
        					tiered = True
        					break
        		
        		if tiered == False and term_length <= max_term_length and 'free' not in name.lower() and 'hour' not in name.lower():
        			five_hundred_kwh = rates[0]['price']
        			one_thousand_kwh = rates[1]['price']
        			two_thousand_kwh = rates[2]['price']
        			if (five_hundred_kwh - one_thousand_kwh) < .01 and (one_thousand_kwh - two_thousand_kwh) < .01:
        			
        				name = plan['name']
        				id = plan['id']
        				efl = ''
        				documents = plan['documents']
        				for document in documents:
        					type = document['type']
        					if type == 'Efl':
        						efl = document['url']
        						break
        					
        				fees = plan['fees']
        				for fee in fees:
        					type = fee['type']
        					if type == 'EarlyTerminationFee':
        						etf = fee['amount']
        						
        				options.append({
        					'plan': {
        						#'id': id,
        						#'name': name,
        						'term': term_length,
        						'efl': efl,
        						'etf': etf,
        						#'id': id,
        						'rates': rates
        					}
        				})
            	
    sorted_plans = sort_by_average_price(options)
    jprint(sorted_plans)
    # for week in weeks:
    #         unit = week['unit']
    #         week_id = unit['id']
    #         week_ids.append(week_id)