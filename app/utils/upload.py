import cloudinary.uploader

def upload_image(file):
    result = cloudinary.uploader.upload(
        file,
        folder="aiutility_uploads",
        resource_type="image"
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }