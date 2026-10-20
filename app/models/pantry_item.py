from datetime import date

from pydantic import BaseModel, Field

from app.models.macronutrients import Macronutrients
from app.models.product import Product


class PantryItem(BaseModel):
    product: Product
    count: int = 1
    # used if exp_date is unpopulated so we can have rough guess of when to send push notifications for certain food items
    input_date: date = Field(default_factory=date.today)
    exp_date: date | None = None
    # used in tie-in with input_date (if perishable, we will have mapping of rough time frames of when to send notifications)
    # might change this later to an ENUM for multiple vals instead of true/false for more precise mapping
    perishable: bool = False
    macronutrients: Macronutrients = Field(default_factory=Macronutrients)
