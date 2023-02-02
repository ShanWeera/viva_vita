from pydantic import BaseModel, Field


class TaxonomyDBSuggestion(BaseModel):
    taxid: int = Field(..., title='Taxonomy ID')
    label: str = Field(..., title='Label for this taxonomy DB entry')
    value: str = Field(..., title='Unique value for this taxonomy DB entry')
