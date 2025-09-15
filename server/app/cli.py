import sys
import uvicorn

def dev():
    uvicorn.run("app.main:app", reload=True, port=8000)

def prod():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

def main():
    cmd = (sys.argv[1:] + ["dev"])[0]
    {"dev": dev, "prod": prod}.get(cmd, dev)()

if __name__ == "__main__":
    main()
