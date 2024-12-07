# getcall

# to start install packages with comand:
pip install django django-oauth-toolkit django-hosts drf-yasg Pillow social-auth-app-django social-auth-core python-dotenv django-health-check

Sistema di Affiliazione (Affiliate System)

Affiliate
id, user_id, name, email, phone, date_joined, status, total_earnings, country, profile_picture, account_balance, last_login, referral_source

AffiliateProgram
id, name, description, commission_rate, currency, min_payout_threshold, max_payout_limit, date_created, is_active, duration, allowed_countries, target_industry

AffiliateLink
id, affiliate_id, program_id, url, click_count, conversion_count, date_created, last_used, link_status, landing_page, custom_tracking_id

AffiliateCommission
id, affiliate_id, program_id, amount, currency, date_awarded, status, approved_by, commission_type, description, tier

AffiliateTransaction
id, commission_id, affiliate_id, transaction_amount, transaction_date, order_id, product_id, status, payment_date, commission_rate, discount_applied, coupon_code

AffiliatePayout
id, affiliate_id, amount, currency, payout_date, payout_method, payout_status, transaction_id, processing_fee, net_amount, payout_provider

AffiliatePerformance
id, affiliate_id, period, total_clicks, total_conversions, conversion_rate, total_earnings, average_order_value, refund_rate, customer_lifetime_value, top_product

AffiliateTier
id, program_id, tier_name, min_sales, commission_rate, tier_benefits, access_level, next_tier_threshold, tier_expiration

AffiliateNotification
id, affiliate_id, message, date_sent, is_read, priority, notification_type

AffiliateSettings
id, affiliate_id, preferred_currency, preferred_payment_method, payout_schedule, notification_preference, dashboard_layout

AffiliateAudit
id, affiliate_id, action_taken, action_date, ip_address, device_info, location

AffiliateCampaign
id, program_id, campaign_name, start_date, end_date, goal, budget, spending_to_date

AffiliateSupportTicket
id, affiliate_id, ticket_number, subject, description, status, date_created, date_closed, priority, assigned_agent
Sistema di Codici di Referral (Referral Code System)
Tabelle aggiuntive e attributi:

ReferralProgram
id, name, description, reward_type, reward_value, currency, min_referral_count, max_referrals_per_user, date_created, is_active, program_duration, allowed_regions, target_industry

ReferralCode
id, user_id, program_id, code, usage_count, date_created, status, expiry_date, referred_user_count, unique_url, campaign_source, campaign_medium

ReferralTransaction
id, referral_code_id, referred_user_id, transaction_date, order_id, transaction_amount, currency, status, conversion_value, discount_value, coupon_code_used, channel

ReferralReward
id, referral_code_id, referred_user_id, reward_type, reward_value, date_awarded, status, expiry_date, reward_description, reward_source

ReferralUser
id, user_id, total_referrals, active_referrals, inactive_referrals, total_rewards_earned, total_spent_by_referred_users, average_order_value, loyalty_points_earned

ReferralBonus
id, program_id, bonus_type, bonus_value, min_referrals_required, bonus_date, expiry_date, max_usage, eligibility_criteria

ReferralNotification
id, user_id, message, date_sent, is_read, type, priority, action_required

ReferralSettings
id, user_id, default_reward_type, max_referrals_allowed, notification_preference, auto_share_setting, social_share_message

ReferralConversion
id, referral_code_id, referred_user_id, conversion_date, conversion_value, status, reward_issued, conversion_source, referral_type

ReferralStats
id, referral_code_id, period, click_count, conversion_count, total_rewards, average_conversion_value, highest_referral_earning

ReferralAudit
id, referral_code_id, action_taken, action_date, user_id, ip_address, device_info

ReferralCampaign
id, program_id, campaign_name, start_date, end_date, goal, budget, spending_to_date, target_audience

ReferralEngagement
id, referral_code_id, user_id, email_opened, email_clicked, social_share_count, last_interaction_date

# to start
python -m venv env
source env\bin\activate

or

env\scripts\activate
python manage.py runserver

# How to use subdomains for different apps in django

source:

https://dev.to/ksharma20/how-to-use-subdomains-for-different-apps-in-django-project--fbi

# Test locally

To test locally, we should configure HOST DNS local.

On Linux e Mac, file can be found in path /etc/hosts. On Windows should be found maybe %SystemRoot%\system32\drivers\etc\hosts.

hosts:
127.0.0.1 localhost
255.255.255.255 broadcasthost
::1             localhost

127.0.0.1 www.mysite.local
127.0.0.1 help.mysite.local


# Table of Contents

