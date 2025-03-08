import os
import json
import requests
from datetime import datetime


class LinkedInAutomation:
    def __init__(self, credentials_path):
        self.credentials = self.load_credentials(credentials_path)

    def load_credentials(self, credentials_path):
        with open(credentials_path, 'r') as file:
            return json.load(file)

    def get_headers(self, access_token):
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

    def upload_image_to_linkedin(self, image_path, access_token):
        upload_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
        headers = self.get_headers(access_token)

        upload_request_payload = {
            "registerUploadRequest": {
                "owner": f"urn:li:person:{self.credentials['person_id']}",
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [{
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }]
            }
        }

        upload_response = requests.post(upload_url, headers=headers, json=upload_request_payload)

        if upload_response.status_code != 200:
            print(f"Error in registering upload: {upload_response.status_code}")
            print("Error response:", upload_response.text)
            raise Exception(f"Error in registering upload: {upload_response.text}")

        upload_data = upload_response.json()

        try:
            upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset = upload_data['value']['asset']
            return upload_url, asset
        except KeyError:
            raise Exception("Failed to find 'uploadUrl' in response. Check the response for errors.")

    def upload_image_file(self, image_path, upload_url):
        with open(image_path, 'rb') as f:
            file_data = f.read()
            upload_response = requests.put(upload_url, data=file_data, headers={'Content-Type': 'application/octet-stream'})

            if upload_response.status_code != 201:
                print(f"Failed to upload image. Status code: {upload_response.status_code}")
                print("Error response:", upload_response.text)
                raise Exception(f"Error uploading image: {upload_response.text}")
            else:
                print("Image uploaded successfully!")

    def create_post_with_image(self, access_token, asset, message):
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = self.get_headers(access_token)

        post_data = {
            "author": f"urn:li:person:{self.credentials['person_id']}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": message
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [{
                        "status": "READY",
                        "description": {"text": message},
                        "media": asset,
                    }]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(post_url, headers=headers, json=post_data)

        if response.status_code in [200, 201]:
            print("Post successful!")
            print("Post response:", response.json())
        else:
            print(f"Failed to post. Status Code: {response.status_code}")
            print("Error response:", response.json())

    def upload_and_post_image(self, image_path, message, access_token):
        try:
            upload_url, asset = self.upload_image_to_linkedin(image_path, access_token)
            print(f"Image uploaded successfully, Asset ID: {asset}")

            self.upload_image_file(image_path, upload_url)

            self.create_post_with_image(access_token, asset, message)

        except Exception as e:
            print("Error:", e)


def read_files_from_directory(directory):
    messages = [
        "📊 **Exploring new career opportunities in Data Science**. Passionate about big data, predictive analytics, and real-time data processing. Experienced in using **Pandas**, **NumPy**, and **TensorFlow** for data-driven decision-making. #OpenToWork #DataScience #BigData #AI #Analytics #MachineLearning",
        
        "🚀 **Seeking new job opportunities in Data Science**. Looking for roles involving machine learning, data analysis, and AI. Skilled in **Pandas**, **NumPy**, and **Scikit-learn** for data analysis. Let's connect and discuss opportunities! #OpenToWork #DataScience #MachineLearning #AI #JobSearch #Analytics",
        
        "🌐 **Looking for a position as an API Developer**. Experienced in creating robust APIs with **Django**, **FastAPI**, and **Flask**. Proficient in designing scalable and secure APIs for high-demand applications. #JobSearch #API #FastAPI #Django #OpenToWork #Python #WebDevelopment",
        
        "🛠️ **Searching for challenging positions as an API Developer**. Specializing in building scalable APIs with **FastAPI** and **Django**. Solid experience in integrating APIs with cloud services, databases, and machine learning models. #JobSearch #API #Python #FastAPI #Cloud #APIDeveloper",
        
        "🔍 **Open to job opportunities in Data Science**. Expertise in data mining, machine learning, **Pandas**, **NumPy**, and statistical modeling. Seeking to apply my skills in solving complex business problems and driving data-driven decisions. #OpenToWork #DataScience #MachineLearning #Analytics #JobSearch",
        
        "⚙️ **Looking for new roles in API Development**. Skilled in designing, testing, and optimizing APIs using **FastAPI**, **Django**, and **Flask**. Proficient in integrating data analytics models and building secure production-ready APIs. #APIJobs #OpenToWork #Django #FastAPI #Python #JobSearch",
        
        "💡 **Currently available for a position in Data Science or API Development**. Eager to contribute my expertise in **Pandas**, **NumPy**, **Django**, and **FastAPI** to a dynamic team. Let's connect and discuss how I can contribute to your organization. #JobSearch #OpenToWork #DataScience #API #Python"
    ]

    image_paths = [
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\Consuming-APIs-1.webp",
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\django-4.webp",
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\Top-Robotics-APIs-for-Developers.webp",
        
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\day-5.webp",
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\day-6.jpg",
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\day-7.jpg",
        r"C:\Users\Deepak\Desktop\new\linkedin\deployee\images\funny-cat-2.webp"
    ]
    
    return messages, image_paths


# Example usage of the class
if __name__ == '__main__':
    credentials_path = rf"C:\Users\Deepak\api\linked\credentials.json"
    linkedin_automation = LinkedInAutomation(credentials_path)

    project_directory = rf"C:\Users\Deepak\api\linked"  #   image folder created and  Set the path to your project directory
    messages, image_paths = read_files_from_directory(project_directory)

    # Ensure there is at least one image to go with the messages
    if not image_paths:
        print("Error: No images found in the directory.")
    else:
        # Use the instance's access token directly
        access_token = linkedin_automation.credentials['access_token']

        # Call the method with the correct arguments
        for message, image_path in zip(messages, image_paths):
            linkedin_automation.upload_and_post_image(image_path, message, access_token)
