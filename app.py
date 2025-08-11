import streamlit as st
import requests

st.set_page_config(page_title="Image Generator", page_icon="🎨", layout="centered")
st.title("🎨 AI Image Generator")

# Input prompt from user
prompt = st.text_input("Enter your prompt:", placeholder="E.g., A futuristic city skyline at sunset")

# Generate image button
if st.button("Generate Image"):
    if prompt.strip():
        try:
            api_url = f"https://88k3gu36od.execute-api.us-east-1.amazonaws.com/Dev/?prompt={prompt}"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()

                # Directly get the presigned URL from body
                image_url = data.get("body")

                if image_url:
                    # Display image
                    st.image(image_url, caption=f"Prompt: {prompt}", use_container_width=True)

                    # Fetch image bytes for download
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        st.download_button(
                            label="📥 Download Image",
                            data=img_response.content,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
                    else:
                        st.error("Failed to download image from S3.")

                else:
                    st.error("Image URL not found in API response.")

            else:
                st.error(f"API request failed with status {response.status_code}")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt before generating.")
