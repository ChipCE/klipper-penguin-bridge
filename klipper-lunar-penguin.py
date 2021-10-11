import time
import schedule
import json
import requests
import configparser
import subprocess

VERSION = "0.1b-20211012"
CONFIG_FILE = "./config.json"


class SystemConfig(object):

    def __init__(self, configFile):
        self.configOk = True
        configJson = {}
        with open(configFile) as config_file:
            configJson = json.loads(config_file.read())
        # check params
        if "variablesFile" not in configJson or "moonrakerPort" not in configJson or "updateInterval" not in configJson or "taskList" not in configJson or "apiTimeout" not in configJson:
            raise ValueError("Missing parameter(s)")
        if type(configJson["variablesFile"]) != str or configJson["variablesFile"] == "":
            raise ValueError("Invalid moonrakerPort")
        if type(configJson["moonrakerPort"]) != int or configJson["moonrakerPort"] <= 0:
            raise ValueError("Invalid moonrakerPort")
        if type(configJson["apiTimeout"]) != int or configJson["apiTimeout"] <= 0:
            raise ValueError("Invalid apiTimeout")
        if type(configJson["updateInterval"]) != int or configJson["updateInterval"] <= 0:
            raise ValueError("Invalid updateInterval")
        if type(configJson["taskList"]) != list or len(configJson["taskList"]) <= 0:
            raise ValueError("Invalid taskList")

        self.variablesFile = configJson["variablesFile"]
        self.moonrakerPort = configJson["moonrakerPort"]
        self.apiTimeout = configJson["apiTimeout"]
        self.updateInterval = configJson["updateInterval"]
        self.taskList = []

        for rawTask in configJson["taskList"]:
            tmpTask = Task(rawTask)
            self.taskList.append(tmpTask)


class Task(object):
    def __init__(self, rawObj):
        if "command" not in rawObj or "execTimeout" not in rawObj or "variableName" not in rawObj:
            raise ValueError("Missing parameter(s)")
        if type(rawObj["command"]) != str or rawObj["command"] == "":
            raise ValueError("Invalid command")
        if type(rawObj["variableName"]) != str or rawObj["variableName"] == "":
            raise ValueError("Invalid variableName")
        if type(rawObj["execTimeout"]) != int or rawObj["execTimeout"] <= 0:
            raise ValueError("Invalid execTimeout")

        self.command = rawObj["command"]
        self.execTimeout = rawObj["execTimeout"]
        self.variableName = rawObj["variableName"]


class TaskRunner(object):
    def __init__(self, config):
        self.config = config

    def _readVarList(self):
        try:
            self.varList = configparser.ConfigParser()
            self.varList.sections()
            self.varList.read(self.config.variablesFile)
            return True
        except Exception as e:
            print("Exception:", e)
            return False

    def _getVarValue(self, varName):
        try:
            return self.varList["Variables"][varName].replace("'", "")
        except Exception:
            return ""

    def _getExecResult(self, command, cwd=None, timeout=1):
        print("#EXEC :", command)
        proc = subprocess.Popen(
            [command], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = ""
        stderr = ""
        try:
            (stdout, stderr) = proc.communicate(timeout=timeout)
        except Exception as e:
            print("Exception", e)
            print("Error", stderr)
            return "none"

        resultStr = stdout.decode('utf-8').replace("\n", "")
        if resultStr == "":
            return "none"

        return resultStr

    def _updateVarValue(self, varName, varValue, apiTimeout):
        postData = {"commands": [
            "SAVE_VARIABLE VARIABLE=" + varName + " VALUE=\'\"" + varValue + "\"\'"]}
        url = "http://localhost:" + \
            str(self.config.moonrakerPort) + "/api/printer/command"

        try:
            rawResult = requests.post(url, data=str(json.dumps(postData)), headers={
                                      'Content-type': 'application/json', 'Accept': 'application/json'}, timeout=apiTimeout)
            if rawResult.status_code in range(200, 300):
                return True
        except Exception as e:
            print("exception", e)
            return False
        return False

    def run(self):
        # read current var list
        if self._readVarList():
            for task in self.config.taskList:
                print("")
                resultStr = self._getExecResult(
                    command=task.command, timeout=task.execTimeout)
                savedValue = self._getVarValue(task.variableName)
                print("#SAVED :", savedValue)
                print("#RESULT :", resultStr)
                if resultStr != savedValue:
                    apiResult = self._updateVarValue(
                        task.variableName, resultStr, self.config.apiTimeout)
                    print("#UPDATE :", apiResult)
                else:
                    print("#UPDATE : skipped")


def main():
    config = SystemConfig(CONFIG_FILE)
    runner = TaskRunner(config)
    runner.run()
    # run task route each n second(s)
    schedule.every(config.updateInterval).seconds.do(runner.run)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
