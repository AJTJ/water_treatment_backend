- Set the domain in QR code generation

API
- Add Auth for generating QR codes

Equipment
- Review Ewan's notes on specifics about endpoints

Alembic
- Why are there errors in the versions?
    # TODO: Add another fallback method... should the google sheet reset completely sometimes?

Google sheet
- programmatic sorting
Implement periodic consistency checks to validate that the Google Sheet matches the database. If inconsistencies are found, perform targeted updates rather than a complete rewrite.
- periodic retries of failed syncs?