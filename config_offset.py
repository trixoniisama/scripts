import sys

def apply_offset(file_path, offset):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        if not content.startswith("ForceKeyFrames : "):
            print("The file does not contain the expected format.")
            return

        prefix = "ForceKeyFrames : "
        frame_numbers = content[len(prefix):].strip().split(',')

        offset = int(offset)
        updated_frame_numbers = [
            f"{int(num[:-1]) + offset}f" for num in frame_numbers if int(num[:-1]) >= abs(offset) or offset > 0
        ]

        updated_content = prefix + ','.join(updated_frame_numbers)

        with open(file_path, 'w') as file:
            file.write(updated_content)

        print("The file has been updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py path/to/file.config offset")
    else:
        file_path = sys.argv[1]
        offset = sys.argv[2]
        apply_offset(file_path, offset)

