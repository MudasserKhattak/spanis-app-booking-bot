#!/bin/bash

# Docker entrypoint script for Spanish Appointment Bot

set -e

# Start Xvfb for headless browser operation
echo "Starting Xvfb display server..."
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
export DISPLAY=:99

# Wait for Xvfb to start
sleep 2

# Test Chrome installation
echo "Testing Chrome installation..."
google-chrome --version
chromedriver --version

# Test espeak for audio notifications
echo "Testing audio system..."
espeak "System ready" 2>/dev/null || echo "Audio system initialized (may not have sound output in container)"

echo "Spanish Appointment Bot container is ready!"
echo "Chrome and ChromeDriver are properly installed"
echo "Audio notifications are available via espeak"
echo ""
echo "To run the bot, use commands like:"
echo "  python example1.py"
echo "  python example2.py"
echo "  python your_custom_script.py"
echo ""
echo "Don't forget to configure your CustomerProfile with real data!"

# Execute the main command
exec "$@"
