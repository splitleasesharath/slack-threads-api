import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from slack_thread_client import SlackThreadClient
from PIL import Image, ImageDraw, ImageFont
import io as byte_io
import time

def create_test_image(text="Test Image", color='blue'):
    """Create a simple test image with text"""
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)

    # Draw a colored rectangle
    draw.rectangle([50, 50, 350, 150], fill=color, outline='black', width=2)

    # Add text
    draw.text((200, 100), text, fill='white', anchor='mm')

    # Convert to bytes
    img_bytes = byte_io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes.getvalue()

def moderate_image_test():
    """Moderate test for image uploads - one at a time with pauses"""
    print("Moderate Image Upload Test")
    print("=" * 50)
    print("Testing image uploads with moderate pacing...\n")

    client = SlackThreadClient()

    # Test 1: Upload image as main message
    print("TEST 1: Upload image as main message")
    print("-" * 40)
    try:
        print("Creating test image...")
        main_image = create_test_image("Main Channel Image", 'green')

        print("Uploading image to main channel...")
        response = client.upload_file(
            file_content=main_image,
            filename="main_channel_test.png",
            initial_comment="📷 Test 1: Image uploaded to main channel",
            title="Main Channel Test"
        )

        if response and response.get('ok'):
            print("✅ SUCCESS: Image uploaded to main channel")
            print(f"   File ID: {response.get('file_id')}")
        else:
            print(f"❌ FAILED: {response.get('error')}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

    # Pause before next test
    print("\nWaiting 3 seconds before next test...")
    time.sleep(3)

    # Test 2: Create thread then upload image to it
    print("\nTEST 2: Upload image as thread reply")
    print("-" * 40)
    try:
        print("Creating new thread...")
        thread_ts = client.start_thread("🧵 Thread for image test")

        if thread_ts:
            print(f"✅ Thread created: {thread_ts}")

            print("Waiting 2 seconds...")
            time.sleep(2)

            print("Creating test image for thread...")
            thread_image = create_test_image("Thread Reply Image", 'blue')

            print("Uploading image to thread...")
            response = client.upload_file(
                file_content=thread_image,
                filename="thread_reply_test.png",
                thread_ts=thread_ts,
                initial_comment="📷 Test 2: Image uploaded as thread reply",
                title="Thread Reply Test"
            )

            if response and response.get('ok'):
                print("✅ SUCCESS: Image uploaded to thread")
                print(f"   File ID: {response.get('file_id')}")
                print(f"   Thread TS: {thread_ts}")

                # Add a text reply after the image
                print("\nAdding text reply after image...")
                time.sleep(2)
                client.reply_to_thread(
                    thread_ts=thread_ts,
                    text="✅ Image successfully added to thread above!"
                )
                print("✅ Text reply added")
            else:
                print(f"❌ FAILED: {response.get('error')}")
        else:
            print("❌ Failed to create thread")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Test 1: Upload image to main channel")
    print("- Test 2: Upload image as thread reply")
    print("\n⚠️ Note: If tests fail with 'missing_scope', ensure you have:")
    print("   - files:write scope")
    print("   - files:read scope")
    print("   And remember to reinstall the app and update the token!")

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw
        moderate_image_test()
    except ImportError:
        print("Installing Pillow for image generation...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("✅ Pillow installed. Please run the script again.")