import sys
import json
import heapq
import logging
from typing import List, Dict

def configure_logging() -> None:
    """Configure logging settings."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_records(input_file: str) -> List[Dict]:
    """
    Read records from the input file.
    
    Args:
        input_file (str): Path to the input file.
    
    Returns:
        List[Dict]: List of records with scores and ids.
    
    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If a record is missing the 'id' field or the format is incorrect.
    """
    try:
        with open(input_file, 'r') as file:
            records = []
            for line in file:
                line = line.strip()
                if not line:
                    # Ignore empty lines
                    continue
                
                try:
                    score, record = line.split(': ', 1)
                    score = int(score)
                    record_dict = json.loads(record)
                    if 'id' in record_dict:
                        records.append((score, record_dict['id']))
                    else:
                        raise ValueError("Record does not contain an 'id' field.")
                except ValueError as e:
                    logging.error(f"Invalid record format: {line}. Error: {e}")
                    raise

            return records
    except FileNotFoundError as e:
        logging.error(f"Input file not found: {input_file}. Error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the file. Error: {e}")
        raise

def get_highest_scores(records: List[Dict], n: int) -> List[Dict]:
    """
    Get the top n records with the highest scores.
    
    Args:
        records (List[Dict]): List of records with scores and ids.
        n (int): Number of top records to return.
    
    Returns:
        List[Dict]: List of top n records.
    """
    top_records = heapq.nlargest(n, records)
    return [{'score': score, 'id': record_id} for score, record_id in top_records]

def main(input_file: str, n: int) -> None:
    """
    Main function to execute the script.
    
    Args:
        input_file (str): Path to the input file.
        n (int): Number of top records to return.
    """
    configure_logging()
    
    try:
        records = read_records(input_file)
        top_records = get_highest_scores(records, n)
        print(json.dumps(top_records, indent=5))
    except FileNotFoundError:
        sys.exit(1)
    except ValueError:
        sys.exit(2)
    except Exception as e:
        logging.critical(f"Critical error: {e}")
        sys.exit(3)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python <source>.py <input_file> <n>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        n = int(sys.argv[2])
        if n <= 0:
            raise ValueError("The number of top records must be greater than 0.")
    except ValueError as e:
        print(f"Invalid number of top records: {e}")
        sys.exit(1)

    main(input_file, n)
