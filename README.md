Apache Multi-Site Setup Script

This script automates the setup of multiple websites on an Apache server, including HTTP and HTTPS configurations. It simplifies the process of creating virtual hosts, obtaining SSL certificates using Let's Encrypt, and ensuring proper configurations for each domain.
Features
•	Automates Apache installation and configuration.
•	Sets up virtual hosts for multiple websites.
•	Creates directories and sample index.html files for each site.
•	Configures SSL certificates with Certbot using the --webroot plugin.
•	Ensures proper SSL paths in virtual host files.
•	Includes error handling and troubleshooting tips.
•	Tests SSL auto-renewal.
Prerequisites
1.	A server running a compatible Linux distribution (e.g., Ubuntu).
2.	A public IP address.
3.	Domains with A/AAAA records pointing to the server's IP.
4.	Sudo privileges on the server.
5.	Python 3 installed.
Usage
1.	Clone the Repository:
2.	git clone <repository-url>
3.	cd <repository-folder>
4.	Run the Script: Execute the script and follow the interactive prompts:
5.	python3 apache_setup_script.py
6.	Input Required Information:
o	Number of sites to set up.
o	Domain names (e.g., example.com).
o	Administrator email for SSL certificates.
7.	Verify Sites:
o	Access the configured sites at http://<domain> and https://<domain>.
Troubleshooting
Common Errors and Fixes
1. Apache Fails to Start
•	Check Apache configuration: 
•	sudo apache2ctl configtest
•	Inspect logs for details: 
•	sudo journalctl -xeu apache2.service
2. SSL Certificate Issues
•	Verify domain DNS configuration.
•	Use the --webroot plugin if the --apache plugin fails: 
•	sudo certbot certonly --webroot -w /var/www/<domain> -d <domain> -d www.<domain>
3. Wrong Content Served
•	Ensure DocumentRoot in the virtual host file points to the correct directory.
•	Clear browser cache or test in incognito mode.
Customization
You can modify the script to:
•	Use different document root paths.
•	Add additional Apache modules.
•	Implement redirects from HTTP to HTTPS.
License
This script is licensed under the MIT License. Feel free to modify and share it.


