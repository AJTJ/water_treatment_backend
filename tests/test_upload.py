# from typing import Any
# import requests

# # Set the URL of the FastAPI endpoint
# UPLOAD_URL = "http://localhost:8000/api/v1/s3/upload/"  # Adjust the port if your FastAPI server is running on a different port

# # Path to the image file in the project root
# image_file_path = (
#     "/Users/ajtj/python_projects/water_treatment_backend/tech_headshot.jpeg"
# )


# def upload_image(file_path: str) -> Any:
#     """
#     Uploads an image to the specified FastAPI endpoint.

#     :param file_path: The path to the image file to upload.
#     :return: Response from the server.
#     """
#     with open(file_path, "rb") as file:
#         files = {"file": (file_path, file)}
#         try:
#             response = requests.post(UPLOAD_URL, files=files)
#             response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             return {"error": str(e)}


# # Test the upload by sending the tech_headshot.jpg file
# if __name__ == "__main__":
#     result = upload_image(image_file_path)
#     print(result)
