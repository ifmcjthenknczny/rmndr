# Project Name
rmndr

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
This is a simple app which iterates over csv-file database and checks for possible recipients of e-mails, given date of service, years of validity and days before expiration date to notify. Then it sends e-mails to entires in database meeting these conditions. This app is designed for small databases and its main purpose and intention is to remind customers to repeat an order. It is also meant to be run at autostart from command line (password and confirmation is required every time).

## Screenshots
![App in use](./screenshot.png)

## Technologies
* Python 3.7.6 (packages: csv, datetime, email, faker, getpass, mimetypes, random, shutil, smtplib)

## Setup
Designed on Windows 10. First run updates "goto.ps1" file which is connected with "rmndr.lnk" and makes it possible to run app from command line. Several settings in SETTINGS.py file are needed to be set before first use. Also, it probably will need some settings in sender mailbox to be changed, especially those about less secure applications.

## Features
> Done
* Searching in csv database for possible recipients of emails.
* Personalizing messages (html-style) with information from database.
* Starting SMTP server and sending messages.
* Creating backup of database and updating it.
* Adding information about sent e-mails into second database.
* Checking permission for the file.
* Password entering in command line.
* Multiple changeable settings.
* Generating fake database to test changes made in code.
* Automatic setup of command line shortcut.

> To-do list:
* Easy personalization for individual companies.
* Possible acceleration of the program by implementing queue data structure.
* Columns title in generated CSV files.
* Install in autostart folder.

## Status
Project is: _in progress_

## Inspiration
It is project to be implemented in my job in service industry, which highly relies on loyality of customers.

## Contact
maciej.konieczny.1993@gmail.com feel free to contact me!