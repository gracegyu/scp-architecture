# Floating License Server Setup

| EzDent-i | "EzDent-i" | ezdenti | (baseServerUrl)/opflicense/ezdenti |
| --- | --- | --- | --- |
| Ez3D-i | "Ez3D-i" | ez3di | (baseServerUrl)/opflicense/ez3di |
| EzOrtho | "EzOrtho" | ezortho | (baseServerUrl)/opflicense/ezortho |
| Prora View | "Prora View" | proraview | (baseServerUrl)/opflicense/proraview |

Default baseServerUrl will be http://127.0.0.1:43112 which is configurable in EzServer Control Panel.

# Service Config File

See product_ids value in license_manager section from [EzServer Service Config File Format](<../EzServerService/EzServer Service Config File Format.md>)

# Nginx configuration

File location: (EzWebServer Installed Directory)\bin\nginx\conf\proxies\opflicense_(product_id).conf

e.g. Ez3D-i

```
location~^/opflicense/ez3di/(.*){        proxy_pass       http://127.0.0.1:44405/$1$is_args$args;        proxy_set_headerHost              $host:$server_port;        proxy_set_headerX-Forwarded-For   $remote_addr;        proxy_set_headerX-Forwarded-Proto $scheme;        proxy_redirect   off;}
```

# LexFloatServer Config File

File Location: (EzServer Installed Directory)\LicenseManager\config\opflicense_(product_id).ini

e.g. EzDent-i

```
c:\ProgramFiles(x86)\VATECH\EzServer\LicenseManager\config\opflicense_ezdenti.ini
```