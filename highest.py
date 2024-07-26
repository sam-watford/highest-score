import sys
import json
import heapq
import logging
from typing import List, Dict, Tuple

def configure_logging() -> None:
    """Configure logging settings."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_line(line: str) -> Tuple[int, Dict]:
    """
    Process a single line of input and return the score and record.
    
    Args:
        line (str): A line from the input file.
    
    Returns:
        Tuple[int, Dict]: The score and record dictionary.
    
    Raises:
        ValueError: If the line format is incorrect or the record is missing the 'id' field.
    """
    score, record = line.split(': ', 1)
    score = int(score)
    record_dict = json.loads(record)
    if 'id' not in record_dict:
        raise ValueError("Record does not contain an 'id' field.")
    return score, record_dict

def read_records(input_file: str, n: int) -> List[Tuple[int, str]]:
    """
    Read records from the input file and return the top n records.
    
    Args:
        input_file (str): Path to the input file.
        n (int): Number of top records to return.
    
    Returns:
        List[Tuple[int, str]]: List of top n records with scores and ids.
    
    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If a record is missing the 'id' field or the format is incorrect.
    """
    try:
        with open(input_file, 'r') as file:
            min_heap = []
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    score, record_dict = process_line(line)
                    if len(min_heap) < n:
                        heapq.heappush(min_heap, (score, record_dict['id']))
                    else:
                        heapq.heappushpop(min_heap, (score, record_dict['id']))
                except ValueError as e:
                    logging.error(f"Invalid record format: {line}. Error: {e}")
                    raise
        
        return min_heap
    except FileNotFoundError as e:
        logging.error(f"Input file not found: {input_file}. Error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the file. Error: {e}")
        raise

def get_highest_scores(min_heap: List[Tuple[int, str]]) -> List[Dict]:
    """
    Convert the heap of top records into a list of dictionaries.
    
    Args:
        min_heap (List[Tuple[int, str]]): Min-heap of top records.
    
    Returns:
        List[Dict]: List of top records as dictionaries.
    """
    return [{'score': score, 'id': record_id} for score, record_id in sorted(min_heap, reverse=True)]

def main(input_file: str, n: int) -> None:
    """
    Main function to execute the script.
    
    Args:
        input_file (str): Path to the input file.
        n (int): Number of top records to return.
    """
    configure_logging()
    
    try:
        min_heap = read_records(input_file, n)
        top_records = get_highest_scores(min_heap)
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
