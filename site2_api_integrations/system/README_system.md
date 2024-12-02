# Running GUnicorn as a service

Create a .service file for your Gunicorn application under /etc/systemd/system.

For example, if your app is called myapp, create the file /etc/systemd/system/myapp.service

```
[Unit]
Description=Gunicorn instance to serve MyApp
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/your/venv/bin/gunicorn -w 3 -b 0.0.0.0:8000 wsgi:app

[Install]
WantedBy=multi-user.target
```

## Explanation of the Service File

- User and Group: Specifies the user and group under which the Gunicorn process will run (e.g., www-data or nobody for security). Avoid running as root.
- WorkingDirectory: Path to your application's working directory.
- ExecStart: Specifies the command to start Gunicorn. Replace:
    - /path/to/your/venv/bin/gunicorn with the path to your Gunicorn binary (if using a virtual environment, use its path).
    - -w 3: Number of worker processes.
    - -b 0.0.0.0:8000: Bind Gunicorn to all network interfaces on port 8000.
    - wsgi:app: Your app's entry point. Replace wsgi:app with the module and application name (e.g., app:app if your app is named app.py).

#### Reload Systemd and Start the Service

```
sudo systemctl daemon-reload
```

#### Start the Gunicorn service:

```
sudo systemctl start myapp
```

#### Enable it to start on boot:

```
sudo systemctl enable myapp
```