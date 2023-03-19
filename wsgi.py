import uvicorn

from viva_vdm.v1.api import app


def main():
    uvicorn.run(app, port=8000, host='0.0.0.0')


if __name__ == "__main__":
    main()
