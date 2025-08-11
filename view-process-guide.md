# How to View the Selenium Process

There are several ways to see what's happening when the Spanish Appointment Bot runs with Selenium:

## Method 1: VNC Connection (Best for Real-time Viewing) 🎬

### Build and Run VNC-enabled Container:
```bash
# Build VNC-enabled image
docker build -f Dockerfile.vnc -t spanish-bot-vnc .

# Run with VNC support
docker run -it --rm \
  -p 5900:5900 \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/my_config_visual.py:/app/my_config_visual.py \
  spanish-bot-vnc bash

# Inside container, start VNC and run bot
/usr/local/bin/docker-entrypoint-vnc.sh python my_config_visual.py
```

### Connect VNC Client:
- **Address:** `localhost:5900`
- **Password:** None (no password required)

### VNC Clients:
- **Windows:** TightVNC, RealVNC, UltraVNC
- **macOS:** Built-in Screen Sharing, RealVNC
- **Linux:** Remmina, TigerVNC, Vinagre
- **Web Browser:** noVNC (if configured)

## Method 2: Screenshot Monitoring 📸

Enable automatic screenshots in your configuration:

```python
customer = CustomerProfile(
    # ... your other settings ...
    save_artifacts=True,  # Enable screenshots
    auto_captcha=False,   # Disable auto-captcha to see captcha pages
)
```

Screenshots are saved to the `artifacts/` directory:
- `citas-TIMESTAMP.png` - Available appointment slots
- `offices-TIMESTAMP.html` - Available offices
- `CONFIRMED-CITA-TIMESTAMP.png` - Successful booking
- `error-TIMESTAMP.png` - Error states

### View Screenshots:
```bash
# List all screenshots
ls -la artifacts/

# View latest screenshots (Linux/macOS)
ls -t artifacts/*.png | head -5 | xargs -I {} echo "Latest: {}"

# Open artifacts folder (Windows)
explorer artifacts

# Open artifacts folder (macOS)
open artifacts

# Open artifacts folder (Linux)
xdg-open artifacts
```

## Method 3: Debug Mode with Pauses ⏸️

Modify your script to pause at key moments:

```python
import time

# Add pauses in your custom script
def debug_cycle_cita(driver, context, fast_forward_url, fast_forward_url2):
    # ... existing code ...
    
    # Take screenshot and pause
    driver.save_screenshot(f"debug-step-{time.time()}.png")
    print("Pausing for 10 seconds to inspect...")
    time.sleep(10)
    
    # Continue with process...
```

## Method 4: Browser Logs 📝

Enable browser logging to see what's happening:

```python
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Add to your webdriver setup
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'browser': 'ALL'}

# Get logs during execution
logs = driver.get_log('browser')
for log in logs:
    print(f"Browser log: {log}")
```

## Method 5: Interactive Container 🖥️

Run the container interactively to control execution:

```bash
# Start interactive container
docker-compose run --rm spanish-bot bash

# Inside container, run step by step
python -c "
from bcncita import *
customer = CustomerProfile(...)
driver = init_wedriver(customer)
# Now manually call functions and inspect
"
```

## Quick Setup for VNC Viewing:

1. **Copy visual config:**
   ```bash
   cp my_config_visual.py.example my_config_visual.py
   # Edit with your real data
   ```

2. **Build VNC image:**
   ```bash
   docker build -f Dockerfile.vnc -t spanish-bot-vnc .
   ```

3. **Run with VNC:**
   ```bash
   docker run -it --rm -p 5900:5900 \
     -v $(pwd)/my_config_visual.py:/app/my_config_visual.py \
     -v $(pwd)/artifacts:/app/artifacts \
     spanish-bot-vnc
   ```

4. **Connect VNC client to `localhost:5900`**

5. **Inside container:**
   ```bash
   python my_config_visual.py
   ```

Now you can watch the browser in real-time as it navigates the Spanish appointment website!

## Tips:
- VNC Method: Best for development and debugging
- Screenshot Method: Good for production monitoring
- Use `auto_captcha=False` to see captcha solving process
- Enable `save_artifacts=True` for automatic documentation
- Lower the `cycles` number for shorter testing sessions
