# VNC Connection Troubleshooting Guide

## Quick Fix Commands

### 1. Test VNC Server (Simple Method)
```bash
# Stop any running containers
docker stop $(docker ps -q --filter ancestor=spanish-bot-vnc)

# Run simple VNC test
docker run -it --rm -p 5900:5900 spanish-bot-vnc /bin/bash -c "
  echo 'Starting Xvfb...';
  Xvfb :1 -screen 0 1280x720x24 &
  sleep 3;
  echo 'Starting VNC server...';
  x11vnc -display :1 -nopw -listen 0.0.0.0 -xkb -rfbport 5900 -shared -forever -bg;
  sleep 2;
  echo 'VNC server started. Testing connection...';
  netstat -tlnp | grep 5900;
  echo 'Try connecting VNC client to localhost:5900 now';
  echo 'Press Ctrl+C when done testing';
  sleep 300
"
```

### 2. Run VNC Test with Browser
```bash
# Copy visual config if not done already
cp my_config_visual.py.example my_config_visual.py

# Run VNC container with test
docker run -it --rm -p 5900:5900 \
  -v $(pwd)/test-vnc.py:/app/test-vnc.py \
  spanish-bot-vnc /bin/bash -c "
    /usr/local/bin/docker-entrypoint-vnc.sh python test-vnc.py
  "
```

## Common Issues and Solutions

### Issue 1: "VNC server closed connection"

**Cause:** VNC server not listening on correct interface

**Solution:**
```bash
# Check if VNC is listening on the right port inside container
docker exec -it <container_id> netstat -tlnp | grep 5900

# Should show: 0.0.0.0:5900 (not 127.0.0.1:5900)
```

### Issue 2: "Connection refused"

**Cause:** VNC server not started or port not exposed

**Solution:**
```bash
# Check container logs
docker logs <container_id>

# Check if port is exposed
docker port <container_id>

# Should show: 5900/tcp -> 0.0.0.0:5900
```

### Issue 3: "Can't connect to display :1"

**Cause:** Xvfb not running or display issue

**Solution:**
```bash
# Check Xvfb process
docker exec -it <container_id> ps aux | grep Xvfb

# Restart display server
docker exec -it <container_id> /bin/bash -c "
  killall Xvfb;
  Xvfb :1 -screen 0 1280x720x24 &
  sleep 2;
  x11vnc -display :1 -nopw -listen 0.0.0.0 -rfbport 5900 -shared -forever &
"
```

## VNC Client Configuration

### TightVNC Viewer (Windows)
- Server: `localhost:5900` or `localhost::5900`
- Password: Leave empty
- Options: Enable "Request shared session"

### RealVNC Viewer
- Address: `localhost:5900`
- Encryption: Prefer off (for testing)
- Authentication: None

### Built-in macOS Screen Sharing
- Address: `vnc://localhost:5900`
- Password: Leave empty

### Remmina (Linux)
- Protocol: VNC
- Server: `localhost:5900`
- Password: Leave empty
- Color depth: True color (24 bit)

## Debugging Commands

### Check Container Status
```bash
# List running containers
docker ps

# Check container logs
docker logs <container_id>

# Access container shell
docker exec -it <container_id> bash
```

### Check Network Connectivity
```bash
# Test port connectivity from host
telnet localhost 5900

# Or using nc
nc -zv localhost 5900

# Should return: Connection to localhost 5900 port [tcp/*] succeeded!
```

### Manual VNC Server Start
```bash
# If automatic start fails, start manually
docker exec -it <container_id> /bin/bash -c "
  export DISPLAY=:1;
  killall x11vnc Xvfb 2>/dev/null;
  Xvfb :1 -screen 0 1280x720x24 &
  sleep 3;
  x11vnc -display :1 -nopw -listen 0.0.0.0 -rfbport 5900 -shared -forever -bg;
  echo 'VNC server restarted';
  netstat -tlnp | grep 5900
"
```

### Test Browser in Container
```bash
# Open interactive shell and test browser
docker exec -it <container_id> /bin/bash

# Inside container:
export DISPLAY=:1
python -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.google.com')
input('Press Enter to close browser...')
driver.quit()
"
```

## Alternative: noVNC Web Client

If traditional VNC clients don't work, you can use noVNC (web-based):

```bash
# Run container with noVNC
docker run -it --rm \
  -p 5900:5900 \
  -p 6080:6080 \
  spanish-bot-vnc /bin/bash -c "
    /usr/local/bin/docker-entrypoint-vnc.sh &
    sleep 5;
    # Install and start noVNC (if available)
    echo 'VNC running on :5900, noVNC would be on :6080';
    sleep 300
  "
```

## Success Verification

When VNC is working correctly, you should see:
1. ✅ Container logs show "VNC server started successfully"
2. ✅ `netstat` shows `0.0.0.0:5900` listening
3. ✅ VNC client connects without "connection closed" error
4. ✅ You see a desktop/window manager in VNC client
5. ✅ Browser windows appear when running Python scripts

## Quick Test Script

Save this as `quick-vnc-test.sh`:
```bash
#!/bin/bash
echo "🧪 Quick VNC Test"
echo "1. Building VNC image..."
docker build -f Dockerfile.vnc -t spanish-bot-vnc . > /dev/null

echo "2. Starting VNC container..."
CONTAINER_ID=$(docker run -d -p 5900:5900 spanish-bot-vnc /bin/bash -c "
  /usr/local/bin/docker-entrypoint-vnc.sh sleep 60
")

echo "3. Waiting for VNC to start..."
sleep 5

echo "4. Testing VNC port..."
if nc -zv localhost 5900 2>/dev/null; then
    echo "✅ VNC port is accessible!"
    echo "🎯 Try connecting your VNC client to localhost:5900"
    echo "Container ID: $CONTAINER_ID"
    echo "Run: docker logs $CONTAINER_ID"
else
    echo "❌ VNC port not accessible"
    echo "Container logs:"
    docker logs $CONTAINER_ID
fi

echo "5. Container will stop automatically in 60 seconds"
```

Make it executable: `chmod +x quick-vnc-test.sh`
Run it: `./quick-vnc-test.sh`