- [Microsoft IIS](#microsoft-iis)

- [Apache + mod_wsgi](#apache-and-mod_wsgi)

- [nginx + Waitress](#nginx-and-waitress)


##  Microsoft IIS

- Watch on YouTube: [Deploy Django on Windows using Microsoft IIS](https://youtu.be/APCQ15YqqQ0)

### Steps

1. Install IIS on your VM or machine, and enable CGI

    - [How to Install IIS on Windows 8 or Windows 10](https://www.howtogeek.com/112455/how-to-install-iis-8-on-windows-8/)

    - [CGI](https://docs.microsoft.com/en-us/iis/configuration/system.webserver/cgi)

2. Copy `getcall` to `C:/inetpub/wwwroot/getcall`

3. Install Python 3.7 in `C:/Python37`, and install the necessary libraries `django`, `openpyxl`, `wfastcgi`; see `getcall/install_requirements.bat`

4. Navigate to `C:/`, right-click on `Python37`, and edit `Properties`. Under Security, add `IIS AppPool\DefaultAppPool`. `DefaultAppPool` is the default app pool.

5. Enable wfastcgi

    - Open a CMD terminal as Administrator, and run the command `wfastcgi-enable`. 
    
    - Copy the Python path, and replace the `scriptProcessor="<to be filled in>"` in web-config-template with the Python path returned by `wfastcgi-enable`.

6. Edit the remaining settings in `web-config-template` then save it as `web.config` in the `C:/inetpub/wwwroot/` directory. It should NOT sit inside `getcall/`. Other settings can be modified if `getcall` does NOT sit at `C:/inetpub/wwwroot/`

    - Edit project `PYTHONPATH` (path to your project)

    - Edit `WSGI_HANDLER` (located in your `wsgi.py`)

    - Edit `DJANGO_SETTINGS_MODULE` (your `settings.py` module)

7. Open Internet Information Services (IIS) Manager. Under connections select the server, then in the center pane under Management select Configuration Editor. Under Section select system.webServer/handlers. Under Section select Unlock Section. This is required because the `C:/inetpub/wwwroot/web.config` creates a [route handler](https://pypi.org/project/wfastcgi/#route-handlers) for our project.


8. Add Virtual Directory. In order to enable serving static files map a static alias to the static directory, `C:/inetpub/wwwroot/getcall/static/`

9. Refresh the server and navigate to `localhost`



## Apache and mod_wsgi

- Watch on YouTube: [Deploy Django with Apache and mod_wsgi on Windows Server 2019](https://www.youtube.com/watch?v=frEjX1DNSpc)

### References:

- [How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/modwsgi/)

For Apache 2.4 and mod_wsgi use the httpd.conf.template


### Steps 

1. Download and install Apache 2.4 in `C:/Apache24`. Use [Apache Lounge](https://www.apachelounge.com/download/), or any flavor you prefer.

    - After copying files over to `C:/Apache24`, open a CMD terminal as Administrator. Navigate to `C:/Apache24` and run `bin\httpd.exe -k install` to install the Apache service. You can then navigate to `localhost` to view the test page.

    - You can start the service by running `httpd.exe -k start`

    - You can stop the services by running `httpd.exe -k stop` and restart it by `httpd.exe -k restart`

2. Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). You will need this before you run `pip install mod_wsgi`.

3. Install Python 3.7 in `C:/Python37` (you don't need to create a virtual environment)

4. Install `django`, `openpyxl`, `modwsgi` (see `install_requirements.bat`)

5. On a CMD terminal, run `mod_wsgi-express module-config`, then copy the contents and edit  `getcall/httpd.conf.template`. Edit paths to Python and your Django project.

6. On a CMD terminal, run `C:/Apache24/bin/httpd.exe -k start`, open a web browser and navigate to `localhost` (make sure `ALLOWED_HOSTS` has been updated).



### References:

- [Configure Python web apps for IIS](https://docs.microsoft.com/en-us/visualstudio/python/configure-web-apps-for-iis-windows?view=vs-2019)

- [WFastCGI](https://pypi.org/project/wfastcgi/)

For Microsoft IIS please use the `getcall/web-config-template` and the `getcall/static/web.config` files. Update the `web-config-template` as needed. It will be used to create a `web.config` that sits on `C:/inetpub/wwwroot/web.config`; The directory will contain all project files: `C:/inetpub/wwwroot/web.config` along with `C:/inetpub/wwwroot/getcall`.



## nginx and Waitress

- Watch on YouTube: [Deploy Django with NGINX and Waitress on Windows Server 2019](https://youtu.be/BBKq6H9Rm5g)

### Steps

1. Download and copy nginx to `C:/`.

2. Install Python 3.7 in `C:/Python37` and install 

    - `django`, `openpyxl` and [`waitress`](https://docs.pylonsproject.org/projects/waitress/en/stable/)

3. Edit `ALLOWED_HOSTS` in `settings.py`. Waitress will be running the Django server at `http://localhost:8080`.

4. Collect static files by running `python manage.py collectstatic`

5. Edit `nginx_waitress/webproeject_nginx.conf`

    - Edit the `server_name`

    - Edit the path to `/static` (and `/media` if needed)
    
    - Edit `proxy_pass` to match the server running from Waitress (i.e. `runserver.py`). This will usually be `localhost` or your IP address

6. Create two directories inside of `C:/nginx/`

    - Create `sites-enabled` and `sites-available`

    - Copy `getcall_nginx.conf` to the two directories

6. Edit `C:/nginx/conf/nginx.conf`

    - Add `include <path to your sites-enabled/getcall_nginx.conf>;`

    - Change port `80` to a non-essential port like `10`. We will need to utilize `80` for our Django project

7. Open a terminal at `C:/nginx/` and run `nginx.exe -t` to check files, and if everything is successful run `nginx.exe` to start the server

8. Open a web browser and navigate to `http://localhost`
