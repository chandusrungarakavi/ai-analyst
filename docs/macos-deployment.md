# macOS Deployment Guide

This guide provides instructions for deploying the AI Analyst application components on macOS.

## Deployment Scripts

The repository includes two deployment scripts for macOS:

1. `push-adk-web.sh`: Deploys the web interface
2. `push-ai-agent.sh`: Deploys the AI agent

### Making Scripts Executable

Before running the deployment scripts, make them executable:

```bash
chmod +x push-adk-web.sh
chmod +x push-ai-agent.sh
```

### Making Scripts Executable

Before running the deployment scripts, make them executable:

```bash
chmod +x push-adk-web.sh
chmod +x push-ai-agent.sh
```

### Deploying Components

1. **Deploy Web Interface**

   ```bash
   ./push-adk-web.sh
   ```

   This script will:

   - Build the ADK web interface Docker image
   - Push it to Google Artifact Registry
   - List available image tags

2. **Deploy AI Agent**
   ```bash
   ./push-ai-agent.sh
   ```
   This script will:
   - Build the AI agent Docker image
   - Push it to Google Artifact Registry
   - List available image tags
