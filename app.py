import requests
import os
import datetime
import platform





class Api_monitor:

    def __init__(self, base, endpoints, logfile):

        dir = os.path.dirname(__file__)
        data_folder = os.path.join(dir, 'logs')

        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        self.log_dir = os.path.join(data_folder, logfile)

        self.base_url= base
        self.endpoints= endpoints


    def log(self, msg):
        machine = platform.node()
        now = datetime.datetime.now()
        date = "{0}_{1}_{2} {3}:{4}:{5}".format(
            now.year, now.month, now.day,
            now.hour, now.minute, now.second)

        text = "{0}/{1}: {2}".format(machine, date, msg)
        # Print to console
        print("    log=" + text)

        # Add to log file
        with open(self.log_dir, 'a+') as fout:
            fout.write("{0}\n".format(text))



    def poller(self):
        stats = dict()
        for endpoint in self.endpoints:
            response = requests.get(self.base_url+ endpoint)
            stats.update({endpoint: response.status_code})
            if (stats[endpoint] == 200):
                message ="{0} : {1} : ok".format(endpoint, response.status_code)
                self.log(message)
            if (stats[endpoint] != 200):
                #TODO AWS Topic
                message = "{0} : {1} : failed".format(endpoint, response.status_code)
                self.log(message)



if __name__ == "__main__":
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
                    "404endpoint.php",
                    "upgrade.php"]
    p = Api_monitor('https://www.itourmobile.com/API/',endpoints, "log.txt")
    p.poller()