PointRisk - Forest Fires Predicting System
A forest fire predicting weather web application.
Overview
Predicts real-time forest fire risk.
Location-specific: Users can input a city or coordinates.
Uses current weather data.
Employs two prediction methods:
● Simple formula.
● Smarter machine learning model (Random Forest).
Goal: To increase awareness and enable fire prevention.
1. Prerequisites for Running the Project
Software Requirements:
● Any web browser such as Chrome, Edge, Safari.
● Requires Python 3.13.1 or higher installed in the system.
● A code editor or platform is needed to run the backend, such as Visual Studio
Code (VS Code) or Google Colab.
● Website solely runs on a web browser.
Hardware Requirements:
● Any PC/Laptop.
● Stable internet connection for the prediction and response output.
2. How to Execute the Project
Step 1: Run the back end
1. Open the Backend File - Locate the file named app.py. This file contains the
backend logic for the application.
2. Launch in Your Preferred Code Editor - Open app.py using Visual Studio
Code (VS Code) or any code editor/IDE of your choice.
3. Start the Server - In the terminal (within VS Code or your system terminal), run
the following command:
python app.py
4. Verify the Server is Running - After executing the command, several lines will
appear in the terminal.
Look for the line that says:
Running on http://127.0.0.1:5000/
5. Open the Website - Click on the local URL (http://127.0.0.1:5000/) or
paste it into your browser. The website should now be displayed and ready for
use.
Step 2: Using the Dashboard
The dashboard provides two methods for wildfire risk prediction, along with several
informative tabs:
Prediction (City-Based)
1. Enter the city name in the input text field.
2. Click the "Predict" button.
3. Scroll down to view the complete output.
4. A summary panel will display:
○ Wildfire risk percentage
○ City name
○ Date and time
○ Temperature
○ Humidity
○ Windspeed
5. Below this, a weather map will visualize the selected city's geographical and
climatic conditions.
Prediction (Coordinates / ML-Based)
1. Enter the latitude and longitude of the desired location.
2. Click the "Predict (ML)" button.
3. Scroll down to view the complete output.
4. A summary panel will display:
○ Wildfire risk percentage
○ Latitude and longitude
○ Temperature
○ Humidity
○ Windspeed
5. Below this, a weather map will show the location's climate data and map view.
About Us Tab
Provides a brief introduction to the website and its purpose.
Precautions Tab
Redirects users to a verified page containing safety measures and precautions related
to forest fires.
Know More About Forest Fires Tab
Links to an authenticated resource that explains the causes and impacts of forest fires
in detail.
3. Technologies Used
● Frontend: HTML, CSS, JavaScript
● UI & Icons: Google Fonts (Poppins)
● Mapping: Leaflet.js for dynamic weather and geographical maps
4. Test Scenarios (Quick Check)
To quickly test and evaluate the application's functionality:
● Enter a city name to receive immediate wildfire risk predictions.
● Enter latitude and longitude for more precise, ML-based predictions.
● Use either input method to generate an interactive map-based output.
Conclusion
You can easily demonstrate and test this project by running the backend (app.py) and
opening the provided localhost URL in a web browser. The system is designed to be:
● Simple to set up
● Easy to navigate
● User-friendly for quick interaction and evaluation
