#!/bin/bash

# VNC-enabled Docker entrypoint script for Spanish Appointment Bot

set -e

echo "🔧 Starting VNC-enabled Spanish Appointment Bot..."

# Start Xvfb for display
echo "Starting Xvfb display server on :1..."
Xvfb :1 -screen 0 1280x720x24 > /dev/null 2>&1 &
export DISPLAY=:1

# Wait for Xvfb to start
sleep 3

# Start window manager
echo "Starting Fluxbox window manager..."
fluxbox > /dev/null 2>&1 &

# Start VNC server
echo "Starting VNC server on port 5900..."
x11vnc -display :1 -nopw -listen 0.0.0.0 -xkb -rfbport 5900 -shared -forever > /dev/null 2>&1 &

# Wait for VNC to start
sleep 2

echo "✅ VNC server started successfully!"
echo "📺 Connect with VNC client to: localhost:5900"
echo ""

# Test Chrome installation
echo "Testing Chrome installation..."
google-chrome --version
chromedriver --version

echo ""
echo "🎯 You can now:"
echo "  1. Connect VNC client to localhost:5900 to watch the browser"
echo "  2. Run your bot scripts and see them in action!"
echo ""

# Execute the main command
exec "$@"
