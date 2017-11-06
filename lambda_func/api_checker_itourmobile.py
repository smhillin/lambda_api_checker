import requests
import os
import datetime
import platform

#os.environ['site']= 'https://www.itourmobile.com/API/'
SITE = os.environ['site']
#mock_event['time'] = datetime.datetime.now()


class Api_monitor:
    def __init__(self, base, endpoints, logfile):


        self.base_url = base
        self.endpoints = endpoints

    def log(self, msg):
        machine = platform.node()
        now = datetime.datetime.now()
        date = "{0}_{1}_{2} {3}:{4}:{5}".format(
            now.year, now.month, now.day,
            now.hour, now.minute, now.second)

        text = "{0}/{1}: {2}".format(machine, date, msg)
        print("{0}\n".format(text))

    def poller(self):
        stats = dict()
        failed_endpoints = {}
        for endpoint in self.endpoints:
            response = requests.get(self.base_url + endpoint)
            stats.update({endpoint: response.status_code})
            if (stats[endpoint] == 200):
                message = "{0} : {1} : ok".format(endpoint, response.status_code)
                print(message)
            if (stats[endpoint] != 200):
                message = "{0} : {1} : validation failed".format(endpoint, response.status_code)
                failed_endpoints.update({endpoint: response.status_code})
                print(message)
        if failed_endpoints:
            raise Exception('Failed Endpoints:', failed_endpoints)


def lambda_handler(event, context):
    print('Checking {} at {}...'.format(SITE, event['time']))
    endpoints = ["getActiveTours.php",
                 "getTour.php",
                 "getExplorePoints.php",
                 "getExploreCategories.php",
                 "register.php",
                 "login.php",
                 "getUserAccount.php",
                 "editUserAccount.php",
                 "getTourRatings.php",
                 "rateTour.php",
                 "recordAppPurchase.php",
                 "cancelAppPurchase.php",
                 "useFB.php",
                 "doesAccountExist.php",
                 "upgrade.php"]
    p = Api_monitor(SITE, endpoints, "log.txt")
    p.poller()
