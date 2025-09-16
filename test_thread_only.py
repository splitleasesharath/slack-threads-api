import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from slack_thread_client import SlackThreadClient
import time

print("Testing Slack Thread Functionality (Text Only)")
print("=" * 50)

client = SlackThreadClient()

# Test 1: Send message to main channel
print("\n1. Sending message to main channel...")
response = client.send_message("📢 Testing main channel message")
if response and response.get('ok'):
    print(f"   ✅ Message sent successfully!")
    print(f"   Timestamp: {response['ts']}")

# Test 2: Create a thread
print("\n2. Creating a new thread...")
thread_ts = client.start_thread("🧵 Starting a conversation thread")
if thread_ts:
    print(f"   ✅ Thread created successfully!")
    print(f"   Thread ID: {thread_ts}")

    # Test 3: Send replies to thread
    print("\n3. Sending replies to thread...")
    time.sleep(1)

    reply1 = client.reply_to_thread(thread_ts, "Reply 1: This is the first reply")
    if reply1 and reply1.get('ok'):
        print(f"   ✅ First reply sent")

    time.sleep(1)
    reply2 = client.reply_to_thread(thread_ts, "Reply 2: This is the second reply")
    if reply2 and reply2.get('ok'):
        print(f"   ✅ Second reply sent")

    time.sleep(1)
    reply3 = client.reply_to_thread(thread_ts, "Reply 3: Thread conversation working perfectly! ✨")
    if reply3 and reply3.get('ok'):
        print(f"   ✅ Third reply sent")

    # Test 4: Batch messages
    print("\n4. Sending batch messages to thread...")
    messages = [
        "📊 Batch message 1: Starting process...",
        "⚙️ Batch message 2: Processing...",
        "✅ Batch message 3: Complete!"
    ]

    responses = client.send_batch_to_thread(
        thread_ts=thread_ts,
        messages=messages,
        delay_seconds=1.0
    )

    success_count = sum(1 for r in responses if r and r.get('ok'))
    print(f"   ✅ Sent {success_count}/{len(messages)} batch messages")

print("\n" + "=" * 50)
print("✅ Thread functionality test completed!")
print("Check your Slack channel for the thread with multiple replies.")
print("\n📝 Note: For image uploads, you need to add 'files:read' scope")
print("   in your Slack app configuration along with 'files:write'")