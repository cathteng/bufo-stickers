#!/usr/bin/env python3
"""
Generate iOS sticker packs from images in the all-the-bufo repository.
Supports both static and animated stickers (GIFs converted to APNG).
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image, ImageSequence


# iOS sticker size requirements
STICKER_SIZES = {
    'small': (300, 300),
    'medium': (408, 408),
    'large': (618, 618)
}

# Maximum sticker file size (500KB for iOS)
MAX_FILE_SIZE = 500 * 1024

SOURCE_DIR = Path('source-repo')
OUTPUT_DIR = Path('output')


def create_sticker_pack_structure(pack_name):
    """Create the directory structure for an iOS sticker pack."""
    pack_dir = OUTPUT_DIR / f"{pack_name}.stickerpack"
    pack_dir.mkdir(parents=True, exist_ok=True)
    return pack_dir


def is_animated_gif(image_path):
    """Check if an image is an animated GIF."""
    try:
        with Image.open(image_path) as img:
            if img.format == 'GIF':
                # Try to seek to the second frame
                try:
                    img.seek(1)
                    return True
                except EOFError:
                    return False
    except:
        pass
    return False


def resize_animated_gif(image_path, output_path, size='medium'):
    """
    Resize and convert an animated GIF to APNG for iOS stickers.
    
    Args:
        image_path: Path to source GIF
        output_path: Path to save processed APNG
        size: One of 'small', 'medium', 'large'
    """
    try:
        with Image.open(image_path) as img:
            target_size = STICKER_SIZES[size]
            frames = []
            durations = []
            
            # Process each frame
            for frame in ImageSequence.Iterator(img):
                # Convert to RGBA
                frame = frame.convert('RGBA')
                
                # Resize to fill the sticker size (may crop to maintain aspect ratio)
                frame_aspect = frame.width / frame.height
                target_aspect = target_size[0] / target_size[1]
                
                if frame_aspect > target_aspect:
                    # Frame is wider, scale by height
                    new_height = target_size[1]
                    new_width = int(new_height * frame_aspect)
                else:
                    # Frame is taller, scale by width
                    new_width = target_size[0]
                    new_height = int(new_width / frame_aspect)
                
                frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Crop to exact target size (center crop)
                left = (new_width - target_size[0]) // 2
                top = (new_height - target_size[1]) // 2
                frame = frame.crop((left, top, left + target_size[0], top + target_size[1]))
                
                frames.append(frame)
                # Get frame duration (default to 100ms if not specified)
                durations.append(img.info.get('duration', 100))
            
            # Save as APNG (animated PNG) - iOS supports this format
            frames[0].save(
                output_path,
                'PNG',
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,  # Loop forever
                optimize=True
            )
            
            # Check file size
            if os.path.getsize(output_path) > MAX_FILE_SIZE:
                # If too large, reduce frame count
                print(f"  ⚠️  Animation too large, reducing frames...")
                # Keep every other frame
                reduced_frames = frames[::2]
                reduced_durations = [d * 2 for d in durations[::2]]
                
                reduced_frames[0].save(
                    output_path,
                    'PNG',
                    save_all=True,
                    append_images=reduced_frames[1:],
                    duration=reduced_durations,
                    loop=0,
                    optimize=True,
                    compress_level=9
                )
            
            return True
    except Exception as e:
        print(f"  ❌ Error processing animated GIF {image_path}: {e}")
        return False


def resize_image_for_sticker(image_path, output_path, size='medium'):
    """
    Resize and optimize an image for iOS stickers.
    Handles both static images and animated GIFs.
    
    Args:
        image_path: Path to source image
        output_path: Path to save processed image
        size: One of 'small', 'medium', 'large'
    """
    # Check if it's an animated GIF
    if is_animated_gif(image_path):
        print(f"  🎬 Animated GIF detected - converting to APNG")
        return resize_animated_gif(image_path, output_path, size)
    
    # Process static image
    try:
        with Image.open(image_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get target size
            target_size = STICKER_SIZES[size]
            
            # Resize to fill the sticker size (may crop to maintain aspect ratio)
            img_aspect = img.width / img.height
            target_aspect = target_size[0] / target_size[1]
            
            if img_aspect > target_aspect:
                # Image is wider, scale by height
                new_height = target_size[1]
                new_width = int(new_height * img_aspect)
            else:
                # Image is taller, scale by width
                new_width = target_size[0]
                new_height = int(new_width / img_aspect)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to exact target size (center crop)
            left = (new_width - target_size[0]) // 2
            top = (new_height - target_size[1]) // 2
            new_img = img.crop((left, top, left + target_size[0], top + target_size[1]))
            
            # Save with optimization
            new_img.save(output_path, 'PNG', optimize=True)
            
            # Check file size and reduce quality if needed
            if os.path.getsize(output_path) > MAX_FILE_SIZE:
                # If too large, try saving with compression
                new_img.save(output_path, 'PNG', optimize=True, compress_level=9)
            
            return True
    except Exception as e:
        print(f"  ❌ Error processing {image_path}: {e}")
        return False


def create_contents_json(pack_dir, sticker_files):
    """
    Create Contents.json file for the sticker pack.
    This is required for iOS sticker packs.
    """
    contents = {
        "info": {
            "version": 1,
            "author": "Generated from all-the-bufo"
        },
        "stickers": []
    }
    
    for sticker_file in sticker_files:
        contents["stickers"].append({
            "filename": sticker_file.name
        })
    
    contents_path = pack_dir / "Contents.json"
    with open(contents_path, 'w') as f:
        json.dump(contents, f, indent=2)


def find_images(directory):
    """Find all image files in a directory."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    images = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                images.append(Path(root) / file)
    
    return images


def main():
    """Main function to generate iOS sticker packs."""
    print("🐸 Starting Bufo sticker pack generation...")
    
    # Check if source directory exists
    if not SOURCE_DIR.exists():
        print(f"❌ Source directory {SOURCE_DIR} not found!")
        return
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Find all images in source repo
    images = find_images(SOURCE_DIR)
    
    if not images:
        print("❌ No images found in source repository!")
        return
    
    print(f"📸 Found {len(images)} images")
    
    # Group images by subdirectory or create single pack
    # For simplicity, we'll create one main pack
    pack_name = "BufoStickers"
    pack_dir = create_sticker_pack_structure(pack_name)
    
    print(f"📦 Creating sticker pack: {pack_name}")
    
    sticker_files = []
    processed_count = 0
    
    for idx, image_path in enumerate(images, 1):
        print(f"Processing {idx}/{len(images)}: {image_path.name}")
        
        # Use original filename but ensure .png extension
        original_name = image_path.stem  # filename without extension
        output_filename = f"{original_name}.png"
        output_path = pack_dir / output_filename
        
        # Process the image
        if resize_image_for_sticker(image_path, output_path, size='medium'):
            sticker_files.append(output_path)
            processed_count += 1
    
    print(f"✅ Processed {processed_count}/{len(images)} images")
    
    # Create Contents.json
    create_contents_json(pack_dir, sticker_files)
    
    print(f"✅ Sticker pack created: {pack_dir}")
    print(f"📊 Total stickers: {len(sticker_files)}")
    print("\n🎉 Sticker generation complete!")
    
    # Create a simple README in the output directory
    readme_path = OUTPUT_DIR / "README.txt"
    with open(readme_path, 'w') as f:
        f.write("Bufo iOS Stickers\n")
        f.write("=================\n\n")
        f.write(f"Total stickers: {len(sticker_files)}\n")
        f.write(f"Generated from: https://github.com/knobiknows/all-the-bufo\n\n")
        f.write("Installation Instructions:\n")
        f.write("1. Transfer the .stickerpack folder to your iOS device\n")
        f.write("2. Use a compatible app to import the stickers\n")
        f.write("3. Enjoy your Bufo stickers! 🐸\n")


if __name__ == "__main__":
    main()

