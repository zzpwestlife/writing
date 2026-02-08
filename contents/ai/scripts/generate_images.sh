#!/bin/bash

# Check API Key
if [ -z "$MODELSCOPE_API_KEY" ]; then
    echo "Error: MODELSCOPE_API_KEY is not set."
    echo "Please export MODELSCOPE_API_KEY='your_key' and try again."
    exit 1
fi

BASE_DIR="/Users/joeyzou/Code/OpenSource/writing"
SCRIPT_PATH="$BASE_DIR/.claude/skills/smart-illustrator/scripts/generate-image.ts"
PROMPTS_DIR="$BASE_DIR/contents/ai/scripts/prompts"
ASSETS_DIR="$BASE_DIR/contents/ai/assets"

echo "Generating Cover..."
npx -y bun "$SCRIPT_PATH" \
  --prompt-file "$PROMPTS_DIR/cover.txt" \
  --output "$ASSETS_DIR/ai_collaboration_stages_cover.png" \
  --aspect-ratio 2.35:1

echo "Generating Stage 1..."
npx -y bun "$SCRIPT_PATH" \
  --prompt-file "$PROMPTS_DIR/stage1.txt" \
  --output "$ASSETS_DIR/stage_1_human_driving.png" \
  --aspect-ratio 4:3

echo "Generating Stage 2..."
npx -y bun "$SCRIPT_PATH" \
  --prompt-file "$PROMPTS_DIR/stage2.txt" \
  --output "$ASSETS_DIR/stage_2_ai_copilot.png" \
  --aspect-ratio 4:3

echo "Generating Stage 3..."
npx -y bun "$SCRIPT_PATH" \
  --prompt-file "$PROMPTS_DIR/stage3.txt" \
  --output "$ASSETS_DIR/stage_3_ai_pilot.png" \
  --aspect-ratio 4:3

echo "Generating Stage 4..."
npx -y bun "$SCRIPT_PATH" \
  --prompt-file "$PROMPTS_DIR/stage4.txt" \
  --output "$ASSETS_DIR/stage_4_auto_pilot.png" \
  --aspect-ratio 4:3

echo "All images generated in $ASSETS_DIR"
