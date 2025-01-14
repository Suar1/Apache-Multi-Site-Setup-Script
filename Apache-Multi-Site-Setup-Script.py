import os
import subprocess

def run_command(command):
    """Run a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Gather Inputs
print("Welcome to the Apache Multi-Site Setup Wizard!")

# Ask how many sites to set up
while True:
    try:
        site_count = int(input("How many sites do you want to set up? Enter a number: ").strip())
        if site_count > 0:
            break
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

domains = []
for i in range(site_count):
    domain = input(f"Enter the domain name for site {i + 1} (e.g., suar.services): ").strip()
    if domain:
        domains.append(domain)

email = input("Enter the email address for SSL certificates (e.g., info@suar.services): ").strip()

# Install Apache and Certbot
print("\nInstalling Apache and required tools...")
run_command("sudo apt update")
run_command("sudo apt install -y apache2 certbot python3-certbot-apache")

# Enable Apache Modules
print("\nEnabling necessary Apache modules...")
run_command("sudo a2enmod ssl")
run_command("sudo a2enmod rewrite")

# Create Directories and Configuration Files
for domain in domains:
    print(f"\nSetting up {domain}...")

    # Create directory for the website
    web_root = f"/var/www/{domain}"
    run_command(f"sudo mkdir -p {web_root}")
    run_command(f"sudo chown -R $USER:$USER {web_root}")

    # Add sample index.html
    index_file = f"{web_root}/index.html"
    with open(index_file, "w") as f:
        f.write(f"<h1>Welcome to {domain}</h1>")
    run_command(f"sudo chmod 644 {index_file}")

    # Create virtual host file
    conf_file = f"/etc/apache2/sites-available/{domain}.conf"
    with open(conf_file, "w") as f:
        f.write(f"""<VirtualHost *:80>
    ServerAdmin {email}
    ServerName {domain}
    ServerAlias www.{domain}
    DocumentRoot {web_root}

    ErrorLog ${{APACHE_LOG_DIR}}/{domain}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{domain}_access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerAdmin {email}
    ServerName {domain}
    ServerAlias www.{domain}
    DocumentRoot {web_root}

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/{domain}/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/{domain}/privkey.pem

    ErrorLog ${{APACHE_LOG_DIR}}/{domain}_error.log
    CustomLog ${{APACHE_LOG_DIR}}/{domain}_access.log combined
</VirtualHost>
""")
    run_command(f"sudo chmod 644 {conf_file}")

    # Enable the site
    run_command(f"sudo a2ensite {domain}.conf")

# Restart Apache
print("\nRestarting Apache...")
run_command("sudo systemctl restart apache2")

# Obtain SSL Certificates
print("\nObtaining SSL certificates...")
for domain in domains:
    print(f"Processing certificate for {domain}...")
    run_command(f"sudo certbot certonly --webroot -w /var/www/{domain} -d {domain} -d www.{domain}")

# Update Virtual Host Files with SSL Paths
for domain in domains:
    print(f"Updating virtual host file for {domain} to include SSL certificates...")
    conf_file = f"/etc/apache2/sites-available/{domain}.conf"
    with open(conf_file, "r") as f:
        config = f.read()

    ssl_config = f"""
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/{domain}/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/{domain}/privkey.pem
    """

    config = config.replace("SSLEngine on\n", ssl_config)

    with open(conf_file, "w") as f:
        f.write(config)

# Restart Apache After SSL Configuration
print("\nRestarting Apache to apply SSL changes...")
run_command("sudo systemctl restart apache2")

# Test SSL Auto-Renewal
print("\nTesting SSL certificate auto-renewal...")
run_command("sudo certbot renew --dry-run")

# Final Message
print("\nSetup Complete! Your websites are now available at:")
for domain in domains:
    print(f"- http://{domain}")
    print(f"- https://{domain}")
