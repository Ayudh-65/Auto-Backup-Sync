# Auto-Backup-Sync
Socket-based python application to automate scheduled backups.

A CLI application that automates scheduled file backups to server at fixed intervals.
It can sync live file data at server through seamless, scheduled backups with custom intervals.

## Usage

- Run the client and server scripts on the respective host (currently configured to work on localhost as server). <br /><br />
```$python3 server.py``` and ```$python3 client.py```<br /><br />
- Client application will prompt you to enter the file path.<br />
- Client application will then connect to the server, and a copy of your file will be created at the server's directory.<br />
- File will automatically sync all changes to the server copy every 'n' seconds (given as input).<br />
- Close the client and server scripts manually using ```ctrl+c```
