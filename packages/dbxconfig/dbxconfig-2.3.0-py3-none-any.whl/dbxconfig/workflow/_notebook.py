# used to carry notebook data
from pydantic import BaseModel, Field


class Notebook(BaseModel):
    path: str = Field(...)
    timeout: int = Field(default=3600)
    parameters: dict = Field(default=None)
    retry: int = Field(default=0)
    enabled: bool = Field(default=True)

    # add the notebook name to parameters using the path and return
    def get_parameters(self):
        """Add the notebook path to parameters"""

        if not self.parameters:
            self.parameters = dict()

        params = self.parameters
        params["notebook"] = self.path

        return params
