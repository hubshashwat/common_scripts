To create 100 text files with numbers in their content using SFTP, you can use the put command with input redirection. Here's how you can do it:

1. Open a command prompt or terminal window on your local machine.

2. Navigate to the directory where you want to create the files.

3. Run the following command to create 100 files with names file1.txt, file2.txt, file3.txt, and so on up to file100.txt, with the numbers in their content:

     ```for i in {1..100}; do echo "$i" > file$i.txt; done```

This will create 100 text files with the specified names and numbers in their content.

4. Now, open an SFTP connection to the remote server using the sftp command:

      ```sftp user@mock-sftp.dev.co```
Enter your password when prompted.

5. Navigate to the directory on the remote server where you want to upload the files using the cd command. For example, if you want to upload the files to the /upload directory, you would type cd /upload.

6. Use the put command with input redirection to upload the files to the remote server:

    ```put file*.txt```
This command uploads all files in the current local directory with the file*.txt pattern to the remote directory that you navigated to in step 5.

7. Once the files are uploaded, you can check if they have been successfully transferred using the ls command. For example, to list the files in the /upload directory on the SFTP server, you would type:

    ```ls```
This command will display a list of files in the /upload directory on the SFTP server.
