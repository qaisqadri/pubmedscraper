import scrapy


class PubmedspiderSpider(scrapy.Spider):
	name = 'pmspider'
	# allowed_domains = ['https://www.ncbi.nlm.nih.gov/m/pubmed/trending/']
	start_urls = ['https://www.ncbi.nlm.nih.gov/m/pubmed/trending/']

	def parse(self, response):
		self.log('visited pubmed')
		self.count=0

		
		link1 = response.xpath("//ul[@class='r']/li/a/@href").extract_first()

		print(link1)

		yield response.follow(link1, callback=self.parse_link)

	def parse_link(self, response):
		self.count+=1
		title = response.xpath('//h2[@class="title"]/text()').extract_first()

		authors=response.xpath('//div[@class="auths"]/a/text()').extract()
		sup=response.xpath('//div[@class="auths"]//sup/text()').extract()
		author_info=response.xpath('//div[@class="exi"]//dd/text()').extract()
		citation=response.xpath('//p[@class="j"]/text()').extract_first()
		# abstract=response.xpath('//div[@class="ab"]/p//text()').extract()
		abstract=response.xpath('//div[@class="ab"]/p/span/text()').extract()
		

		if abstract == []:
			abstract=response.xpath('//div[@class="ab"]/p//text()').extract()
			# print("\n\n\n\n\n\n in if \n\n\n\n\n\n\n")
		# print("\n\n abstract is : ",abstract,"\n\n")
		PMID=response.xpath('//div[@class="meta"]//span/text()').extract_first()

		yield{
			'title':title,
			'authors':authors,
			'sup':sup,
			'author_info':author_info,
			'citation':citation,
			'abstract':abstract,
			'PMID':PMID,
		}

		next=response.xpath('//a[@class="but nxt"]/@href').extract_first()
		if next:
			print("\n\n next page is : ",next,"\n\n")
			yield response.follow(next, callback=self.parse_link)

        

