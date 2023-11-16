import fastapi
import requests


app = fastapi.FastAPI()

# an api for downloading every minecraft server.jar version

def getLaterVersionVainilla(version: str):
    verMeta = ""
    req = requests.get(f"https://launchermeta.mojang.com/mc/game/version_manifest.json")
    versions = req.json()["versions"]

    for num in versions:
        if num["id"] == version:
            verMeta = num["url"]
            break
    req = requests.get(verMeta)
    return req.json()["downloads"]["server"]["url"]


def getLatestVersionFabric(version: str):
    req = requests.get(f"https://meta.fabricmc.net/v2/versions/loader/{version}/")
    version = req.json()[0]["loader"]["version"]
    return version

def getLatestVersionPaper(version: str):
    req = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{version}/")
    version = req.json()["builds"]
    max = 0
    for num in version:
        if int(num) > max:
            max = int(num)
    return max

def getLatestMinecraftVersion():
    req = requests.get(f"https://launchermeta.mojang.com/mc/game/version_manifest.json")
    versions = req.json()["latest"]
    return versions["release"]

implemented = ["fabric", "paper", "vainilla", "spigot"]


@app.get("/")
def index():
    return {}

@app.get("/api")
def api():
    return {"usage": {"/api/{type}/": "get latest release", "/api/{type}/{version}/": "get specific minecraft version", }, "types": implemented, "version": "minecraft versions"}

@app.get("/api/{type}")
def api(type: str):
    if type == "fabric":
        return fastapi.responses.RedirectResponse(f"https://maven.fabricmc.net/net/fabricmc/fabric-loader/{getLatestVersionFabric(getLatestMinecraftVersion())}/fabric-loader-{getLatestVersionFabric(getLatestMinecraftVersion())}.jar")
    elif type == "paper":
        return fastapi.responses.RedirectResponse(f"https://papermc.io/api/v2/projects/paper/versions/{getLatestMinecraftVersion()}/builds/{getLatestVersionPaper(getLatestMinecraftVersion())}/downloads/paper-{getLatestMinecraftVersion()}-{getLatestVersionPaper(getLatestMinecraftVersion())}.jar")
    elif type == "vainilla":
        return fastapi.responses.RedirectResponse(getLaterVersionVainilla(getLatestMinecraftVersion()))
    elif type == "spigot":
        return fastapi.responses.RedirectResponse(f"https://download.getbukkit.org/spigot/spigot-{getLatestMinecraftVersion()}.jar")
    else:
        return {"error": "type not found", "valid-types": implemented}

@app.get("/api/{type}/{version}")
def api(type: str, version: str):
    if type == "fabric":
        return fastapi.responses.RedirectResponse(f"https://maven.fabricmc.net/net/fabricmc/fabric-loader/{getLatestVersionFabric(version)}/fabric-loader-{getLatestVersionFabric(version)}.jar")
    elif type == "paper":
        return fastapi.responses.RedirectResponse(f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{getLatestVersionPaper(version)}/downloads/paper-{version}-{getLatestVersionPaper(version)}.jar")
    elif type == "vainilla":
        return fastapi.responses.RedirectResponse(getLaterVersionVainilla(version))
    elif type == "spigot":
        return fastapi.responses.RedirectResponse(f"https://download.getbukkit.org/spigot/spigot-{version}.jar")
    else:
        return {"error": "type not found", "valid-types": implemented}

app.host("0.0.0.0", app, "Tetas")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )



