"""
Automated NSFW Dataset Downloader
Downloads 60GB of training data from the nsfw_data_scraper project
"""

import os
import urllib.request
import time
from pathlib import Path
import glob

def download_from_url_file(url_file, output_dir, max_images=2000):
    """Download images from a text file containing URLs"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    if not os.path.exists(url_file):
        print(f'⚠ File not found: {url_file}')
        return 0
    
    print(f'\n{"="*60}')
    print(f'Processing: {os.path.basename(url_file)}')
    print(f'Output: {output_dir}')
    
    with open(url_file, 'r', encoding='utf-8', errors='ignore') as f:
        urls = [line.strip() for line in f if line.strip() and line.startswith('http')]
    
    # Limit to max_images
    urls = urls[:max_images]
    
    print(f'Found {len(urls)} URLs (limited to {max_images})')
    print(f'{"="*60}')
    
    downloaded = 0
    failed = 0
    
    for i, url in enumerate(urls):
        if i % 50 == 0:
            print(f'Progress: {i}/{len(urls)} | Success: {downloaded} | Failed: {failed}')
        
        try:
            # Extract filename from URL
            filename = url.split('/')[-1].split('?')[0]
            if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                filename = f'image_{i}.jpg'
            
            output_path = os.path.join(output_dir, filename)
            
            # Skip if already downloaded
            if os.path.exists(output_path):
                downloaded += 1
                continue
            
            # Download with timeout
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                with open(output_path, 'wb') as f:
                    f.write(data)
            
            downloaded += 1
            time.sleep(0.02)  # Faster download
            
        except Exception as e:
            failed += 1
            if i % 50 == 0:
                print(f'  Error: {str(e)[:50]}...')
    
    print(f'\n✓ Complete: {downloaded} downloaded, {failed} failed')
    return downloaded

def main():
    base_dir = r'c:\Users\Shado\Downloads\Detection-of-Sensitive-Data-Exposure-in-Images-main\Detection-of-Sensitive-Data-Exposure-in-Images-main\webapp\public'
    scraper_dir = os.path.join(base_dir, 'nsfw_data_scraper')
    raw_data_dir = os.path.join(scraper_dir, 'raw_data')
    output_dir = os.path.join(scraper_dir, 'data', 'train')
    
    print('=' * 60)
    print('NSFW DATASET DOWNLOADER')
    print('=' * 60)
    print(f'Source: {raw_data_dir}')
    print(f'Output: {output_dir}')
    print('\nThis will download ~60GB of images (several hours)')
    print('Press Ctrl+C to stop at any time\n')
    
    # Custom limits per category
    categories = {
        'porn/urls_porn.txt': ('porn', 2000),
        'hentai/urls_hentai.txt': ('hentai', 600),
        'sexy/urls_sexy.txt': ('sexy', 2000),
        'neutral/urls_neutral.txt': ('neutral', 2000),
        'drawings/urls_drawings.txt': ('drawings', 2000)
    }
    
    total_downloaded = 0
    start_time = time.time()
    
    for url_file, (category, limit) in categories.items():
        url_path = os.path.join(raw_data_dir, url_file)
        output_path = os.path.join(output_dir, category)
        
        print(f'\n\n{"#"*60}')
        print(f'CATEGORY: {category.upper()} (limit: {limit} images)')
        print(f'{"#"*60}')
        
        count = download_from_url_file(url_path, output_path, max_images=limit)
        total_downloaded += count
        
        elapsed = time.time() - start_time
        print(f'\nElapsed time: {elapsed/3600:.1f} hours')
        print(f'Total downloaded so far: {total_downloaded:,} images')
    
    print('\n' + '='*60)
    print('DOWNLOAD COMPLETE!')
    print('='*60)
    print(f'Total images: {total_downloaded:,}')
    print(f'Total time: {(time.time() - start_time)/3600:.1f} hours')
    print(f'Output directory: {output_dir}')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n⚠ Download interrupted by user')
        print('You can restart this script to resume from where it left off')
