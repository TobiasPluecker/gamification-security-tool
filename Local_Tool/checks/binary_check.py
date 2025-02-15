import os

def is_binary(file_path):
    """
    Checks if a file is binary by reading the first 1024 bytes.
    """
    try:
        chunk_size = min(8192, os.path.getsize(file_path)) # for large files
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            return b'\0' in chunk  # Binary files often contain null bytes
    except Exception as e:
        print(f"Error checking file: {file_path} - {e}")
        return False

def check_binary_files(files):
    """
    Checks if disallowed binary files are included in the commit.
    Also verifies file extensions against allowed and forbidden lists.
    """
    # Extensions that are allowed (text files and known binary files)
    ALLOWED_EXTENSIONS = [
        # Images and icons
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',  # Bilder
        '.mp3', '.wav', '.ogg',  # Audio
        '.mp4', '.mkv', '.webm',  # Video

        # Documents and tables
        '.pdf', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.ods', '.ppt', '.pptx', '.rtf',

        # code and scripts
        '.c', '.cpp', '.h', '.hpp', '.py', '.rb', '.js', '.ts', '.html', '.css',
        '.json', '.xml', '.yml', '.yaml', '.ini', '.sh', '.bat', '.php', '.java',
        '.cs', '.go', '.rs', '.swift', '.sql',

        # markup and text
        '.md', '.rst', '.txt', '.csv', '.tsv', '.log',

        # Fonts
        '.ttf', '.otf', '.woff', '.woff2',

        # other
        '.db', '.sqlite', '.dat'
    ]

    # Extensions that are explicitly forbidden
    FORBIDDEN_EXTENSIONS = [
        # Executable files
        '.exe', '.dll', '.bin', '.o', '.so', '.class', '.jar', '.msi', '.bat', '.sh', '.cmd',

        # Compressed or bundled executables
        '.apk', '.dmg', '.iso', '.app', '.deb', '.rpm', '.img', '.pkg', '.vmdk',

        # Scripts and macro files (potentially harmful)
        '.ps1', '.vbs', '.js', '.wsf', '.hta',

        # System and configuration files (potentially risky)
        '.sys', '.inf', '.reg', '.ini', '.dat',

        # Other binary files
        '.pyc', '.pyo', '.swf',

        # Other formats rarely needed in repositories
        '.crt', '.pem', '.key', '.der',  # Certificates and key files
        '.tmp', '.bak',  # Temporary and backup files
        '.log'  # Large log files
    ]

    binary_files = []

    for file in files:
        if not os.path.exists(file):
            continue  # Ignore non-existent files

        # Check if the file is binary
        if is_binary(file):
            # Check file extension
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in FORBIDDEN_EXTENSIONS:
                binary_files.append(file)
            elif file_ext not in ALLOWED_EXTENSIONS:
                binary_files.append(file)

    if binary_files:
        return {
            'check': 'binary_files',
            'level': 'ERROR',
            'message': f'Disallowed binary files detected: {", ".join(binary_files)}'
        }

    return None
