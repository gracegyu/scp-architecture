# license_server_port_offsetFile information

- File name: service_environment.ini
- Source URL: http://essvn.vatech.co.kr/svn/vatech/trunk/product/ezserver/VTEzWebServerService/src/res/Settings/service_environment_base.ini
- Default Installed Location:
    - (EzWebServer installed Directory)/service_environment.ini
        - e.g. c:/Program Files (x86)/VATECH/EzWebServer/service_environment.ini
- How to manage versions
    - v1: It was included in installer with service_environment_base.ini and copy to service_environment.ini if not exists when service is starting.
    - v2 or newer: It should NOT be included in EzServer installer.
        - Should handle the file when service is starting:
            - It should be created with default values if the ini file does not exist.
            - It should be migrated to the latest version if the ini file already exists and there is no version information or older version.

# File format

**service_envronment.ini**

```
;-------------------------------------------------------------------------------[config_format];;Version1 was usedfor previous versions ofEzServer v5.5.;This field MUST be changed whenthis file format is changed.;Default value:9;Since v2version=9
;-------------------------------------------------------------------------------[common];Global configuration;;Intervalfor health check;Default value:1000;Since v2health_check_interval_ms=1000;;Intervalfor connection check;Default value:1000;Since v2connection_check_interval_ms=1000;;Retry countfor connection check;This connection isforServicetoControlPanel;Default value:5;Since v3connection_check_retry_count=5;;Retry countfor service start failure;Default value:10;Since v3service_start_failure_retry_count=10;;Log file rotation interval(days);(Editable byUser);Default value:180;Since v2log_rotation_interval_days=180;;Log file rotation time;(Editable byUser);Default value:00:00:00(hh:mm:ss);Since v2log_rotation_time=00:00:00
;-------------------------------------------------------------------------------[internal_services];;Start number of port range isfor internal services except external services; that exposedtoexternal services such as echo, nginx.;The port scanning will be done within the port range.;(Editable byUser);Default value:44401;Since v2port_range_start=44401;;End number of the portrange. Calculated byManager/ControlPanel.;Default value:44499;Since v9,Changedtonon-editable by users.;Since v2port_range_end=44499;;Services names.;Currently, these values are used as section name.;Since v7,Appended rest_api_v2;Default value: nginx|php-fastcgi|auth_provider|license_manager|updater|messenger|pms_integration|rest_api_v2|rest_api_metrics;Since v2services=nginx|php-fastcgi|auth_provider|license_manager|updater|messenger|pms_integration|rest_api_v2|rest_api_metrics;;Services port count.;The floating license server ports are assigned afterFastCGI,AuthProvider,LicenseManager,Updater,Messenger, PMSIntegration, RESTAPI v2, REST APIMetrics.;Since v8,Default value is changed from7to8for REST APIMetrics;Since v7,Default value is changed from6to7;Default value:8;Since v2license_server_port_offset=8
;-------------------------------------------------------------------------------[paths];;Pathfor log files.;Default value:./logs;Since v1logs=./logs;;Pathfor temporary files.;Default value:./temp;Since v1temp=./temp;;Path of hidden console app.;Default value:./bin/tools/RunHiddenConsole.exe;Since v1hidden_app=./bin/tools/RunHiddenConsole.exe;;Path ofEzWebServer config file.;Default value:./www/ezwebserver/src/application/config;Since v1ezws_config_dir=./www/ezwebserver/src/application/config;;Path ofFileManager config file.;Default value:../Common/FM/Setting;Since v1fm_config_dir=../Common/FM/Setting
;-------------------------------------------------------------------------------[nginx];;Base path of nginx.;Default value:./bin/nginx;Since v1path=./bin/nginx;;Executable path.;Default value: nginx.exe;Since v1name=nginx.exe;;Path of config file.;Default value:./bin/nginx/conf/nginx.conf;Since v1config=./bin/nginx/conf/nginx.conf;-------------------------------------------------------------------------------[server];WebServer(external);;Host name.;(Editable byUser);Default value:127.0.0.1;Since v2hostname=127.0.0.1;; HTTP+UDP port;This is usedfor both HTTP and UDPfor server lookup.;(Editable byUser);Default value:43112;Since v1port=43112;;Receive buffer size.;Default value:4096;Since v1recv_buffer=4096;;Trueif HTTP is enabled.;(Editable byUser);Default value:true;Since v2http_enabled=true;;Trueif HTTPS is enabled.;(Editable byUser);Default value:false;Since v2https_enabled=false;;Trueif self-signed SSL certificated is used.;Use self-signed certificate;(Editable byUser);Default value:true;Since v2https_ssl_cert_self_signed=true;;Path of SSL certificate file.;(Editable byUser);Default value: c:/ProgramFiles(x86)/VATECH/EzWebServer/bin/nginx/conf/ssl/ezwebserver.internal.crt;Since v2https_ssl_cert_file=c:/ProgramFiles(x86)/VATECH/EzWebServer/bin/nginx/conf/ssl/ezwebserver.internal.crt;;Path of SSL key file.;(Editable byUser);Default value: c:/ProgramFiles(x86)/VATECH/EzWebServer/bin/nginx/conf/ssl/ezwebserver.internal.key;Since v2https_ssl_key_file=c:/ProgramFiles(x86)/VATECH/EzWebServer/bin/nginx/conf/ssl/ezwebserver.internal.key;; HTTPS port.;(Editable byUser);Default value:43132;Since v2https_port=43132
;-------------------------------------------------------------------------------[php-fastcgi];Fast CGI(internal);;Base path.;Default value:./bin/php;Since v1path=./bin/php;;Executable file name.;Default value: php-cgi.exe;Since v1name=php-cgi.exe;;Path of config file.;Default value:./bin/php/php.ini;Since v1config=./bin/php/php.ini;;Host name.;Default value:127.0.0.1;Since v1host=127.0.0.1;;Port number ofFast CGI.;(Editable byUser);Default value:44401;Since v1port=44401;;Maximum number of requests.;(Editable byUser);Default value:0;Since v3max_req=0;;Deprecated sincev8. Maximum number of child processes.;(Editable byUser);Default value:4;Since v3children=4;; PHPPoolSize;Default value:4;Since v8php_pool_size=4;;Maximum number of single php_pool's child processes.;Total number of fast cgi processes= php_pool_size* php_pool_children;(Editable byUser);Since v8php_pool_children=2
;-------------------------------------------------------------------------------[auth_provider];EzServerAuthProvider(internal);;Port number.;(Editable byUser);Default value:44402;Since v2port=44402;;Base path.;Default value:./AuthProvider;Since v2path=./AuthProvider;;Executable name.;Default value:./bin/EzServerAuthProvider.exe;;Since v6, renamed from./bin/AuthProvider.exeto./bin/EzServerAuthProvider.exe;Since v3executable=./bin/EzServerAuthProvider.exe;;Arguments.;Default value: start;Since v2args=start
;-------------------------------------------------------------------------------[license_manager];EzServerLicenseManager(internal);;Port number.;Default value:44403;(Editable byUser);Since v2port=44403;;BasePath.;Default value:./LicenseManager;Since v2path=./LicenseManager;;Executable file path(Relativetobase path).;Default value:./bin/EzServerLicenseManager.exe;Since v6, renamed from./bin/LicenseManager.exeto./bin/EzServerLicenseManager.exe;Since v2executable=./bin/EzServerLicenseManager.exe;;Arguments.;Default value: start;Since v2args=start;;ProductIDs.;The floating license server ports will be assigned from(n=port_range_start+ license_server_port_offset)ton+(number of productIDs-1).
;Default value: ezdenti|ez3di|ezortho;Since v5product_ids=ezdenti|ez3di|ezortho|proraview|cleverone;-------------------------------------------------------------------------------[updater];EzServerUpdater(internal);;Port number.;Default value:44404;(Editable byUser);Since v4port=44404;;BasePath.;Default value:./Updater;Since v4path=./Updater;;Executable name.;Default value:./bin/EzServerUpdater.exe;Since v6, renamed from./bin/Updater.exeto./bin/EzServerUpdater.exe;Since v4executable=./bin/EzServerUpdater.exe;;Arguments.;Default value: start;Since v4args=start
;-------------------------------------------------------------------------------[messenger];EzServerMessenger;;Messager name.(internal);Usedtosend messages betweenServerControlPanel andServerService.;Default value:Ewoosoft.EzServer.Messenger;Since v2name=Ewoosoft.EzServer.Messenger
;;Port number.;Default value:44405;(Editable byUser);Since v4port=44405;;BasePath.;Default value:./Messenger;Since v4path=./Messenger;;Executable name.;Default value:./bin/EzServerMessenger.exe;Since v4executable=./bin/EzServerMessenger.exe;;Arguments.;Default value: start;Since v4args=start
;-------------------------------------------------------------------------------[pms_integration];EzServer PMSIntegration(internal);;Port number.;Default value:44406;(Editable byUser);Since v6port=44406;;BasePath.;Default value:./PMSIntegration;Since v6path=./PMSIntegration;;Executable name.;Default value:./bin/EzServerPMSIntegration.exe;Since v6executable=./bin/EzServerPMSIntegration.exe;;Arguments.;Default value: start;Since v6args=start
;-------------------------------------------------------------------------------[rest_api_v2];EzServer RESTAPIv2(internal);;Port number.;Default value:44407;(Editable byUser);Since v7port=44407;;BasePath.;Default value:./RESTAPIv2;Since v7path=./RESTAPIv2;;Executable name.;Default value:./bin/EzServerRESTAPIv2.exe;Since v7executable=./bin/EzServerRESTAPIv2.exe;;Arguments.;Default value: start;Since v7args=start
;-------------------------------------------------------------------------------[rest_api_metrics]; REST APIMetrics(Internal);;Port number.;Default value:44408;(Editable byUser);Since v8port=44408
; EOF
```

