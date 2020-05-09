import luigi

from .tasks import MainPage

if __name__ == "__main__":
    luigi.build([MainPage()], local_scheduler=True)
