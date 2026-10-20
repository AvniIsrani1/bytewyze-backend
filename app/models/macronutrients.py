from pydantic import BaseModel, Field
from app.models.micronutrients import Micronutrients

class Macronutrients(BaseModel):
    calories: float = 0.0

    # fat
    totalFat: float = 0.0
    saturatedFat: float = 0.0
    transFat: float = 0.0

    cholesterol: float = 0.0
    sodium: float = 0.0

    # carbs
    totalCarb: float = 0.0
    dietaryFiber: float = 0.0
    totalSugars: float = 0.0
    addedSugars: float = 0.0

    protein: float = 0.0

    # vitamins + minerals
    micronutrients: Micronutrients = Field(default_factory = Micronutrients)





