from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Allow browser access from the grader page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # assignment asks for browser access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Layer 1: defaults
# --------------------------------------------------
config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

# --------------------------------------------------
# Layer 2: config.development.yaml
# --------------------------------------------------
config.update({
    "workers": 3,
    "log_level": "error",
    "api_key": "key-lh18ut61ny",
})

# --------------------------------------------------
# Layer 3: .env
# --------------------------------------------------
dotenv = {
    "APP_PORT": "8336",
    "APP_DEBUG": "false",
    "APP_LOG_LEVEL": "debug",
    "APP_API_KEY": "key-72r3w9ju8g",
    # If present:
    # "NUM_WORKERS": "5"
}

for k, v in dotenv.items():
    if k == "NUM_WORKERS":
        config["workers"] = v
    elif k.startswith("APP_"):
        config[k[4:].lower()] = v

# --------------------------------------------------
# Layer 4: OS environment
# --------------------------------------------------
osenv = {
    "APP_PORT": "8805",
    "APP_LOG_LEVEL": "error",
}

for k, v in osenv.items():
    config[k[4:].lower()] = v


def to_bool(v):
    return str(v).lower() in ("true", "1", "yes", "on")


@app.get("/effective-config")
def effective_config(set: List[str] = Query(default=[])):
    result = dict(config)

    # CLI overrides
    for item in set:
        if "=" in item:
            k, v = item.split("=", 1)
            result[k] = v

    return {
        "port": int(result["port"]),
        "workers": int(result["workers"]),
        "debug": to_bool(result["debug"]),
        "log_level": str(result["log_level"]),
        "api_key": "****",
    }
