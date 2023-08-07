from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class AuthenticationResponse(BaseModel):
    access_token: str
    lifetime: timedelta = Field(alias="expires_in", default=timedelta(0))
    epoch: datetime = datetime.now()

    @property
    def expires_at(self) -> datetime:
        return self.epoch + self.lifetime

    @property
    def is_valid(self) -> bool:
        print(f"{self.expires_at} | {datetime.now()}")
        return self.expires_at > datetime.now()
