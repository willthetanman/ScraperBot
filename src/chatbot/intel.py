# -*- coding: utf-8 -*-

"""
Intel handler

"""

import httplib2, re, sys, argparse, urllib, urllib2
import dispatch

@dispatch.handler("ip")
def ip_handler(params, message=None, *args, **kwargs):


    if isinstance(params, basestring):
        # print "Is String" + params
        return "\n".join(grab_requests(params))
        # return grab_requests(params)

    else:
        print params
        ip_address = " ".join(params)
        print ip_address
        return "\n".join(grab_requests(ip_address))

def grab_requests(input):

    input = str(input)
    rpd7 = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.IGNORECASE)
    rpdFind7 = re.findall(rpd7,input)
    rpdSorted7=sorted(rpdFind7)
    rpdSorted7=str(rpdSorted7)
    rpdSorted7=rpdSorted7[2:-2]

    # rpd8 = re.compile('([-a-z0-9A-Z]+\.[-a-z0-9A-Z]*).+', re.IGNORECASE)
    # rpdFind8 = re.findall(rpd8,input)
    # rpdSorted8=sorted(rpdFind8)
    # rpdSorted8=str(rpdSorted8)
    # rpdSorted8=rpdSorted8[2:-2]

    rpd9 = re.compile('[a-fA-F0-9]{32}', re.IGNORECASE)
    rpdFind9 = re.findall(rpd9,input)
    rpdSorted9=sorted(rpdFind9)
    rpdSorted9=str(rpdSorted9)
    rpdSorted9=rpdSorted9[2:-2]

    if rpdSorted7 == input:
        print '--------------------------------'
        print '[*] ' + input + ' is an IP. '
        print '[*] Running IP toolset'
        ipInput = input
        return robtex(ipInput),ipvoid(ipInput),fortiURL(ipInput),alienvault(ipInput),virustotal(ipInput),threatexpert(ipInput)

    elif rpdSorted9 == input:
        print '--------------------------------'
        print '[*] ' + input + ' is an MD5 Hash. '
        print '[*] Running MD5 Hash Toolset'
        md5 = input
        return md5Hash(md5)

    else:
        print '--------------------------------'
        print '[*] ' + input + ' is a URL.  '
        print '[*] Running URL toolset'
        urlInput = input
        return urlvoid(urlInput), fortiURL(urlInput), threatexpert(urlInput)

def alienvault(ipInput):
    url = "http://labs.alienvault.com/labs/index.php/projects/open-source-ip-reputation-portal/information-about-ip/?ip=" + ipInput   
    proxy = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy)
    response = opener.open("http://labs.alienvault.com/labs/index.php/projects/open-source-ip-reputation-portal/information-about-ip/?ip=" + ipInput)
    content = response.read()
    contentString = str(content)
    
    rpd = re.compile('.*IP not found.*')
    rpdFind = re.findall(rpd,contentString)

    if not rpdFind:
        return ('[+] IP is listed in AlienVault IP reputation database at ' + url)
    else:
        return ('[-] IP is not listed in AlienVault IP reputation database')
   

def virustotal(ipInput):
	url = "http://www.virustotal.com/en/ip-address/" + ipInput + "/information/"
	proxy = urllib2.ProxyHandler()
	opener = urllib2.build_opener(proxy)
	response = opener.open("http://www.virustotal.com/en/ip-address/" + ipInput + "/information/")
	content = response.read()
	contentString = str(content)

	rpd = re.compile('Unknown IP!')
	rpdFind = re.findall(rpd,contentString)
	
	if not rpdFind:
		return ('[+] IP is listed in Virustotal IP reputation database at ' + url)
	else:
		return ('[-] IP is not listed in Virustotal IP reputation database')
   

def threatexpert(ipInput):
	url = "http://www.threatexpert.com/reports.aspx?find=" + ipInput
	proxy = urllib2.ProxyHandler()
	opener = urllib2.build_opener(proxy)
	response = opener.open("http://www.threatexpert.com/reports.aspx?find=" + ipInput)	
	content = response.read()
	contentString = str(content)
	# print content

	rpd = re.compile('no ThreatExpert reports found')
	rpdFind = re.findall(rpd,contentString)

	if not rpdFind:
		return ('[+] Report found for ' + ipInput +' listed in ThreatExpert database at ' + url)
	else:
		return('[-] No reports found in ThreatExpert database')

