from scrapy import cmdline

name = 'to8to_qa'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
