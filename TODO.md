- Set the domain in QR code generation

Control Serialization in API Endpoints:

When returning data, exclude the recursive fields that could cause the problem using FastAPI's response_model_exclude_unset or dict(exclude={...}).
Example for an API response:

python
Copy code
@app.get("/suppliers", response_model=List[SupplierBase])
def get_suppliers():
    suppliers = db.query(Supplier).all()
    # Prevent the recursive serialization
    return [supplier.dict(exclude={"equipment": True}) for supplier in suppliers]
Read vs Write Models:

Use the full model for creating/updating records (when full relational data might be needed) and use a simplified model for read operations (when relationships don’t need to be recursively included).
Example for Create/Update:

python
Copy code
class SupplierCreate(BaseModel):
    name: str
    equipment_ids: List[uuid.UUID]
Example for Read:

python
Copy code
class SupplierRead(BaseModel):
    id: uuid.UUID
    name: str
    # Optionally include a shallow reference to equipment
    equipment: Optional[list[EquipmentBaseSimple]]
Conclusion:
Yes, this recursive reference could be a problem in your code, especially with many-to-many relationships.
The most idiomatic approach is to use separate models for input (write) and output (read), where the output model doesn’t include the full nested relationship. This ensures you avoid circular references while still keeping the data structure intact for validation and input.
Additionally, control what gets serialized in your API responses by using FastAPI's response_model_exclude_unset or Pydantic's exclude feature when needed.
This approach will help you avoid recursive reference issues while keeping your models maintainable and easy to work with. Would you like to implement this or have further clarification on any part?

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