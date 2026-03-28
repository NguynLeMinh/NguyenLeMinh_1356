import hashlib

def calculate_sha256_hash(data):
    sha256_hash = hashlib.sha256()
    
    sha256_hash.update(data.encode('utf-8'))
    
    return sha256_hash.hexdigest()

if __name__ == "__main__":

    data_to_hash = input("Nhập dữ liệu để băm bằng SHA-256: ")

    hash_value = calculate_sha256_hash(data_to_hash)

    print("Giá trị hash SHA-256:", hash_value)