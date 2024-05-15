# Self-Domain Setup Documentation

For the most part, I followed [this guide that was created for Ubuntu with minor tweaks.](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04)

I had a few issues due to bad configuration setup, but the only one that wasn't addressed by the guide was fixed [by the following StackOverflow comment.](https://stackoverflow.com/a/69992384)

The issue was caused by the nginx user being set to the www-data group by default and being unable to access the flask.sock file because it's owned by the flask group. I moved the nginx user into the flask group which fixed the issue.

`sudo sed -i 's/user www-data;/user flask;/' /etc/nginx/nginx.conf`

The SSL/TLS setup was particularly trivial. Using certbot, I was able to put a LetsEncrypt cert on the domain within a few minutes.
