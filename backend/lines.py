import requests

def get_x_lines(file_url, x):
    response = requests.get(file_url, stream=True)  # Enable streaming
    
    if response.status_code == 200:
        lines = ""
        line_count = 0
        for line in response.iter_lines(decode_unicode=True):  # Read file line by line
            lines += line + "\n"  # Write each line to file
            line_count += 1
            if line_count >= x:  # Stop after 100 lines
                break
        return lines
    else:
        raise Exception(f"Failed to fetch CSV data. Status code: {response.status_code}")
    

# Example usage
if __name__ == "__main__":
    file_url = "https://archive.org/download/20250128-cdc-datasets/COVID-19_Case_Surveillance_Public_Use_Data.csv"
    lines = get_x_lines(file_url, 100)
    print(lines)
