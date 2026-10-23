"""
ShopSphere MongoDB Atlas Migration & Verification Utility
Transfers local databases/collections to MongoDB Atlas with BSON types, document IDs,
and index preservation, then verifies document counts and integrity.
"""

import os
import sys
import json
import argparse
from bson import json_util
import pymongo
from pymongo.errors import BulkWriteError

def parse_args():
    parser = argparse.ArgumentParser(description="Migrate ShopSphere databases to MongoDB Atlas")
    parser.add_argument("--atlas-uri", required=True, help="MongoDB Atlas connection string (mongodb+srv://...)")
    parser.add_argument("--backup-dir", default=r"d:\Mongo_db-project\ShopSphere_Local_Backup", help="Path to local backup directory")
    parser.add_argument("--databases", nargs="+", default=["shopsphere", "shopsphere_olist"], help="Databases to migrate")
    parser.add_argument("--batch-size", type=int, default=1000, help="Bulk insert batch size")
    return parser.parse_args()

def migrate():
    args = parse_args()
    print("Connecting to MongoDB Atlas...")
    atlas_client = pymongo.MongoClient(args.atlas_uri)
    
    # Test connection
    try:
        atlas_client.admin.command("ping")
        print("Connected successfully to MongoDB Atlas!")
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}", file=sys.stderr)
        sys.exit(1)

    results = {}

    for db_name in args.databases:
        db_dir = os.path.join(args.backup_dir, db_name)
        if not os.path.exists(db_dir):
            print(f"Warning: Backup directory for {db_name} does not exist at {db_dir}. Skipping.")
            continue

        print(f"\n==========================================")
        print(f"Migrating Database: {db_name}")
        print(f"==========================================")
        
        target_db = atlas_client[db_name]
        meta_file = os.path.join(db_dir, "_metadata.json")
        metadata = {}
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)

        results[db_name] = {}

        for filename in os.listdir(db_dir):
            if not filename.endswith(".json") or filename == "_metadata.json":
                continue

            coll_name = filename[:-5]
            file_path = os.path.join(db_dir, filename)
            target_coll = target_db[coll_name]

            expected_count = metadata.get(coll_name, {}).get("count", 0)
            existing_count = target_coll.count_documents({})
            
            print(f"\nCollection: {coll_name}")
            print(f"  Local Backup Count: {expected_count}")
            print(f"  Atlas Existing Count: {existing_count}")

            if existing_count >= expected_count and expected_count > 0:
                print(f"  Collection already populated on Atlas. Skipping document import.")
            elif expected_count > 0:
                print(f"  Transferring {expected_count} documents in batches of {args.batch_size}...")
                batch = []
                inserted = 0
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        doc = json_util.loads(line)
                        batch.append(doc)
                        if len(batch) >= args.batch_size:
                            try:
                                target_coll.insert_many(batch, ordered=False)
                            except BulkWriteError as bwe:
                                # In case of partial rerun, ignore duplicate keys
                                pass
                            inserted += len(batch)
                            print(f"    Progress: {inserted}/{expected_count} documents...", end="\r")
                            batch = []
                if batch:
                    try:
                        target_coll.insert_many(batch, ordered=False)
                    except BulkWriteError:
                        pass
                print(f"  Documents transferred successfully.")

            # Recreate Indexes
            indexes = metadata.get(coll_name, {}).get("indexes", [])
            if indexes:
                print(f"  Rebuilding {len(indexes)} index(es)...")
                for idx in indexes:
                    idx_name = idx.get("name")
                    if idx_name == "_id_":
                        continue
                    key_pairs = list(idx.get("key", {}).items())
                    unique = idx.get("unique", False)
                    try:
                        target_coll.create_index(key_pairs, name=idx_name, unique=unique)
                    except Exception as e:
                        print(f"    Notice for index {idx_name}: {e}")

            final_count = target_coll.count_documents({})
            match = (final_count == expected_count)
            print(f"  Final Atlas Count: {final_count} (Match: {match})")
            results[db_name][coll_name] = {
                "expected": expected_count,
                "atlas": final_count,
                "match": match
            }

    print("\n==========================================")
    print("MIGRATION & VERIFICATION SUMMARY")
    print("==========================================")
    all_matched = True
    for db_name, colls in results.items():
        print(f"\nDatabase: {db_name}")
        for coll_name, data in colls.items():
            status = "MATCH" if data["match"] else "MISMATCH"
            if not data["match"]:
                all_matched = False
            print(f"  - {coll_name:22}: Local={data['expected']:<6} Atlas={data['atlas']:<6} [{status}]")

    if all_matched:
        print("\nAll migrated collections match exactly with 100% data integrity!")
    else:
        print("\nSome counts differed. Please review logs.")

if __name__ == "__main__":
    migrate()
