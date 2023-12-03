import geocoder
import paho.mqtt.client as mqtt
import time
import logging

# MQTT broker details
broker_address = "197.2.47.247"
topic = "location"  # Topic to publish location

# Instantiate the MQTT client
client = mqtt.Client("RaspberryPi")

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the log level to DEBUG

# Function to get location
def get_location():
    g = geocoder.ip('me')
    return g.latlng

# Function to publish location to MQTT broker
def publish_location():
    max_retries = 5  # Set the maximum number of retry attempts
    retry_count = 0  # Initialize the retry counter

    while retry_count < max_retries:
        try:
            client.connect(broker_address, port = 5465  )
            logging.debug("Connected to the broker")
            break  # Break the loop if successful connection
        except TimeoutError as te:
            retry_count += 1
            logging.debug(f"Timeout Error: {te}")
            if retry_count < max_retries:
                time.sleep(10)  # Wait for 10 seconds before retrying
            else:
                logging.error("Max retry attempts reached. Exiting.")
                return  # Exit the function if max retries reached

    while True:
        location = get_location()
        if location:
            latitude, longitude = location
            message = f"{latitude},{longitude}"
            client.publish(topic, message)
            logging.debug(f"Published location: {message}")
            print("Published location:", message)
        time.sleep(10)  # Publish every 60 seconds

    client.loop_forever()

# Execute the publish_location function
publish_location()