def robtex(ipInput):   
    proxy = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy)
    response = opener.open("http://robtex.com/" + ipInput)
    content = response.read()
    contentString = str(content)

    # rpd = re.compile('href\=\"\/\/.+\.robtex\.com\/(.+).html\"\s+\>.+\<\/a\>\s\<\/span\>\<\/td\>\n\<td\sclass\="\w+\"\scolspan\="\d*\"\>a', re.IGNORECASE)
    rpd = re.compile('host\.robtex\.com.+\s\>(.+)\<\/a\>', re.IGNORECASE)
    rpdFind = re.findall(rpd,contentString)
    
    rpdSorted=sorted(rpdFind)
    
    i=''
    for i in rpdSorted:
        if len(i)>4:
            if not i == ipInput:
                return '[+] A records from Robtex: ' + (i)
    if i=='':
        return '[-] This IP does not resolve to a domain'

def ipvoid(ipInput):                
    proxy = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy)
    response = opener.open("http://ipvoid.com/scan/" + ipInput)
    content = response.read()
    contentString = str(content)
    
    rpderr = re.compile('An\sError\soccurred', re.IGNORECASE)
    rpdFinderr = re.findall(rpderr,contentString)
    # print content2String
    if "ERROR" in str(rpdFinderr):
        ipvoidErr = True
    else:
        ipvoidErr = False
    if ipvoidErr == False:
        rpd2 = re.compile('Detected\<\/font\>\<\/td..td..a.rel..nofollow..href.\"(.{6,70})\"\stitle\=\"View', re.IGNORECASE)
        rpdFind2 = re.findall(rpd2,contentString)
        rpdSorted2=sorted(rpdFind2)
    
        rpd3 = re.compile('ISP\<\/td\>\<td\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind3 = re.findall(rpd3,contentString)
        rpdSorted3=sorted(rpdFind3)
    
        rpd4 = re.compile('Country\sCode.+flag\"\s\/\>\s(.+)\<\/td\>', re.IGNORECASE)
        rpdFind4 = re.findall(rpd4,contentString)
        rpdSorted4=sorted(rpdFind4)

        returnList = []
    
        j=''
        for j in rpdSorted2:
            returnList.append('[+] Host is listed in blacklist at '+ j)
        if j=='':
            returnList.append('[-] IP is not listed in a blacklist')
       
        k=''
        for k in rpdSorted3:
            returnList.append('[+] The ISP for this IP is: '+ k)
        if k=='':
            returnList.append('[-] No ISP listed')
        
        l=''
        for l in rpdSorted4:
            returnList.append('[+] Geographic Location: '+ l)
        if l=='':
            returnList.append('[-] No GEO location listed')

        return '\n'.join(returnList)

    else:
        print'[*] Scanning host now on IPVoid.com.  May take a few seconds.'

        url = ('http://www.ipvoid.com/')
        raw_params = {'ip':ipInput,'go':'Scan Now'}
        params = urllib.urlencode(raw_params)
        request = urllib2.Request(url,params,headers={'Content-type':'application/x-www-form-urlencoded'})
        page = urllib2.urlopen(request)
        page = page.read()
        contentString = str(page)
        
        rpd2 = re.compile('Detected\<\/font\>\<\/td..td..a.rel..nofollow..href.\"(.{6,70})\"\stitle\=\"View', re.IGNORECASE)
        rpdFind2 = re.findall(rpd2,contentString)
        rpdSorted2=sorted(rpdFind2)
    
        rpd3 = re.compile('ISP\<\/td\>\<td\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind3 = re.findall(rpd3,contentString)
        rpdSorted3=sorted(rpdFind3)
    
        rpd4 = re.compile('Country\sCode.+flag\"\s\/\>\s(.+)\<\/td\>', re.IGNORECASE)
        rpdFind4 = re.findall(rpd4,contentString)
        rpdSorted4=sorted(rpdFind4)

        returnList = []
    
        j=''
        for j in rpdSorted2:
            returnList.append('[+] Host is listed in blacklist at '+ j)
        if j=='':
            return('[-] IP is not listed in a blacklist')
       
        k=''
        for k in rpdSorted3:
            returnList.append('[+] The ISP for this IP is: '+ k)
        if k=='':
            return('[-] No ISP listed')
        
        l=''
        for l in rpdSorted4:
            returnList.append('[+] Geographic Location: '+ l)
        if l=='':
            returnList.append('[-] No GEO location listed')

        return '\n'.join(returnList)

def fortiURL(ipInput):
    proxy = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy)
    response = opener.open("http://www.fortiguard.com/ip_rep/index.php?data=" + ipInput + "&lookup=Lookup")
    content = response.read()
    contentString = str(content)
    
    rpd = re.compile('Category:\s(.+)\<\/h3\>\s\<a', re.IGNORECASE)
    rpdFind = re.findall(rpd,contentString)
    rpdSorted=sorted(rpdFind)
    
    #print content3String
    m=''
    for m in rpdSorted:
        return ('[+] FortiGuard URL Categorization: '+ m)
    if m =='':
        return ('[-] Unable to connect to FortiGuard.com')


def urlvoid(url):                
    proxy = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy)
    response = opener.open("http://urlvoid.com/scan/" + url)
    content = response.read()
    contentString = str(content)
    
    rpderr = re.compile('An\sError\soccurred', re.IGNORECASE)
    rpdFinderr = re.findall(rpderr,contentString)
    # print contentString
    if "ERROR" in str(rpdFinderr):
        ipvoidErr = True
    else:
        ipvoidErr = False
    if ipvoidErr == False:
        
        rpd1 = re.compile('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).+Scan\swith\s', re.IGNORECASE)
        rpdFind1 = re.findall(rpd1,contentString)
        rpdSorted1=sorted(rpdFind1) 
        
        rpd2 = re.compile('DETECTED.{25,40}href\=\"(.{10,50})\"\stitle', re.IGNORECASE)
        rpdFind2 = re.findall(rpd2,contentString)
        rpdSorted2=sorted(rpdFind2)   

        rpd3 = re.compile('latitude\s\/\slongitude.+\<td\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind3 = re.findall(rpd3,contentString)
        rpdSorted3=sorted(rpdFind3)
        
        rpd4 = re.compile('alt\=\"flag\".+\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind4 = re.findall(rpd4,contentString)
        rpdSorted4=sorted(rpdFind4)
        
        rpd5 = re.compile('Domain\s1st\sRegistered.+\<td\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind5 = re.findall(rpd5,contentString)
        rpdSorted5=sorted(rpdFind5)

        returnList = []
        
        i=''
        for i in rpdSorted1:
            returnList.append('[+] Host IP Address is '+ i)
        if i=='':
            returnList.append('[-] IP is not listed')
        
        j=''
        for j in rpdSorted2:
            returnList.append('[+] Host is listed in blacklist at '+ j)
        if j=='':
            returnList.append('[-] IP is not listed in a blacklist')
       
        k=''
        for k in rpdSorted3:
            returnList.append('[+] Latitude / Longitude: '+ k)
        if k=='':
            returnList.append('[-] No Latitude / Longitude listed')
        
        l=''
        for l in rpdSorted4:
            returnList.append('[+] Country: '+ l)
        if l=='':
            returnList.append('[-] No Country listed')
        
        m=''
        for m in rpdSorted5:
            returnList.append('[+] Domain creation date: '+ m)
        if m=='':
            returnList.append('[-] Domain creation date not listed.')

        return '\n'.join(returnList)

    else:
        print '[*] Scanning host now on URLVoid.com.  May take a few seconds.'
        urlvoid = ('http://www.urlvoid.com/')
        raw_params = {'url':url,'Check':'Submit'}
        params = urllib.urlencode(raw_params)
        request = urllib2.Request(urlvoid,params,headers={'Content-type':'application/x-www-form-urlencoded'})
        page = urllib2.urlopen(request)
        page = page.read()
        contentString = str(page)
        #print contentString
        rpd1 = re.compile('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).+Scan\swith\s', re.IGNORECASE)
        rpdFind1 = re.findall(rpd1,contentString)
        rpdSorted1=sorted(rpdFind1) 
        
        rpd2 = re.compile('DETECTED.{25,40}href\=\"(.{10,50})\"\stitle', re.IGNORECASE)
        rpdFind2 = re.findall(rpd2,contentString)
        rpdSorted2=sorted(rpdFind2)   

        rpd3 = re.compile('latitude\s\/\slongitude.+\<td\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind3 = re.findall(rpd3,contentString)
        rpdSorted3=sorted(rpdFind3)
        
        rpd4 = re.compile('alt\=\"flag\".+\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind4 = re.findall(rpd4,contentString)
        rpdSorted4=sorted(rpdFind4)
        
        rpd5 = re.compile('Domain\s1st\sRegistered.+\<td\>(.+)\<\/td\>', re.IGNORECASE)
        rpdFind5 = re.findall(rpd5,contentString)
        rpdSorted5=sorted(rpdFind5)

        returnList = []
        
        i=''
        for i in rpdSorted1:
            returnList.append('[+] Host IP Address is '+ i)
        if i=='':
            return('[-] IP is not listed')
        
        j=''
        for j in rpdSorted2:
            returnList.append('[+] Host is listed in blacklist at '+ j)
        if j=='':
            return('[-] IP is not listed in a blacklist')
       
        k=''
        for k in rpdSorted3:
            returnList.append('[+] Latitude / Longitude: '+ k)
        if k=='':
            return('[-] No Latitude / Longitude listed')
        
        l=''
        for l in rpdSorted4:
            returnList.append('[+] Country: '+ l)
        if l=='':
            returnList.append('[-] No Country listed')
        
        m=''
        for m in rpdSorted5:
            returnList.append('[+] Domain creation date: '+ m)
        if m=='':
            returnList.append('[-] Domain creation date not listed.')

        return '\n'.join(returnList)

def md5Hash(md5):
    # Set proxy based on system default
    proxy = urllib2.ProxyHandler()
    opener = urllib2.build_opener(proxy)
    
    # Connect to threatexpert and check if hash is listed 
    url = "http://www.threatexpert.com/report.aspx?md5=" + md5
    response = opener.open(url)
    content = response.read()
    contentString = str(content)
    rpd = re.compile('Submission\sreceived.\s(.+)\<\/li\>')
    rpdFind = re.findall(rpd,contentString)

    # Connect to minotaur and check if hash is listed 
    url1 = "http://minotauranalysis.com/search.aspx?q=" + md5 
    response1 = opener.open(url1)
    content1 = response1.read()
    contentString1 = str(content1)
    rpd1 = re.compile('Date\sSubmitted.\<\/td\>\<td\>(.{12,25})\<\/td\>')
    rpdFind1 = re.findall(rpd1,contentString1)

    # Connect to vxvault and check if hash is listed 
    url3 = "http://vxvault.siri-urz.net/ViriList.php?MD5=" + md5
    response3 = opener.open(url3)
    content3 = response3.read()
    contentString3 = str(content3)      
    rpd3 = re.compile('\d{4}\-\d{2}\-\d{2}')
    rpdFind3 = re.findall(rpd3,contentString3)

    returnList = []
    
    # print results of hash findings
    if rpdFind:
        returnList.append('[+] MD5 last scanned on ' + str(rpdFind)[2:-2] + ' at ' + url)
    else:
        returnList.append('[-] MD5 Not Found ThreatExpert')
 
    if rpdFind1:
        returnList.append('[+] MD5 last scanned on ' + str(rpdFind1)[2:-2] + ' at ' + url1)
    else:
        returnList.append('[-] MD5 Not Found on Minotaur')     
    
    if rpdFind3:
        returnList.append('[+] MD5 last scanned on ' + str(rpdFind3[0]) + ' at ' + url3)
    else:
        returnList.append('[-] MD5 Not Found on VxVault')          

    return returnList        

# print md5Hash('d429bf3d8ebeaa5fc09da6250201e5bc')
# print grab_requests('d429bf3d8ebeaa5fc09da6250201e5bc')