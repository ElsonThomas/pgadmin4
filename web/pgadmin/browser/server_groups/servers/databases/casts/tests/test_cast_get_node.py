from __future__ import print_function
from pgadmin.browser.server_groups.servers.databases.tests import \
    utils as database_utils
from pgadmin.utils.route import BaseTestGenerator
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as cast_utils

import sys

if sys.version_info < (3, 3):
    from mock import patch
else:
    from unittest.mock import patch


class CastsGetNodeTestCase(BaseTestGenerator):
    """ This class will fetch the cast node added under database node. """
    skip_on_database = ['gpdb']
    url = '/browser/cast/nodes/'
    scenarios = cast_utils.generate_scenarios("cast_get_node")

    def setUp(self):
        """ This function will create cast."""
        super(CastsGetNodeTestCase, self).setUp()
        self.inv_data = self.inventory_data
        self.default_db = self.server["db"]
        self.database_info = parent_node_dict['database'][-1]
        self.db_name = self.database_info['db_name']
        self.server["db"] = self.db_name
        self.cast_id = cast_utils.create_cast(self.server,
                                              self.inv_data["srctyp"],
                                              self.inv_data["trgtyp"])

    def runTest(self):
        """ This function will fetch added cast."""
        self.server_id = self.database_info["server_id"]
        self.db_id = self.database_info['db_id']
        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        if self.is_positive_test:
            if self.is_list:
                response = cast_utils.api_get_cast_node(self, "")
                cast_utils.assert_status_code(self, response)
            else:
                response = cast_utils.api_get_cast_node(self, self.cast_id)
                cast_utils.assert_status_code(self, response)
        else:
            if self.mocking_required:
                return_value_object = eval(self.mock_data["return_value"])
                with patch(self.mock_data["function_name"],
                           side_effect=[return_value_object]):
                    if self.is_list:
                        response = cast_utils.api_get_cast_node(self, "")
                        cast_utils.assert_status_code(self, response)
                        # act_res = response.status_code
                        # exp_res = self.expected_data["status_code"]
                        # self.assertEquals(act_res, exp_res)

                        cast_utils.assert_error_message(self, response)

                        # act_res = response.json["errormsg"]
                        # exp_res = self.expected_data["error_msg"]
                        # self.assertEquals(act_res, exp_res)

                    else:
                        response = cast_utils.api_get_cast_node(self,
                                                                self.cast_id)
                        cast_utils.assert_status_code(self, response)
                        # act_res = response.status_code
                        # exp_res = self.expected_data["status_code"]
                        # self.assertEquals(act_res, exp_res)
            else:
                self.cast_id = 12893
                response = cast_utils.api_get_cast(self, self.cast_id)
                cast_utils.assert_status_code(self, response)

    def tearDown(self):
        """This function disconnect the test database and drop added cast."""
        connection = utils.get_db_connection(self.server['db'],
                                             self.server['username'],
                                             self.server['db_password'],
                                             self.server['host'],
                                             self.server['port'],
                                             self.server['sslmode'])
        cast_utils.drop_cast(connection, self.inv_data["srctyp"],
                             self.inv_data["trgtyp"])
        database_utils.disconnect_database(self, self.server_id,
                                           self.db_id)
        self.server['db'] = self.default_db
