import pytsk3
import sys
import argparse
import os

def list_files(img, keyword=None):
    """Traverse and list all files (including deleted ones)."""
    fs = pytsk3.FS_Info(img)
    directory = fs.open_dir("/")
    print("[+] Scanning files...")

    for entry in directory:
        if not hasattr(entry, "info") or not entry.info.name.name:
            continue

        try:
            name = entry.info.name.name.decode("utf-8")
        except UnicodeDecodeError:
            name = str(entry.info.name.name)

        is_deleted = entry.info.meta and entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC
        status = "[DELETED]" if is_deleted else "[OK]"

        print(f"{status} {name}")

        # Keyword search in file name
        if keyword and keyword.lower() in name.lower():
            print(f"    -> Keyword match in filename: {name}")

def search_keywords(img, keyword):
    """Search for keyword in raw image data (string search)."""
    print(f"[+] Searching for keyword '{keyword}' in raw image...")
    offset = 0
    found = False

    while True:
        data = img.read_random(offset, 4096)  # Read in chunks
        if not data:
            break
        if keyword.encode() in data:
            print(f"[FOUND] Keyword '{keyword}' at offset: {offset}")
            found = True
        offset += 4096

    if not found:
        print("[-] No keyword matches found.")

def main():
    parser = argparse.ArgumentParser(description="Disk Image Analyzer (Basic)")
    parser.add_argument("image", help="Path to disk image (.dd)")
    parser.add_argument("-k", "--keyword", help="Keyword to search for")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"[-] File {args.image} not found!")
        sys.exit(1)

    try:
        img = pytsk3.Img_Info(url=args.image)
    except IOError as e:
        print(f"[-] Could not open image: {e}")
        sys.exit(1)

    list_files(img, keyword=args.keyword)

    if args.keyword:
        search_keywords(img, args.keyword)

if __name__ == "__main__":
    main()
