from litellm import completion
import os
import json
from dotenv import load_dotenv
load_dotenv()

def get_weather(city):
    """
    Dummy weather function that returns mock weather data
    """
    weather_data = {
        "indore": {
            "city": "Indore",
            "temperature": "28°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind_speed": "12 km/h"
        },
        "mumbai": {
            "city": "Mumbai", 
            "temperature": "32°C",
            "condition": "Sunny",
            "humidity": "70%",
            "wind_speed": "8 km/h"
        },
        "delhi": {
            "city": "Delhi",
            "temperature": "25°C", 
            "condition": "Hazy",
            "humidity": "45%",
            "wind_speed": "15 km/h"
        }
    }
    
    return weather_data.get(city.lower(), {
        "city": city,
        "temperature": "Unknown",
        "condition": "Data not available",
        "humidity": "Unknown",
        "wind_speed": "Unknown"
    })

# Define available tools for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {
        "content": "What is the weather in Indore?",
        "role": "user"
    }
]

response = completion(
    model="gemini/gemini-2.5-flash",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# print complete response
print(json.dumps(response.model_dump(), indent=4))
print("---------------------")

# print only llm text response
print('llm text response:')
print(response.choices[0].message.content)

# Check if the LLM wants to call the weather function
if response.choices[0].message.tool_calls:
    print("\n" + "="*50)
    print("LLM wants to call weather function:")
    
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "get_weather":
            # Parse the arguments
            args = json.loads(tool_call.function.arguments)
            city = args.get("city", "Indore")
            
            print(f"Calling get_weather for city: {city}")
            
            # Call our dummy weather function
            weather_result = get_weather(city)
            
            print("Weather data:")
            print(json.dumps(weather_result, indent=2))
            
            # Create a follow-up message with the weather data
            follow_up_messages = messages + [
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": response.choices[0].message.tool_calls
                },
                {
                    "role": "tool",
                    "content": json.dumps(weather_result),
                    "tool_call_id": tool_call.id
                }
            ]
            
            # Get the final response with weather data
            final_response = completion(
                model="gemini/gemini-2.5-flash",
                messages=follow_up_messages
            )
            
            print("\n" + "="*50)
            print("Final response with weather data:")
            print(final_response.choices[0].message.content)