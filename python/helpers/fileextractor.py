import gzip
import csv

# class to extract csv.gz files
# Use-case: extracting byStation Files

class FileExtractor:

    def extract_file(compressed_file):
        if compressed_file:
            try:
                with gzip.open(compressed_file, "rt", encoding="utf-8") as decompressed_file:
                    csv_reader = csv.reader(decompressed_file)
                    return list(csv_reader)
            except Exception as e:
                print(f"ExtractionError: {e}")
                return None
            return None