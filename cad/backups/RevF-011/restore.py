"""Restore the exact Rev F native/STEP checkpoint from lossless backup parts.

Download the repository ZIP or a checkout including this directory, then run:
    python restore.py
No network access, GitHub token, or Fusion installation is needed to recover
the original files. Fusion is needed to reopen the recovered native design.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def restore(record, parts_dir, output_dir):
    name = record['original_name']
    if Path(name).name != name or name in ('.', '..'):
        raise ValueError('Unsafe original filename in manifest')
    destination = output_dir / name
    if destination.resolve().parent != output_dir.resolve():
        raise ValueError('Destination escapes selected output directory')
    if destination.exists():
        if destination.stat().st_size == record['original_bytes'] and sha256(destination) == record['original_sha256']:
            print('Already verified:', name)
            return
        raise FileExistsError('Existing different file will not be overwritten: ' + str(destination))
    compressed_tmp = restored_tmp = None
    try:
        with tempfile.NamedTemporaryFile(prefix='cbp-backup-', suffix='.gz', dir=output_dir, delete=False) as joined:
            compressed_tmp = Path(joined.name)
            compressed_hash = hashlib.sha256()
            compressed_bytes = 0
            expected_index = 1
            for part in record['parts']:
                if part['index'] != expected_index:
                    raise ValueError('Part order is incomplete for ' + name)
                expected_index += 1
                part_name = Path(part['repository_path']).name
                source = parts_dir / part_name
                if source.resolve().parent != parts_dir.resolve():
                    raise ValueError('Part path escapes selected source directory')
                data = source.read_bytes()
                if len(data) != part['bytes'] or hashlib.sha256(data).hexdigest() != part['sha256']:
                    raise ValueError('Part checksum/size mismatch: ' + part_name)
                identity = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
                if identity != part['git_blob_sha1_expected']:
                    raise ValueError('Git blob identity mismatch: ' + part_name)
                joined.write(data)
                compressed_hash.update(data)
                compressed_bytes += len(data)
        if compressed_bytes != record['compressed_bytes'] or compressed_hash.hexdigest() != record['compressed_sha256']:
            raise ValueError('Joined gzip checksum/size mismatch: ' + name)
        with tempfile.NamedTemporaryFile(prefix='cbp-restored-', suffix='.partial', dir=output_dir, delete=False) as target:
            restored_tmp = Path(target.name)
            with gzip.open(compressed_tmp, 'rb') as source:
                shutil.copyfileobj(source, target)
        if restored_tmp.stat().st_size != record['original_bytes'] or sha256(restored_tmp) != record['original_sha256']:
            raise ValueError('Restored original checksum/size mismatch: ' + name)
        if destination.exists():
            raise FileExistsError('Destination appeared during restore: ' + str(destination))
        restored_tmp.replace(destination)
        restored_tmp = None
        print('Verified and restored:', name, record['original_bytes'], 'bytes')
    finally:
        for temporary in (compressed_tmp, restored_tmp):
            if temporary is not None and temporary.exists():
                temporary.unlink()


def main():
    folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=folder / 'manifest.json')
    parser.add_argument('--parts-dir', type=Path, default=folder)
    parser.add_argument('--output-dir', type=Path, default=folder / 'restored-native')
    parser.add_argument('--file', action='append', dest='names', help='Restore only this original filename; repeat as needed')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
    records = [r for r in manifest['files'] if not args.names or r['original_name'] in args.names]
    if not records:
        raise ValueError('No matching checkpoint files in manifest')
    if args.names and set(args.names) - {r['original_name'] for r in records}:
        raise ValueError('One or more requested files are absent from the manifest')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        restore(record, args.parts_dir.resolve(), args.output_dir.resolve())


if __name__ == '__main__':
    main()
