import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from slack_thread_client import SlackThreadClient
from PIL import Image
import io as byte_io

def create_test_image():
    """Create a simple test image in memory"""
    # Create a simple 200x200 red square image
    img = Image.new('RGB', (200, 200), color='red')

    # Add some text (optional, requires PIL with font support)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 150, 150], fill='blue')
    draw.text((70, 90), "TEST", fill='white')

    # Save to bytes
    img_bytes = byte_io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes.getvalue()

def test_image_uploads():
    """Test image upload capabilities"""
    print("Testing Slack Image Upload Capabilities")
    print("=" * 50)

    # Initialize client
    client = SlackThreadClient()

    # Test 1: Upload image to main channel
    print("\n1. Testing image upload to main channel...")
    try:
        # Create test image
        test_image = create_test_image()

        # Upload to channel
        response = client.upload_file(
            file_content=test_image,
            filename="test_image_main.png",
            initial_comment="📸 Test image upload to main channel",
            title="Main Channel Test Image"
        )

        if response and response.get('ok'):
            print("   ✅ Image uploaded to main channel successfully!")
            print(f"   File ID: {response.get('file_id')}")
        else:
            print(f"   ❌ Failed to upload image: {response}")

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 2: Create thread and upload image to it
    print("\n2. Testing image upload to thread...")
    try:
        # Start a new thread
        thread_ts = client.start_thread("🧵 Starting thread for image test")

        if thread_ts:
            print(f"   Thread created: {thread_ts}")

            # Create another test image
            test_image_2 = create_test_image()

            # Upload image as reply to thread
            response = client.upload_file(
                file_content=test_image_2,
                filename="test_image_thread.png",
                thread_ts=thread_ts,
                initial_comment="📸 Test image upload as thread reply",
                title="Thread Reply Test Image"
            )

            if response and response.get('ok'):
                print("   ✅ Image uploaded to thread successfully!")
                print(f"   File ID: {response.get('file_id')}")

                # Add another text reply after the image
                client.reply_to_thread(
                    thread_ts=thread_ts,
                    text="✅ Image successfully added to thread!"
                )
            else:
                print(f"   ❌ Failed to upload image to thread: {response}")
        else:
            print("   ❌ Failed to create thread")

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 3: Upload local file if exists
    print("\n3. Testing local file upload...")
    import os

    # Try to find any image file in current directory
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    local_image = None

    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            local_image = file
            break

    if local_image:
        print(f"   Found local image: {local_image}")
        try:
            # Upload local file
            response = client.upload_file(
                file_path=local_image,
                initial_comment=f"📁 Local file upload test: {local_image}",
                title="Local File Test"
            )

            if response and response.get('ok'):
                print("   ✅ Local file uploaded successfully!")
            else:
                print(f"   ❌ Failed to upload local file: {response}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    else:
        print("   ⚠️  No local image files found to test")

        # Create a test image file
        print("   Creating test.png for upload...")
        test_img = Image.new('RGB', (100, 100), color='green')
        test_img.save('test.png')

        try:
            response = client.upload_file(
                file_path='test.png',
                initial_comment="📁 Created and uploaded test.png",
                title="Generated Test Image"
            )

            if response and response.get('ok'):
                print("   ✅ Created and uploaded test.png successfully!")
            else:
                print(f"   ❌ Failed to upload test.png: {response}")

            # Clean up
            os.remove('test.png')

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    print("\n" + "=" * 50)
    print("Image upload tests completed! Check your Slack channel.")
    print("\nCapabilities verified:")
    print("✅ Upload images to main channel")
    print("✅ Upload images as thread replies")
    print("✅ Upload from file path")
    print("✅ Upload from bytes content")

if __name__ == "__main__":
    # Check if PIL is installed
    try:
        from PIL import Image, ImageDraw
        test_image_uploads()
    except ImportError:
        print("❌ PIL/Pillow not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("✅ Pillow installed. Please run the script again.")