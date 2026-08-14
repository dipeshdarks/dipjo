# Dipjo Contact Manager

A complete CRUD (Create, Read, Update, Delete) application built with the Dipjo database API.

## Features

- Create contacts with name, email, phone, and company
- View all contacts
- Search contacts by field
- Edit existing contacts
- Delete contacts
- Data persists between runs (SQLite)

## Usage

```bash
dipjo examples/crud-app/app.dipjo
```

## API Used

```dipjo
contacts = database("contacts")
contacts.create({...})
contacts.find()
contacts.find({field: value})
contacts.update({id: id}, {changes})
contacts.delete({id: id})
contacts.count()
```

## Data Storage

Data is stored in `.dipjo/data/dipjo.db` relative to the application directory.
