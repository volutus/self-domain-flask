# Self-Domain Setup Documentation

## Initial Setup
For the most part, I followed [this guide that was created for Ubuntu with minor tweaks.](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04)

I had a few issues due to bad configuration setup, but the only one that wasn't addressed by the guide was fixed [by the following StackOverflow comment.](https://stackoverflow.com/a/69992384)

The issue was caused by the nginx user being set to the www-data group by default and being unable to access the flask.sock file because it's owned by the flask group. I moved the nginx user into the flask group which fixed the issue.

`sudo sed -i 's/user www-data;/user flask;/' /etc/nginx/nginx.conf`

## Initial TLS Setup (Certbot)
The SSL/TLS setup was particularly trivial. Using certbot, I was able to put a LetsEncrypt cert on the domain within a few minutes.

This is addressed in the DigitalOcean guide above, but [this specific guide from F5 is useful as well.](https://www.f5.com/company/blog/nginx/using-free-ssltls-certificates-from-lets-encrypt-with-nginx)

## Cloudflare
Afterwards, I opted to add the domain to Cloudflare via their free plan. I added the domain, changed the nameservers at my registrar (Namecheap), and removed the cert in certbot with `sudo certbot delete`. 

I also had to remove the HTTP -> HTTPS redirect which I did by restoring the nginx configuration file in sites-available to the original one from the Digital Ocean setup guide.

## CI/CD 
I did some cleanup on the scripts by moving them into their own folder and creating a deployment script (deploy.sh).

This required some administrative work on the system side. I added the following to a new file (flask-rules) inside the `/etc/sudoers.d` directory

```bash
flask ALL= NOPASSWD: /bin/systemctl restart flask.service
flask ALL= NOPASSWD: /bin/systemctl stop flask.service
flask ALL= NOPASSWD: /bin/systemctl start flask.service
```

This system is also using policy kit so I had to implement an additional file for that.
The file is stored at `/etc/polkit-1/localauthority/50-local.d/manage-units.pkla` and has the following contents.

```bash
[Allow users to manage services]
Identity=unix-group:flask
Action=org.freedesktop.systemd1.manage-units
ResultActive=yes
```
Even with these rules, I have to target the service by its full name which is a bit odd, but this setup allows me to automatically restart the Flask service without needing credentials. As a result, it could be automated if desired.

## Docker
At this point, I wanted to test a Docker setup, so I installed the Docker engine [using the standard guide from Docker](https://docs.docker.com/engine/install/debian/). 

The goal is to reach a setup similar to the [one in this example repo.](https://github.com/docker/awesome-compose/tree/master/nginx-wsgi-flask)

## Postgres

I found that a database was going to be a requirement and not an option based on the applications I want to implement, so I added a Postgres DB to the VPS via Docker.

```Dockerfile
docker pull postgres:alpine
docker run --name postgres-flask -e POSTGRES_PASSWORD=%PASS% -e PGPORT=%RANDOM_PORT% -p %RANDOM_PORT%:%RANDOM_PORT% -d postgres:alpine
```

Afterwards, I added a Firewall exception in the VPS console for the random port I selected. This rule is also IP-restricted, but you (or I) may encounter issues with CGNAT when opting for this additional layer of security.

To confirm that the installation was working, I used DBeaver to connect to my database and confirmed that it was able to connect as expected.
