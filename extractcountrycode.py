import json 
code_country_list = {}
file = open('Phonecountrycode.json','r')
countrycode = json.load(file) #Load the json file into the list of the code 
print(list(countrycode.get('countries'))[1].get('name'))
countrylist = list(countrycode.get('countries'))
for i in range(0,len(countrylist)):
           country_name_data = list(countrycode.get('countries'))[i].get('name')
           country_code_data = list(countrycode.get('countries'))[i].get('code')
           code_country_list[country_name_data] = country_code_data 
print(code_country_list)
writefile = open("Extracted_code_country.json",'w')
writejson = json.dump(code_country_list,writefile)
for r in range(0,len(list(code_country_list))):
                print(code_country_list.get(list(code_country_list)[r]))
