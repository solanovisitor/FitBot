import requests

from agent.agents import Agent

class FitnessAgent:
    def __init__(self, openai_api_key: str, nut_api_key: str):
        self.openai_api_key = openai_api_key
        self.nut_api_key = nut_api_key

        self.agent = Agent(
            openai_api_key=self.openai_api_key,
            functions=[self.get_nutritional_info, self.calculate_bmr, self.calculate_tdee, self.calculate_ibw, self.calculate_bmi, self.calculate_calories_to_lose_weight]
        )

    def get_nutritional_info(self, query: str) -> dict:
        """Fetch the nutritional information for a specific food item.

        :param query: The food item to get nutritional info for
        :return: The nutritional information of the food item
        """
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, timeout=100, headers={'X-Api-Key': self.nut_api_key})

        if response.status_code == requests.codes.ok:
            return response.json()  # Use json instead of text for a more structured data
        else:
            return {"Error": response.status_code, "Message": response.text}
        
    def calculate_bmi(self, weight: float, height: float) -> float:
        """Calculate the Body Mass Index (BMI) for a person.

        :param weight: The weight of the person in kg
        :param height: The height of the person in cm
        :return: The BMI of the person
        """
        height_meters = height / 100  # convert cm to meters
        bmi = weight / (height_meters ** 2)
        return round(bmi, 2)  # round to 2 decimal places for readability
    
    def calculate_calories_to_lose_weight(self, desired_weight_loss_kg: float) -> float:
        """Calculate the number of calories required to lose a certain amount of weight.

        :param desired_weight_loss_kg: The amount of weight the person wants to lose, in kilograms
        :return: The number of calories required to lose that amount of weight
        """
        calories_per_kg_fat = 7700  # Approximate number of calories in a kg of body fat
        return desired_weight_loss_kg * calories_per_kg_fat


    def calculate_bmr(self, weight: float, height: float, age: int, gender: str, equation: str = 'mifflin_st_jeor') -> float:
        """Calculate the Basal Metabolic Rate (BMR) for a person.

        :param weight: The weight of the person in kg.
        :param height: The height of the person in cm.
        :param age: The age of the person in years.
        :param gender: The gender of the person ('male' or 'female')
        :param equation: The equation to use for BMR calculation ('harris_benedict' or 'mifflin_st_jeor')
        :return: The BMR of the person
        """
        if equation.lower() == 'mifflin_st_jeor':
            if gender.lower() == 'male':
                return (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:  # 'female'
                return (10 * weight) + (6.25 * height) - (5 * age) - 161
        else:  # 'harris_benedict'
            if gender.lower() == 'male':
                return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:  # 'female'
                return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate the Total Daily Energy Expenditure (TDEE) for a person.

        :param bmr: The BMR of the person
        :param activity_level: The activity level of the person
        ('sedentary', 'lightly_active', 'moderately_active', 'very_active', 'super_active')
        :return: The TDEE of the person
        """
        activity_factors = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'super_active': 1.9,
        }
        return bmr * activity_factors.get(activity_level, 1)

    def calculate_ibw(self, height: float, gender: str) -> float:
        """Calculate the Ideal Body Weight (IBW).

        :param height: The height of the person in inches
        :param gender: The gender of the person ("male" or "female")
        :return: The Ideal Body Weight in kg
        """
        if gender.lower() == 'male':
            if height <= 60:  # 5 feet = 60 inches
                return 50
            else:
                return 50 + 2.3 * (height - 60)
        elif gender.lower() == 'female':
            if height <= 60:
                return 45.5
            else:
                return 45.5 + 2.3 * (height - 60)
        else:
            raise ValueError("Invalid gender. Expected 'male' or 'female'.")

    def ask(self, question: str):
        response = self.agent.ask(question)
        return response

    def view_functions(self):
        return self.agent.functions

    def view_chat_history(self):
        return self.agent.chat_history