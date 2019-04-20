#!/usr/bin/python -tt


import sys, re
import pycurl, StringIO
import logging
import atexit
sys.path.append("/usr/share/fence")
from fencing import *
from fencing import fail, EC_STATUS, run_delay

#BEGIN_VERSION_GENERATION
RELEASE_VERSION="4.0.11"
BUILD_DATE="(built Mon Jan 23 09:23:40 EST 2017)"
REDHAT_COPYRIGHT="Copyright (C) Red Hat, Inc. 2004-2010 All rights reserved."
#END_VERSION_GENERATION


def get_power_status(conn, options):
        del conn

        if options["--type"] == "BM":
                command = "getServerPowerState"
                RE_STATUS = re.compile("<root>(.*?)</root>", re.IGNORECASE)
        elif options["--type"] == "VSI":
                command = "getPowerState"
                RE_STATUS = re.compile("<keyName>(.*?)</keyName>", re.IGNORECASE)

        ### Obtain real ID from name
        res = send_command(options, command)

        result = RE_STATUS.search(res)
        if result == None:
                # We were able to parse ID so output is correct
                # in some cases it is possible that RHEV-M output does not
                # contain <status> line. We can assume machine is OFF then
                return "off"
        else:
                status = result.group(1)

        if status.lower() == "on":
                print "about to return 'on' ----- status: %s" % (status)
                return "on"
        elif status.lower() == "running":
                print "about to return 'on' ----- status: %s" % (status)
                return "on"
        else:
                print "about to return 'off' ----- status: %s" % (status)
                return "off"

def set_power_status(conn, options):
        del conn
        action = {
#                'on' : "powerOn",
                'off' : "powerOff"
        }[options["--action"]]
        send_command(options, action)

def send_command(opt, command, method="GET"):
        ## setup correct URL
        if opt.has_key("--ssl"):
                url = "https:"
        else:
                url = "http:"
        if opt.has_key("--api-path"):
                api_path = opt["--api-path"]
        else:
                api_path = "api.service.softlayer.com/rest/v3"
        if opt.has_key("--server-id"):
                id = opt["--server-id"]
        if opt.has_key("--type"):
                type = opt["--type"]

        url += "//" + api_path

        if opt["--type"] == "BM":
                url += "/SoftLayer_Hardware_Server/"
        elif opt["--type"] == "VSI":
                url += "/SoftLayer_Virtual_Guest/"

        url += opt["--server-id"] + "/" + command

        print "url:%s command:%s" % (url, command)

        ## send command through pycurl
        conn = pycurl.Curl()
        web_buffer = StringIO.StringIO()
        conn.setopt(pycurl.URL, url)
        conn.setopt(pycurl.HTTPHEADER, [
                "Version: 3",
                "Content-type: application/xml",
                "Accept: application/xml",
                "Prefer: persistent-auth",
                "Filter: true",
        ])

        if opt.has_key("cookie"):
                conn.setopt(pycurl.COOKIE, opt["cookie"])
        else:
                conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
                conn.setopt(pycurl.USERPWD, opt["--username"] + ":" + opt["--password"])
                if opt.has_key("--use-cookies"):
                        conn.setopt(pycurl.COOKIEFILE, "")

        if int(opt["--shell-timeout"]) < 10:
                conn.setopt(pycurl.TIMEOUT, 10)
        else:
                conn.setopt(pycurl.TIMEOUT, int(opt["--shell-timeout"]))

        if opt.has_key("--ssl") or opt.has_key("--ssl-secure"):
                conn.setopt(pycurl.SSL_VERIFYPEER, 1)
                conn.setopt(pycurl.SSL_VERIFYHOST, 2)

        if opt.has_key("--ssl-insecure"):
                conn.setopt(pycurl.SSL_VERIFYPEER, 0)
                conn.setopt(pycurl.SSL_VERIFYHOST, 0)

        if method == "POST":
                conn.setopt(pycurl.POSTFIELDS, "<action />")

        conn.setopt(pycurl.WRITEFUNCTION, web_buffer.write)

        result = "NONE"
        try:
                conn.perform()

                if not opt.has_key("cookie") and opt.has_key("--use-cookies"):
                        cookie = ""
                        for c in conn.getinfo(pycurl.INFO_COOKIELIST):
                                tokens = c.split("\t",7)
                                cookie = cookie + tokens[5] + "=" + tokens[6] + ";"

                        opt["cookie"] = cookie

                result = web_buffer.getvalue()
        except Exception as e:
                print "oops! exception occurred! what's going on? %s" % (e)
                pass

        logging.debug("%s\n", command)
        logging.debug("%s\n", result)

        print "return of send_command(): %s" % result.replace('\n', '')

        return result

def define_new_opts():
        all_opt["use_cookies"] = {
                "getopt" : "s",
                "longopt" : "use-cookies",
                "help" : "--use-cookies                  Reuse cookies for authentication",
                "required" : "0",
                "shortdesc" : "Reuse cookies for authentication",
                "order" : 1}
        all_opt["api_path"] = {
                "getopt" : ":",
                "longopt" : "api-path",
                "help" : "--api-path=[path]              The path of the API URL",
                "default" : "api.service.softlayer.com/rest/v3",
                "required" : "0",
                "shortdesc" : "The path of the API URL",
                "order" : 2}
        all_opt["type"] = {
                "getopt" : ":",
                "longopt" : "type",
                "help" : "--type=[type]                  The type of the Model",
                "required" : "0",
                "shortdesc" : "The type of the Model",
                "order" : 3}
        all_opt["server_id"] = {
                "getopt" : ":",
                "longopt" : "server-id",
                "help" : "--server-id=[serverid]         The Softlayer Server ID",
                "required" : "0",
                "shortdesc" : "The Sofrlayer Server ID",
                "order" : 4}

def main():
        device_opt = [
                "api_path",
                "login",
                "passwd",
                "ssl",
                "notls",
                "web",
                "type",
                "server_id",
                "use_cookies",
        ]

        atexit.register(atexit_handler)
        define_new_opts()

        all_opt["power_wait"]["default"] = "1"

        options = check_input(device_opt, process_input(device_opt))

        docs = {}
        docs["shortdesc"] = "Fence agent for Softlayer REST API"
        docs["longdesc"] = "fence_rhevm is an I/O Fencing agent which can be \
used with Softlayer REST API to fence BareMetals or Virtual Server Instances."
        docs["vendorurl"] = "http://www.cloudz.co.kr"
        show_docs(options, docs)

        ##
        ## Fence operations
        ####
        run_delay(options)
        result = fence_action(None, options, set_power_status, get_power_status)

        sys.exit(result)

if __name__ == "__main__":
        main()
