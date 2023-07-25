# FitBot: An Advanced Health-Centric Chatbot

FitBot is an AI-driven chatbot that uses large language models (LLMs) such as GPT-4 by OpenAI. It seamlessly integrates with the Nutrition endpoint of API Ninjas, providing accurate nutritional data and personalized health recommendations.

## Features
1. **Nutritional Information Retrieval:** Fetches accurate nutritional data of any given food item by leveraging the Nutrition endpoint of API Ninjas.
2. **Health Calculations:** Computes Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), Ideal Body Weight (IBW), and more.
3. **User-Friendly Interaction:** Features a chat-like interface that is easy to use and interact with.
4. **Consistent Learning and Improvement:** As the underlying model (GPT-4) continues to learn and improve, so too does FitBot.

## Setup and Installation

To get FitBot up and running, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/[YourUsername]/FitBot.git
   cd FitBot

2. **Setup Virtual Environment (Optional)**

    It's recommended to create a virtual environment to keep the dependencies required by this project separate.

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies**

    Install the required packages using pip:

    ```bash
    pip install -r requirements.txt

4. **Run the Project**

    You're all set! Run the project with:

    ```bash
    python run_chatbot.py

## Usage

Once the chatbot is up and running, you can start asking queries. Here's an example of how to interact with it:

Please create a meal plan for a person 1.8m tall, weighting 84.7Kg, who does weight lifting 4 times a week and runs 5Km 2 or 3 times a week and want to go from 12.7% BF to 10% in two months. The person lives in Curitiba, Brazil. Please output the total calories, protein, carbohydrates and fat for each meal. Please inform the person's BMI as well.

FitBot will generate a meal plan based on the information provided and also inform the person's BMI.

## Support

If you encounter any issues or have any questions about the project, feel free to open an issue on this GitHub repository.

## License

FitBot is open-source software licensed under the MIT license.