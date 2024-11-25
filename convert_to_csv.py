import csv
import json

def json_file_to_csv(json_file_path, csv_file_path):
    """
    Chuyển đổi file JSON chứa nhiều bản ghi sang CSV.

    Args:
    - json_file_path (str): Đường dẫn file JSON.
    - csv_file_path (str): Đường dẫn để lưu file CSV.
    """
    # Đọc dữ liệu JSON từ file
    with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)  # Dữ liệu JSON dạng list
    
    # Xác định tiêu đề CSV
    headers = [
        "id", "content", "start_index", "headers",
        "has_code", "has_list", "has_table",
        "has_blockquote", "char_count", "word_count",
        "prev_chunk", "next_chunk"
    ]
    
    # Ghi dữ liệu vào file CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Viết tiêu đề
        writer.writerow(headers)
        
        # Viết từng dòng dữ liệu
        for record in data:
            metadata = record.get("metadata", {})
            writer.writerow([
                record.get("id", ""),
                record.get("content", ""),
                metadata.get("start_index", ""),
                "\n".join(metadata.get("headers", [])),
                metadata.get("has_code", ""),
                metadata.get("has_list", ""),
                metadata.get("has_table", ""),
                metadata.get("has_blockquote", ""),
                metadata.get("char_count", ""),
                metadata.get("word_count", ""),
                metadata.get("prev_chunk", ""),
                metadata.get("next_chunk", "")
            ])

# Đường dẫn file JSON đầu vào và CSV đầu ra
json_file_path = "chunks.json"  # Thay bằng đường dẫn file JSON của bạn
csv_file_path = "chunks.csv"

# Gọi hàm để chuyển đổi
json_file_to_csv(json_file_path, csv_file_path)
print(f"CSV file has been created at '{csv_file_path}'.")