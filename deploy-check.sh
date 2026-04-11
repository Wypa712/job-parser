#!/bin/bash
# Deployment script for GitHub Actions

echo "🚀 Job Parser - GitHub Actions Deployment Checklist"
echo "======================================================"
echo ""

# 1. Check if .env is configured
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials"
    exit 1
fi

# 2. Validate .env has required variables
check_env_var() {
    if ! grep -q "^$1=" .env || grep "^$1=$" .env > /dev/null; then
        echo "❌ Missing or empty: $1"
        return 1
    fi
    return 0
}

REQUIRED_VARS=("GROQ_API_KEY" "TELEGRAM_BOT_TOKEN" "TELEGRAM_CHAT_ID")
MISSING_VARS=0

for var in "${REQUIRED_VARS[@]}"; do
    if ! check_env_var "$var"; then
        MISSING_VARS=$((MISSING_VARS + 1))
    else
        echo "✅ $var is configured"
    fi
done

if [ $MISSING_VARS -gt 0 ]; then
    echo ""
    echo "❌ Please configure all required variables in .env"
    exit 1
fi

# 3. Check Python version
python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "✅ Python version: $python_version"

# 4. Validate dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# 5. Test run
echo ""
echo "🧪 Running test check..."
python main.py test

if [ $? -eq 0 ]; then
    echo "✅ Test passed successfully"
else
    echo "❌ Test failed"
    exit 1
fi

echo ""
echo "======================================================"
echo "✅ All checks passed! Ready for deployment"
echo ""
echo "📋 Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Go to GitHub repo → Settings → Secrets and variables → Actions"
echo "3. Add secrets: GROQ_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID"
echo "4. Go to Actions tab and verify workflow"
echo ""
