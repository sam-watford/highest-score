import sys
import json
import heapq

def get_highest_scores(input_file, n):
    try:
        with open(input_file, 'r') as file:
            records = []
            for line in file:
                line = line.strip()
                if not line:
                    # Ignore empty lines
                    continue
                
                score, record = line.split(': ', 1)
                score = int(score)
                record_dict = json.loads(record)
                if 'id' in record_dict:
                    records.append((score, record_dict['id']))
                else:
                    # Raise an exception for records without an 'id' field
                    raise ValueError("Record does not contain an 'id' field.")

            top_records = heapq.nlargest(n, records)

            return [{'score': score, 'id': record_id} for score, record_id in top_records]
    except FileNotFoundError:
        # Exit with code 1 if the input file is not found
        print("Error: Input file not found.")
        exit(1)
    except ValueError as e:
        # Exit with code 2 if the input file is invalid
        print(f"Error: {e}")
        exit(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python <source>.py <input_file> <n>")
        exit(1)

    input_file = sys.argv[1]
    n = int(sys.argv[2])

    result = get_highest_scores(input_file, n)
    print(json.dumps(result, indent=5))
