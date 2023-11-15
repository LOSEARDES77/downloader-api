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


@app.get("/")
def index():
    return {"message": "It works!"}

@app.get("/fabric/{version}")
def fabric(version: str):
    return fastapi.responses.RedirectResponse(f"https://maven.fabricmc.net/net/fabricmc/fabric-loader/{getLatestVersionFabric(version)}/fabric-loader-{getLatestVersionFabric(version)}.jar")

@app.get("/paper/{version}")
def paper(version: str):
    return fastapi.responses.RedirectResponse(f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{getLatestVersionPaper(version)}/downloads/paper-{version}-{getLatestVersionPaper(version)}.jar")

@app.get("/vainilla/{version}")
def vainilla(version: str):
    return fastapi.responses.RedirectResponse(getLaterVersionVainilla(version))

@app.get("/spigot/{version}")
def spigot(version: str):
    return fastapi.responses.RedirectResponse(f"https://download.getbukkit.org/spigot/spigot-{version}.jar")

app.host("0.0.0.0", app, "Tetas")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )



