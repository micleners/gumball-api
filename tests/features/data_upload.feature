Feature: Transaction File Management

  A computer is installed in each gumball machine which logs each transaction with a customer.  A transaction represents
  a customer inserting a credit (25¢ coin) and (ideally) receiving a dispensed gumball.

  Technicians are assigned a "territory" of gumball machines to service and maintain.  Every two weeks, each gumball
  machine is visited by a technician who will download the transaction data.  The technician must then manually upload
  that file to the GSI OpsHub application.

  User Story:
    As a technician assigned to service gumball machines
    I need the ability to upload a file from one of my gumball machines
    So that the transaction data can be processed by the end of the day

  Background:
    Given a technician "#001" is assigned to a gumball machine "GM001"

  Scenario: 1. Technician uploads file successfully
    Given the technician downloaded a gumball data file on 9/21/2018 at 9:34:48 AM
    When the technician requests to upload the file
    Then the response will include an id for the file (indicating success)
    And the file will exist on the shared file server named "T0001.GM001.2018-09-21_093448.zip"

  Scenario: 2. Technician views all uploaded files
    Given the technician has already uploaded several files
    When the technician requests a list their files
    Then the response will show only the files they uploaded

  Scenario: 3. Technician deletes uploaded file
    Given a file was uploaded earlier named "somefile.txt" with id 1234
    When the technician requests file 1234 to be deleted
    Then the response will indicate the file was removed
    And the file named "somefile.txt" will no longer exist on the shared file server