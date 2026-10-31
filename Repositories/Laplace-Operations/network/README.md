# Environment routes

`environments.json` declares the browser origin independently of the service's loopback listener. It also declares
the existing OAuth clients and their callback paths. Client IDs are public; credentials do not belong in this file.

`configure-dns.ps1 -Apply` creates the declared private CNAMEs using the existing Cloudflare login and reads them back.
It refuses conflicting records. `configure-redirects.py --azure-config <provider-management login> --apply` unions the
Microsoft callback URLs with the existing registration and reads back the result. It does not grant permissions to
the runtime identity. Google web-client registration is managed in Google Auth Platform, project
`gen-lang-client-0624169393`; the gcloud IAM OAuth-client commands manage Workforce Identity Federation clients.

The monorepo owns its nginx HTTPS installation in `deploy/linux/site-host.sh` and
`deploy/private-origins.json`. Operations' legacy `setup.sh site` delegates to that host script;
it must not install a second browser route afterward. `network/install-nginx.py` is a compatibility
entry point which resolves the monorepo through `LAPLACE_MONOREPO` or `LAPLACE_SRC` and runs its
installer. It forwards `LAPLACE_PRIVATE_ORIGINS` or an explicit `--configuration` to the owning
installer. No nginx settings in this repository override the monorepo declaration.

From the configured monorepo checkout, the focused admin repair is:

```sh
sudo bash deploy/linux/site-host.sh --routing-only
```

The monorepo validates the existing certificate, nginx configuration and the named HTTPS health
endpoint, and rolls back a failed activation. Certificate issuance and renewal remain separate.

The shared nginx service waits for `network-online.target` and retries a failed start every
ten seconds. This handles private listeners whose addresses arrive after the service's
first start attempt. `sudo bash network/repair-nginx.sh` installs that systemd policy,
validates the existing nginx configuration and starts the service. The same repair runs
before existing secrets protection is reconciled by ordinary setup. It does not replace
site declarations, reset secrets, or unseal OpenBao. `bash network/repair-nginx.sh --check`
compares the installed policy and checks that nginx is active.

`bash tests/nginx-boot.sh` exercises the shipped policy with an isolated nginx process
under the user's systemd manager: its first start fails, the configuration becomes
available, and the automatic retry must serve HTTP 200 over a temporary Unix socket.
This verifies recovery behavior without restarting the serving proxy. Verification of
the installed HTTPS routes remains a separate check.

IIS installation, publication and verification must consume the same machine declaration: `LAPLACE_IIS_API`,
`LAPLACE_IIS_SITE`, `LAPLACE_IIS_POOL`, `LAPLACE_PUBLIC_BASE_URL` and `LAPLACE_IIS_CERTIFICATE_THUMBPRINT`.
The certificate must be installed in LocalMachine/My. IIS bindings and certificate installation are elevated setup
operations; an answering Kestrel process does not prove the IIS application is installed.

Run `acceptance/verify.ps1 -Check browser-routes -Output <new receipt>` on hart-desktop to check the declared browser
origins. It checks DNS/TLS, the SPA, application health and exact Google/Microsoft redirect origins. It stores no
OAuth state or credentials and does not claim a generated redirect proves provider registration or completed login.

References: [ASP.NET Core proxy configuration](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer?view=aspnetcore-10.0),
[IIS hosting](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/iis/?view=aspnetcore-10.0),
[nginx proxy headers](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header),
[Google web-client registration](https://support.google.com/cloud/answer/15549257?hl=en),
[Microsoft callback registration](https://learn.microsoft.com/en-us/entra/identity-platform/reply-url).
