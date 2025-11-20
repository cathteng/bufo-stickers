# 🐸 Bufo iOS Stickers

Automatically generated iOS sticker packs from the [all-the-bufo](https://github.com/knobiknows/all-the-bufo) repository.

**✨ Works with read-only access** - No webhooks or special permissions needed!

## 📥 Download Stickers

### Option 1: Download from Releases (Recommended)
1. Go to the [Releases page](../../releases)
2. Download the latest `ios-stickers.zip` file
3. Extract the zip file to get the `.stickerpack` folder(s)

### Option 2: Download from Artifacts
1. Go to the [Actions tab](../../actions)
2. Click on the latest successful workflow run
3. Download the `ios-stickers` artifact

## 📱 Installation on iOS

### For iMessage Stickers:
1. Transfer the `.stickerpack` folder to your iOS device using:
   - AirDrop
   - Files app (iCloud Drive)
   - Any file transfer method you prefer

2. Use a sticker pack importer app from the App Store, such as:
   - "Sticker Maker Studio"
   - "Sticker.ly"
   - Any compatible sticker pack app

3. Import the sticker pack into the app

4. Access your stickers from iMessage by tapping the App Store icon in iMessage

### Alternative: Create Your Own Sticker App
If you want to create a native iOS sticker app, you can:
1. Download the sticker pack
2. Open Xcode
3. Create a new "Sticker Pack Application"
4. Replace the default stickers with the downloaded ones
5. Build and install on your device

## 🤖 How It Works

This repository automatically:

1. **Monitors the source repository** - Checks all-the-bufo repository weekly for changes
2. **Detects changes** - Only regenerates if new commits are detected (efficient!)
3. **Processes images** - Converts images to iOS sticker format (300-618px, optimized PNG/APNG for animations)
4. **Generates sticker packs** - Creates properly formatted `.stickerpack` directories
5. **Creates releases** - Automatically publishes new releases when stickers are updated
6. **Provides downloads** - Makes sticker packs available as both artifacts and releases

### Automatic Updates

The sticker packs are automatically regenerated:
- **Weekly** - Checks for changes every Sunday and regenerates only if source repo has updates
- **Manually** - Via the GitHub Actions "Run workflow" button for immediate updates
- **No webhook needed** - Works with read-only access to the source repository!

## 🛠️ Technical Details

### Image Processing
- **Static images**: Resized to iOS sticker requirements (408x408px by default)
- **Animated GIFs**: Converted to APNG (Animated PNG) format - iOS supports this!
- Transparent backgrounds are preserved
- Images are optimized to stay under the 500KB limit
- If animations are too large, frame count is automatically reduced
- Output format: PNG/APNG with RGBA color mode

### File Structure
```
output/
  ├── BufoStickers.stickerpack/
  │   ├── Contents.json
  │   ├── sticker_001.png
  │   ├── sticker_002.png
  │   └── ...
  └── ios-stickers.zip
```

## 🔧 Development

### Local Setup

1. Clone this repository:
```bash
git clone https://github.com/YOUR-USERNAME/bufo-stickers.git
cd bufo-stickers
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Clone the source repository:
```bash
git clone https://github.com/knobiknows/all-the-bufo.git source-repo
```

4. Generate stickers:
```bash
python scripts/generate_stickers.py
```

### Customization

You can customize the sticker generation by editing `scripts/generate_stickers.py`:

- **Change sticker size**: Modify the `size` parameter in the `resize_image_for_sticker` function call (options: 'small', 'medium', 'large')
- **Adjust image quality**: Modify the `MAX_FILE_SIZE` constant
- **Create multiple packs**: Modify the grouping logic in the `main` function

## 📝 Configuration

### GitHub Actions Triggers

The workflow runs automatically:

1. **Scheduled**: Every Sunday at midnight UTC, checks for changes in the source repository
2. **Manual**: Click "Run workflow" in the Actions tab for immediate updates
3. **Smart**: Only regenerates stickers if the source repo has actually changed

### Change Check Frequency

Want to check more or less often? Edit `.github/workflows/generate-stickers.yml`:

```yaml
schedule:
  - cron: '0 0 * * 0'  # Every Sunday (current)
  # - cron: '0 0 * * *'  # Once daily
  # - cron: '0 0 */3 * *'  # Every 3 days
  # - cron: '0 0 1 * *'  # Monthly on the 1st
```

### No Setup Required!

This works with **read-only access** to the source repository. You don't need:
- ❌ Webhooks or Personal Access Tokens
- ❌ Access to the source repository settings
- ❌ Forks of the source repository

Just push this repo to GitHub and it works! 🎉

## 📄 License

This project is for generating stickers from the all-the-bufo repository. Please respect the original repository's license and attribution requirements.

## 🙏 Credits

- Source images: [all-the-bufo](https://github.com/knobiknows/all-the-bufo) by knobiknows
- Sticker generation: Automated via GitHub Actions

## 🐛 Issues & Contributions

If you encounter any issues or have suggestions for improvements:

1. Check the [Issues](../../issues) page
2. Create a new issue if needed
3. Pull requests are welcome!

---

Made with 💚 for Bufo enthusiasts 🐸

