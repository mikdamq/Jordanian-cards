# Going live on walakelmeh.com

The website is at `https://walakelmeh.com/` and the game at `https://walakelmeh.com/play/`, both on our Namecheap hosting. Every push to `main` builds both and uploads them automatically (`.github/workflows/deploy.yml`).

## What's already done in the repo

- The website and the game are built into one folder: the website at `/`, the game at `/play/`.
- Forms post to our own script, `/api/send.php`, which emails hello@walakelmeh.com. It has a honeypot, a same-site check, length limits and a rate limit.
- `.htaccess` forces https, sends `www` to the bare domain, sets caching (and no caching for the game's service worker), and sends the old `/privacy.html` to `/privacy/`.
- The share image, partner-kit QR codes, store listing and privacy URL all use walakelmeh.com.
- The old GitHub Pages address has a redirect ready. It switches on only when you say the domain is live (step 6).

## Your steps (about 20 minutes)

### 1. Make sure https works
In Namecheap **cPanel → SSL/TLS Status**, check that `walakelmeh.com` and `www.walakelmeh.com` have a valid certificate. If they don't, click **Run AutoSSL**. The game needs https to install and work offline.

### 2. Create an FTP account for deploys
In **cPanel → FTP Accounts**:
- Log in: `deploy` (it becomes `deploy@walakelmeh.com`)
- Directory: the domain's **Document Root**, shown in **cPanel → Domains** next to walakelmeh.com. On our account that's `/home/chefxmkt/walakelmeh.com`, because walakelmeh.com is an extra domain, not the account's main one. Remove any `/deploy` cPanel adds to the end.
- A strong password, saved in your password manager

Then note the **server hostname** shown under "Configure FTP Client" (something like `server123.web-hosting.com`). Use that hostname rather than `ftp.walakelmeh.com`, because the encrypted connection checks the certificate against it.

### 3. Add the secrets in GitHub
In the repository, go to **Settings → Secrets and variables → Actions**.

**Secrets** tab, then **New repository secret**, three times:

| Name | Value |
| --- | --- |
| `FTP_SERVER` | The server hostname from step 2 |
| `FTP_USERNAME` | `deploy@walakelmeh.com` |
| `FTP_PASSWORD` | The password from step 2 |

**Variables** tab, then **New repository variable**:

| Name | Value |
| --- | --- |
| `FTP_DIR` | `./` (the FTP account already opens inside the domain's folder) |

Never paste these in chat, an issue or a commit. GitHub keeps them encrypted.

### 4. Check the email deliverability
In **cPanel → Email Deliverability**, make sure `walakelmeh.com` shows SPF and DKIM as valid. If not, click **Repair**. This keeps form emails out of spam.

### 5. Publish
Merge the work branch into `main` (or ask Claude to open a pull request). Then watch **Actions → Deploy**. When it's green:
- Open https://walakelmeh.com and https://walakelmeh.com/play/
- Send a test suggestion from any category page and check that it reaches hello@walakelmeh.com (look in spam too, the first time)
- Delete any old default files Namecheap put in the domain's folder (like a default `index.php`). Leave `cgi-bin` and `.well-known` alone.

### 6. Switch the old address to a redirect
Only after step 5 works. Add a repository **variable** `DOMAIN_LIVE` = `true`, then run **Actions → Deploy → Run workflow**. From then on:
- Anyone opening `mikdamq.github.io/Jordanian-cards` goes to `walakelmeh.com/play/`, and the old privacy page goes to `walakelmeh.com/privacy/`.
- Installed copies of the old address clean themselves up and redirect too. Players' saved names and settings can't move between addresses, so they set them once again.

### 7. Tell the search engines
- **Google Search Console**: add the domain property `walakelmeh.com`, verify it with the TXT record it gives you (Namecheap → Domain List → Manage → Advanced DNS), then submit `https://walakelmeh.com/sitemap.xml`.
- **Bing Webmaster Tools**: import the site from Search Console.

### 8. Update the stores
When you create the store listings, use `https://walakelmeh.com/privacy/` as the privacy policy and `https://walakelmeh.com` as the website (also in `docs/store/listing.md`).

## If something goes wrong

| Problem | Fix |
| --- | --- |
| Deploy fails at the upload step | Check the three secrets. If FTPS is refused, ask Namecheap support whether FTP over TLS is on for your plan. |
| The site shows Namecheap's default page | Delete the default `index.php` (or `default.html`) from the domain's folder. |
| The site is empty, or files land in a subfolder | The FTP account's directory must be the domain's Document Root, with no `/deploy` on the end (step 2), and `FTP_DIR` must be `./` (step 3). |
| Forms say there was a problem | Check **cPanel → Track Delivery**. If PHP mail is blocked, Namecheap support can enable it, or we switch the script to SMTP. |
| The game shows an old version | It updates itself on the next visit. A hard refresh also works. |
