from pathlib import Path
from urllib.parse import urljoin
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=['.env'],
        case_sensitive=False,
    )

    URL_HH_BASE: str
    URL_HH_VACANCIES: str
    
    PER_PAGE: int = 100

    LOG_FORMAT: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"

    FILEPATH: Path = Path(__file__).parent / 'data' / 'vacancies_data.json'

    @property
    def url_get_vacancies(self):
        return urljoin(self.URL_HH_BASE, self.URL_HH_VACANCIES)

settings = Settings()