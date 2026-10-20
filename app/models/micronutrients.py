from pydantic import BaseModel

class Micronutrients(BaseModel):
    # we can add/remove based on whatever is common in more diverse food labels
    vitaminC: float = 0.0
    vitaminD: float = 0.0
    vitaminA: float = 0.0
    iron: float = 0.0
    potassium: float = 0.0
    calcium: float = 0.0