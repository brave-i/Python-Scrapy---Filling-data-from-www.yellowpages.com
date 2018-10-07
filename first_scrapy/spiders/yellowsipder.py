# -*- coding: utf-8 -*-
import scrapy
from lxml import html
import requests
import csv

class YellowsipderSpider(scrapy.Spider):

	def main():
		baseurl = 'https://www.yellowpages.com'
		#url = baseurl + '/search?search_terms=Injury+Law+Attorneys&geo_location_terms=CA'	
		url = baseurl + '/search?search_terms=Injury%20Law%20Attorneys&geo_location_terms=california&page=87'

		fieldnames=['Name' , 'Address', 'City','State','PostalCode','Phone','WebSites','Email']
		csvfile = open('result.csv', 'w')
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()



		for sIndex in range(0,100):
			# one page
			searchpage = requests.get(url)
			tree = html.fromstring(searchpage.content)  

			Names =  tree.xpath('//span[@itemprop="name"]/text()')
			print 'Names:----------------------------------------------------------------', Names
			if len(Names) > 1: 
				del Names[0]
				#print "Names:", len(Names), Names

				linkurls = tree.xpath('//span[@itemprop="name"]/../@href')
				del linkurls[0]
				#print 'linkurls', linkurls

				#for index in range(0,2):
				for index in range(0,len(linkurls)):
				 	linkurls[index] = baseurl + linkurls[index]
				 	print 'fullurl', linkurls[index]

				 	subpage = html.fromstring(requests.get(linkurls[index]).content)
					addr_set = 	subpage.xpath('//p[@class="address"]/span/text()')
					print 'address', addr_set

					if len(addr_set) == 4:
						addres = addr_set[0].replace(",","")
						cities = addr_set[1].replace(",","")
						states = addr_set[2]
						pcodes = addr_set[3]

					elif len(addr_set) == 3:
						addres = addr_set[0].replace(",","")
						cities = ""
						states = addr_set[1]
						pcodes = addr_set[2]
					else:
						addres = ""
						cities = ""
						states = ""
						pcodes = ""

					phones	= subpage.xpath('//p[@class="phone"]/text()') 

					if len(phones) > 0:
						phone=phones[0];
					else:
						phone=""
					#print 'phones', phones

					webSites = subpage.xpath('//a[@class="secondary-btn website-link"]/@href')

					if len(webSites) > 0:
						webSite=webSites[0];
					else:
						webSite=""
					#print 'webSites', webSites

					emails = subpage.xpath('//a[@class="email-business"]/@href')

					if len(emails) > 0:
						email=emails[0].replace("mailto:","");
					else:
						email=""
					#print 'emails', emails

					json_one = {"Name":Names[index], "Address":addres, "City":cities, "State":states, "PostalCode":pcodes, "Phone":phone, "WebSites":webSite, "Email":email}
					writer.writerow(json_one)



			nexturls = tree.xpath('//a[@class="next ajax-page"]/@href')
			print 'Next url->',nexturls

			url = baseurl + nexturls[0];

			print "sIndex=", sIndex


		csvfile.close()	



		

		
		#print 'addresses', adress_items
		 	#for item in adress_items:
		 	#	item.xpath('')
		 	#cities	= subpage.xpath('//span[@itemprop="streetAddress"]/text()')
		 	#states		
		#phones	= subpage.xpath('//p[@class="phone"]/text()') 
		#webSites = subpage.xpath('//a[@class="secondary-btn website-link"]/@href')
		#emails = subpage.xpath('//a[@class="email-business"]/@href')
			
		


		# Address =  tree.xpath('//span[@itemprop="streetAddress"]/text()')
		# print 'Address:', Address
		# print 'Address:', len(Address)

		# #Cities = tree.xpath('//span[@itemprop="addressLocality"]/text()')
		# Cities = tree.xpath('//span[@itemprop="streetAddress"]/following-sibling::span[1]/text()')
		# print 'Cities:', Cities
		# print 'Cities:', len(Cities)

		# #States = tree.xpath('//span[@itemprop="addressRegion"]/text()')
		# States = tree.xpath('//span[@itemprop="streetAddress"]/following-sibling::span[2]/text()')
		# print 'States:', States
		# print 'States:', len(States)

		# #Phones = tree.xpath('//div[@itemprop="telephone"]/text()')
		# Phones = tree.xpath('//span[@itemprop="streetAddress"]/../following-sibling::div[1]/text()')
		# print 'Phones:', Phones
		# print 'Phones:', len(Phones)
		
		# WebSites = tree.xpath('//a[@class="track-visit-website"]/@href')
		# #Emails = tree.xpath('//span[@itemprop="addressRegion"]/text()')
		# Emails = []


		# linkurls = tree.xpath('//span[@itemprop="name"]/../@href')
		# del linkurls[0]

		# print 'name counts: ', len(linkurls)

		# for index in range(0,len(linkurls)):
		# 	linkurls[index] = baseurl + linkurls[index]
		# 	#print 'names:',index, linkurls[index]

		# 	subpage = html.fromstring(requests.get(linkurls[index]).content);
		# 	emails = subpage.xpath('//a[@class="email-business"]/@href')

		# 	if len(Emails) > 0:	
		# 		Emails.append(emails[0]).replace("mailto:", "")
		# 	else:
		# 		Emails.append("")

			#if len(Emails) > 0:
			#	print "Email",Emails[0].replace("mailto:", "")

			#Emails[0]: just index.(1~4)
		
		


		#nexturls = tree.xpath('//a[@class="next ajax-page"]/@href')
		#url = baseurl + nexturls[0];

  
	if __name__== "__main__":
  		main()


