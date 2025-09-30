#!/bin/bash
# ----------------------------------------
# Shell Script: push-adk-web.sh
# Builds and pushes adk-web image to Google Artifact Registry using OAuth2
# ----------------------------------------

# Configurable values
SERVICE_NAME="adk-web"
IMAGE_TAG="asia-south1-docker.pkg.dev/ai-analyst-for-startup-eval/ai-analyst-ui/adk-web:latest"
REGISTRY="asia-south1-docker.pkg.dev"
PROJECT_ID="ai-analyst-for-startup-eval"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "\n${CYAN}[Step 1] Checking for gcloud CLI...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo -e "\n${YELLOW}[Info] gcloud CLI not found. Please install it using:${NC}"
    echo "brew install --cask google-cloud-sdk"
    echo -e "\n${YELLOW}[Info] After installation, restart this script.${NC}"
    exit 1
fi

echo -e "\n${CYAN}[Step 2] Verifying gcloud login...${NC}"
ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
if [ -z "$ACCOUNT" ]; then
    echo -e "\n${YELLOW}[Info] No active account found. Launching login flow...${NC}"
    gcloud auth login
    ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
    if [ -z "$ACCOUNT" ]; then
        echo -e "\n${RED}[Error] Login failed. Cannot proceed.${NC}"
        exit 1
    fi
fi

echo -e "\n${CYAN}[Step 3] Setting project...${NC}"
if ! gcloud config set project "$PROJECT_ID"; then
    echo -e "\n${RED}[Error] Failed to set project.${NC}"
    exit 1
fi

echo -e "\n${CYAN}[Step 4] Authenticating Docker with OAuth2 token...${NC}"
TOKEN=$(gcloud auth print-access-token)
if [ -z "$TOKEN" ]; then
    echo -e "\n${RED}[Error] Failed to retrieve access token.${NC}"
    exit 1
fi

if ! echo "$TOKEN" | docker login -u oauth2accesstoken --password-stdin "https://$REGISTRY"; then
    echo -e "\n${RED}[Error] Docker login failed.${NC}"
    exit 1
fi

echo -e "\n${CYAN}[Step 5] Building and pushing multi-architecture image using docker buildx bake...${NC}"

if ! docker buildx version &> /dev/null; then
    echo -e "\n${YELLOW}[Info] docker buildx not found. Creating a builder instance...${NC}"
    if ! docker buildx create --use --name mybuilder; then
        echo -e "\n${RED}[Error] Failed to create docker buildx builder.${NC}"
        exit 1
    fi
fi

if ! docker buildx bake $SERVICE_NAME --push; then
    echo -e "\n${RED}[Error] Docker bake failed to build and push image.${NC}"
    exit 1
fi

echo -e "\n${GREEN}[Success] Multi-architecture image pushed successfully to Artifact Registry!${NC}"

echo -e "\n${CYAN}[Step 6] Listing image tags...${NC}"
gcloud artifacts docker tags list asia-south1-docker.pkg.dev/ai-analyst-for-startup-eval/ai-analyst-ui/adk-web