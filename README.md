# Gumball Services Inc

Gumball Services Inc (Also referred to as "**GSI**") is a vendor which leases and
maintains gumball **machines** located at various retail **sites**.  The company
is structured into **compliance**, **maintenance** and **IT** departments.

The **maintenance** department includes a **dispatcher** and a team of **technicians**.
*Technicians* are assigned a group of gumball **machines** to maintain and service.
The *Dispatcher*'s job is to monitor the state of all gumball **machines**, and
determine if a **technician** needs to take action on one or more of them.

GSI supplies the YummyGummy2k(tm) model gumball machine.  All gumballs cost 25¢
and are dispensed when a customer inserts a credit into machine.  This "advanced" 
machine features an auditing system, where each **transaction** is logged electronically.
The **transaction file** is manually downloaded off the **machine** regularly by 
a **technician**, and then delivered to the **maintenance** department.

Unfortunately, the YummyGummy2k gumball machine is fraught with mechanical and
technology issues:  
 - Customers have complained that after inserting a credit, no gumball is 
    dispensed.
 - Some machines will periodically over-dispense gumballs (unsurprisingly, not 
    reported by customers)
 - The computer installed in the machine may occasionally lose its log data, or 
    the data may become corrupted in some way
 
These are all issues which the **dispatcher** must be able to identify so that 
they may call upon a **technician** to service one of their malfunctioning 
**machines**.

## Developer Instructions

The requirements for this project are in `tests/features` in Gherkin format.  
Feel free to use a BDD test framework of your choice if you wish (though this is 
not a hard requirement).  A scaffold has already been prepared with a simple Flask
app, postgres database and some sample data and a local cloud object store 
(compatible/comparable to AWS)

You will need the following:
  * Git
  * Docker
  * Python 3.7 or higher
  * Linux-like dev environment (this project was designed on OSX)
  
```bash
# extract the archived project (opshub.tar.gz)
cd opshub

# (recommended) create a virtual env
python3.7 -m venv .venv
source .venv/bin/activate

#install requirements for development
pip install -r requirements.txt
pip install -r requirements-dev.txt

# spin up local dev services
docker-compose up -d

# make sure everything is plugged in
pytest tests/functional/test_connections.py
```

## Deliverables

1. Design and build a REST API to facilitate the needs defined in requirements
2. Provide a client to interact with the API.  This may be either a CLI or GUI.

A scaffold has been provided for developing a Flask application. That said, if 
you are more comfortable using a different framework (such as Django), that is 
fine.  The only constraint is that the backend (any non-UI code) must be in 
Python.  For example, you could build the backend out in Django but build a 
front-end in React.

> If using Django, please bear in mind that our team uses SQLAlchemy's Core and ORM library heavily.

The build orchestration for this project is intentionally absent.  Please feel 
free to adopt any additional build tools that you wish.

## Evaluation Criteria

When our team reviews your solution, some (but not all) of the things we will be looking for are:

- Working code :)
- Well-tested, and _testable_ source code
- Documentation, if/where needed.
- Adherence to [conventional code style guidelines](https://www.python.org/dev/peps/pep-0008/)
- Consideration toward UX, especially if the client is a CLI.
- Solid test coverage