# Change history

- v9: Changed port_range_end to non-editable by users for v6.4.0.
- v8: Added Metrics for EzServer v5.5.4, v6.3.0
    - Added "rest_api_metrics" section.
    - Added "port" in "rest_api_metrics" section.
    - Changed "license_server_port_offset" to 8 from 7 in "internal_services" section.
    - In php-fastcgi section:
        - Added "php_pool_size" value.
        - Added "php_pool_children" value.
        - Deprecated "children" value in
- v7: Added EzServer REST API v2 for EzServer v6.2.0
    - Added "rest_api_v2" section.
    - Added "rest_api_v2" in the "services" value.
    - Changed "license_server_port_offset" value from 6 to 7.
- v6: Added PMS Integration for EzServer v5.5.0
    - Added "pms_integration" section
    - "pms_integration" has been added to the value of the "services" and "license_server_port_offset" key in the internal_services section
    - Renamed exe files to add prefix "EzServer".
- v5: Updated for EzServer v5.4.0
    - Added to cleverone in product_ids.
- v4: Added Updater for EzServer v5.3.0
    - Added "messenger" section
    - Added "updater" section.
    - Added "license_server_port_offset" key in the internal_services section.
    - "updater" and "messenger" has been added to the value of the "services" key in the internal_services section.
- v3: Updated for EzServer v5.2.0
    - Changed "children" key to Editable by User.
    - Changed "max_req" key to Editable by User.
    - Added "service_start_failure_retry_count" key in common section.
    - Added "connection_check_retry_count" key in common section.
    - The value of the "executable" key in the auth_provider section has been changed from "./bin/node.exe" to "bin/AuthProvier.exe".
- v2: Updated for EzServer v5.0.0
- v1: Initial version