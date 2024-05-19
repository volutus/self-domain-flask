# Self-Domain Setup Documentation

## Initial Setup
For the most part, I followed [this guide that was created for Ubuntu with minor tweaks.](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04)

I had a few issues due to bad configuration setup, but the only one that wasn't addressed by the guide was fixed [by the following StackOverflow comment.](https://stackoverflow.com/a/69992384)

The issue was caused by the nginx user being set to the www-data group by default and being unable to access the flask.sock file because it's owned by the flask group. I moved the nginx user into the flask group which fixed the issue.

`sudo sed -i 's/user www-data;/user flask;/' /etc/nginx/nginx.conf`

## Initial TLS Setup (Certbot)
The SSL/TLS setup was particularly trivial. Using certbot, I was able to put a LetsEncrypt cert on the domain within a few minutes.

## Cloudflare
Afterwards, I opted to add the domain to Cloudflare via their free plan. I added the domain, changed the nameservers at my registrar (Namecheap), and removed the cert in certbot with `sudo certbot delete`. 

I also had to remove the HTTP -> HTTPS redirect which I did by restoring the nginx configuration file in sites-available to the original one from the Digital Ocean setup guide.

## Docker

At this point, I wanted to test a Docker setup, so I installed the Docker engine [using the standard guide from Docker](https://docs.docker.com/engine/install/debian/). 

The goal is to reach a setup similar to the [one in this example repo.](https://github.com/docker/awesome-compose/tree/master/nginx-wsgi-flask)
