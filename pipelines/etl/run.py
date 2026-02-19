from dotenv import load_dotenv

from pipelines.etl.etl_service import ETLService


if __name__ == "__main__":
    load_dotenv()

    service = ETLService()
    service.run()
