# Fileaccess Utility Class

## Introduction
`Fileaccess` is a utility class for safely dealing with files. This class can be used to read, write, or append to a file, as well as create a file or directory.

## Usage
### Reading a File
To read a file, use the `with` statement and specify the file name and mode as the `Fileaccess` class parameters. Here's an example:

```python
with Fileaccess("filename.txt", "r") as file:
    for line in file:
        print(line)
```

### Writing to a File
To write to a file, use the `with` statement and specify the file name and mode as the `Fileaccess` class parameters. Here's an example:

```python
with Fileaccess("filename.txt", "w") as file:
    file.write("Hello World")
```

### Appending to a File
To append to a file, use the `with` statement and specify the file name and mode as the `Fileaccess` class parameters. Here's an example:

```python
with Fileaccess("filename.txt", "a") as file:
    file.write("Hello World")
```

### Creating a File or Directory
To create a file or directory, use the `createFile` method of the `Fileaccess` class. Here's an example:

```python
Fileaccess.createFile(assetType="f", targetPath="/path/to/file.txt", fileContents="File contents")
```

In the above example, `assetType` can be either `"f"` to create a file or `"d"` to create a directory. The `targetPath` parameter specifies the path where the file or directory will be created. The `fileContents` parameter is optional and can be used to specify the contents of the file.
  
Note: You do NOT need to first create the directory path for a file if the directory path doesn't exist (all you need are access permissions for the user python is running as). The full directory path will automatically be create for you simply by you providing a full file path.
  

## File Access Modes
The `mode` parameter in the `Fileaccess` class specifies the file access mode. Here's a table of the available modes:

| Mode | Meaning |
| --- | --- |
| `r` | Open for reading (default) |
| `w` | Open for writing, truncating the file first |
| `x` | Open for exclusive creation, failing if the file already exists |
| `a` | Open for writing, appending to the end of file if it exists |
| `b` | Binary mode |
| `t` | Text mode (default) |
| `+` | Open for updating (reading and writing) |

## Error Handling
If an error occurs while using the `Fileaccess` class, it will be caught and printed to the console. This can be useful for debugging purposes.

## License
This code is licensed under the MIT License. See the `LICENSE` file for more information.
