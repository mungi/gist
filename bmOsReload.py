import SoftLayer
import argparse
from pprint import pprint

class OsReload():

    def __init__(self):
        parser = argparse.ArgumentParser(description='Baremetal Server OS Reload')
        parser.add_argument("ids", nargs='+', help="list of server id which will be reloaded")
        self.args = parser.parse_args()
        self.client = SoftLayer.Client()
        self.script_url = 'https://raw.githubusercontent.com/mungi/gist/master/pv-sample.ps1'

    def reload_bm(self, bm_id):

        config = {
            'customProvisionScriptUri': self.script_url,
            'upgradeBios': 1
        }

        output = self.client['Hardware_Server'].reloadOperatingSystem('FORCE', config, id=bm_id)
        pprint(output)

if __name__ == "__main__":
    bm = OsReload()

    for id in bm.args.ids:
        bm.reload_bm(id)
