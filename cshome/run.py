from scrapy import cmdline

name = 'to8to'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
