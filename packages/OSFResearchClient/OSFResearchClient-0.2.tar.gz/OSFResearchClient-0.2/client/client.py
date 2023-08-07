import requests
import csv
import io
import json

class Client:
    def __init__(self, base_url, uuid, secret):
        self.base_url = base_url
        self.uuid = uuid
        self.secret = secret
        self.headers = {}
        self.authorization()
        
    def authorization(self):
        r = requests.post(self.base_url + "/auth", json={"id": self.uuid, "secret": self.secret},
                          headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            self.headers = {"Content-Type": "application/json", "Authorization": r.text}
        else:
            raise ValueError("Make sure that the base_url, uuid, and secret are correctly specified")
        
    def addUser(self, email, role):
        r = requests.post(self.base_url + "/users", json={"email": email, "role": role}, headers=self.headers)
        if r.status_code == 401:
            self.authorization()
            return self.addUser(email, role)
        elif r.status_code == 403:
            raise Exception("You do not have access to this functionality")
        elif r.status_code != 200:
            raise Exception("Failed to add user. Here is the error: " + r.text)
        response = json.loads(r.text)
        return (response['id'], response['secret'])
                                         
    def deleteUser(self, uuid):
        r = requests.delete(self.base_url + "/users", json={"id": uuid}, headers=self.headers)
        if r.status_code == 401:
            self.authorization()
            return self.deleteUser(uuid)
        elif r.status_code == 403:
            raise Exception("You do not have access to this functionality")
        elif r.status_code != 200:
            raise Exception("Failed to delete user. Here is the error: " + r.text)
    def setSchema(self, schema):
        # Expects schema to be a dictionary, not a string
        r = requests.put(self.base_url + "/config/schema", headers=self.headers, json=schema)
        if r.status_code != 200:
            raise Exception(r.text)
    def setSchemaTable(self, database_name, schema):
        r = requests.put(self.base_url + f"/config/schema/{database_name}/table", json=schema,
                         headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
    def deleteSchemaTable(self, database_name, table_name):
        r = requests.delete(self.base_url + f"/config/schema/{database_name}/table/{table_name}",
                            headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
    def getPrivacyBudget(self):
        r = requests.get(self.base_url + "/config/privacy/budget", headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
        return r.text
    def setPrivacyBudget(self, budget):
        r = requests.put(self.base_url + "/config/privacy/budget", headers = self.headers,
                         json=budget)
        if r.status_code != 200:
            raise Exception(r.text)
    def query(self, database_name, query):
        r = requests.post('http://localhost:8180/query', json={'database_name': database_name,'query': query},
                          headers=self.headers)
        # Given that Client is already initialized, 401 happens if JWT credentials are expired
        if r.status_code == 401:
            self.authorization()
            return self.query(database_name, query)
        elif r.status_code != 200:
            raise Exception(r.text)
        else:
            return r.text
    # Helper methods to retrieve results
    def getHeader(self, result):
        c = csv.reader(io.StringIO(result), delimiter = '\t', quoting = csv.QUOTE_NONE)
        return next(c)
    def getResultFirstRow(self, result):
        c = csv.reader(io.StringIO(result), delimiter = '\t', quoting = csv.QUOTE_NONE)
        header = next(c)
        return next(c)
    def getResultFirstColumn(self, result):
        c = csv.reader(io.StringIO(result), delimiter = '\t', quoting = csv.QUOTE_NONE)
        header = next(c)
        results = list(c) #All values past header
        results = [r[0] for r in results] #Flatten array
        return results
    # Method to run a query and return either the first aggregate or an error
    def getResultOrError(self, database_name, query):
        try:
            priv_result = self.query(database_name, query)
            priv_agg = self.getResultFirstRow(priv_result)[0]
        except Exception as e:
            return str(e)
        return priv_agg
    def autogenerateSchema(self, database_name, table_name, join_keys=None):
        if join_keys:
            r = requests.post(self.base_url + f"/config/schema/{database_name}/table/{table_name}/generate",
                              headers=self.headers, json={"join_keys": join_keys})
        else:
            r = requests.post(self.base_url + f"/config/schema/{database_name}/table/{table_name}/generate",
                              headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
        else:
            return r.text
    def generatePreview(self, database_name, orig_table, preview_table_name, num_samples):
        r = requests.post(self.base_url + "/preview/generate", headers=self.headers,
            json={"database_name": database_name, "table_name": orig_table, "preview_table_name":
                preview_table_name, "num_samples": num_samples})
        if r.status_code != 200:
            raise Exception(r.text)
    def queryPreview(self, query):
        r = requests.post(self.base_url + "/preview/query", headers=self.headers, json={"query": query})
        if r.status_code == 200:
            return r.text
        else:
            raise Exception(r.text)
    def deletePreview(self, preview_table):
        r = requests.delete(self.base_url + "/preview", json={"preview_table": preview_table},
                            headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            raise Exception(r.text)