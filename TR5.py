#!/usr/bin/env python
#-*- coding: utf-8 -*-
#################################################################################
#NAME: TR5	// TWITTER AUTOREPORTER 5.0					#
#OP: #opIceISIS // #opFocalpoint						#
#										#
#USAGE:	$ cd YOUR_DOWNLOAD_FOLDER						#
# 	$ python TR5.py -u TWITTER_USERNAME -i TWITTER_URL_ONLY_TARGETSLIST.txt	#
#################################################################################

from splinter import Browser
import sys, getopt, re
from datetime import datetime
from splinter.request_handler.status_code import HttpResponseError
import time
import traceback

def main(argv):
    
    d = datetime.now()
    date = str(d.year) + '' + str(d.month) + '' + str(d.day) + '' + str(d.hour) + '' + str(d.minute) + '' + str(d.second)
    try:
        opts, args = getopt.getopt(argv,"hi:u:",["file=","user="])
    except getopt.GetoptError:
        print 'twitterReport.py -u <Twitter username> -i <file>'
        print 'Le fichier des profiles doit comporter une URL par ligne ++'
#        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'twitterReport.py -u <Twitter username> -i <file.txt>'
            print 'Le fichier des profiles doit comporter une URL par ligne'
            sys.exit()
        elif opt in ("-i", "--file"):
            txt = arg
        elif opt in ("-u", "--user"):
            username = arg

    password = raw_input("Enter your twitter password : ")

    try:
        username
        txt
    except getopt.GetoptError:
        print 'twitterReport.py -u <Twitter username> -i <file>'
        print 'Le fichier des profiles doit comporter une URL par ligne'
#        sys.exit()
# uncomment if you want to use privoxy + tor        
#    proxyIP = '127.0.0.1'
#    proxyPort = 8118
#
#    proxy_settings = {'network.proxy.type': 1,
#            'network.proxy.http': proxyIP,
#            'network.proxy.http_port': proxyPort,
#            'network.proxy.ssl': proxyIP,
#            'network.proxy.ssl_port':proxyPort,
#            'network.proxy.socks': proxyIP,
#            'network.proxy.socks_port':proxyPort,
#            'network.proxy.ftp': proxyIP,
#            'network.proxy.ftp_port':proxyPort 
#            }
#
#    with Browser('firefox',profile_preferences=proxy_settings) as browser:
#    with Browser() as browser:
    with Browser() as browser:

        browser.visit("https://twitter.com/")
        browser.execute_script('document.getElementById("signin-email").value = "'+username+'"')
        browser.execute_script('document.getElementById("signin-password").value = "'+password+'"')
        browser.find_by_css('button[type="submit"].submit.btn.primary-btn').click()
        try:
            file = open(txt, 'r')
        except:
            print "Impossible d'ouvrir le fichier"

        for line in file:
            try:
                url = re.match(r"https?://(www\.)?twitter\.com/intent/(#!/)?@?([^/\s]*)",line.strip())
                url = url.group()
                browser.visit(url)
                if not browser.is_element_present_by_css('.route-account_suspended'):
		    browser.find_by_css('a.fn.url.alternate-context').click()
                    browser.find_by_css('.user-dropdown').click()
                    browser.find_by_css('li.report-text button[type="button"]').click()
		    time.sleep(2)
#		    browser.choose('input[type="radio"][value="spam"]').click(1)
#		    browser.find_by_css('.input[type="radio"][value="spam"]')[1].click()
#		    browser.find_element_by_xpath(".//label")[1].click()
#		    browser.find_elements_by_css_selector('.input[type="radio"][value="spam"]')[1].click()
#		    browser.find_by_css('label.spam [type="radio"]').click()
#		    browser.choose("spam")[1].click()
#		    browser.find_elements_by_xpath(".//input[@type='radio' and @value='spam']")[0].click()
		    browser.find_by_css('button.btn.primary-btn.new-report-flow-next-button[type="button"]')[0].click()
		    time.sleep(2)
		    browser.find_by_css('button.btn.primary-btn.new-report-flow-done-button[type="button"]')[0].click()
#                   browser.find_by_css('button.btn.primary-btn:nth-child(1)').click()
                    followers = browser.find_by_css('a[data-nav="followers"] .ProfileNav-value').value;
                    msg = url.strip()
                    with open("log_reported_"+date+".txt", "a") as log:
                        log.write(msg+"\n")
                elif browser.is_element_present_by_css('.route-account_suspended'):
                    msg =  line.strip()+' - Suspended'
                    with open("log_suspended.txt", "a") as log:
                        log.write(msg+"\n")
                else:
                    msg = line.strip()+' - Unknown'
                    with open("log_unknown.txt", "a") as log:
                        log.write(msg+"\n")

                print msg

            except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence !'
                break
            except HttpResponseError:
                msg = line.strip()+' - HttpResponseError'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
		pass
            except:
                if line:
                    msg = url.strip()+' - CatchAllError'
                    var = traceback.format_exc()
                    print str(sys.exc_info()[0])
                    print msg
                    #with open("log_Error.txt", "a") as log:
                    #    log.write(msg+"\n")
                    with open("log_Error.txt", "a") as log: log.write(msg+"\n"+var)    
                else:
                    pass

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence !')
