# Glossary
## Developer

Third-party system that wants to integrate with Alliedstar.

## Alliedstar Open Platform

Alliedstar open platform，provides API for developers.

## User

Clinic or Lab who uses Alliedstar or Third-party system.

## AS Connect System

AS Connect consists of two components: local and cloud. It provides both REST and Command Line interfaces for integrating various types of medical software systems (local or cloud-based). The local component includes the AS Connect local client and server, with all data and files stored in a local SQLite database and file system. The cloud component includes both the web front end and back end, with all data and files stored on MySQL databases and Alibaba Cloud OSS servers.

- **AS Connect Local**


Alliedstar’s Windows client allows users to create cases, perform scans, upload files, and more. Developers can integrate with the local client via the Command Line Interface.

 - **AS Connect Cloud**

Alliedstar’s cloud system is accessible through a web browser. Users can manage cases, create orders, and handle partner relationships online. Developers can integrate with the cloud system using the open platform's API.

## ScanPro

Alliedstar’s scanning software performs the actual scanning operations. It is typically embedded within AS Connect but can also be triggered via the Command Line Interface.
