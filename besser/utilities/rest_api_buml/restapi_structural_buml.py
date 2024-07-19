import pickle
from typing import Union, List, Tuple
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from besser.BUML.metamodel.structural import (DomainModel, Class, Property, PrimitiveDataType, Multiplicity,
                                              Association, BinaryAssociation, Generalization, EnumerationLiteral,
                                              Enumeration, Package, Constraint, NamedElement, Method, Type, Parameter)
from besser.generators.pydantic_classes import PydanticGenerator

from fastapi.middleware.cors import CORSMiddleware

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./__domain_model_database__.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# In-memory database
db_classes = {}
db_associations = {}
db_generalizations = {}
db_enumerations = {}
db_packages = {}
db_constraints = {}

# Database model for storing serialized domain models
class DomainModelModel(Base):
    __tablename__ = 'domain_models'
    id = Column(Integer, primary_key=True, index=True)
    storage_name = Column(String, unique=True)
    serialized_data = Column(LargeBinary)

Base.metadata.create_all(bind=engine)

# Pydantic models for request data
class PropertyCreate(BaseModel):
    name: str
    property_type: str
    multiplicity: tuple[Union[int, str], Union[int, str]] = (1, 1)
    visibility: str = 'public'
    is_composite: bool = False
    is_navigable: bool = False
    is_id: bool = False
    is_read_only: bool = False

class ParameterCreate(BaseModel):
    name: str
    parameter_type: str

class MethodCreate(BaseModel):
    name: str
    visibility: str = 'public'
    is_abstract: bool = False
    parameters: List[ParameterCreate] = []
    type: str = None
    code: str = ""

class ClassCreate(BaseModel):
    name: str
    properties: List[PropertyCreate] = None
    methods: List[MethodCreate] = None
    is_abstract: bool = False
    is_read_only: bool = False

class AssociationCreate(BaseModel):
    name: str
    ends: List[PropertyCreate]

class BinaryAssociationCreate(BaseModel):
    name: str
    ends: List[PropertyCreate]

    @field_validator('ends')
    def check_ends_length(cls, v):
        if len(v) != 2:
            raise ValueError('Binary associations must have exactly two properties')
        return v

class GeneralizationCreate(BaseModel):
    general: str
    specific: str

class EnumerationCreate(BaseModel):
    name: str
    literals: List[str]

class PackageCreate(BaseModel):
    name: str
    classes: List[str] = None

class ConstraintCreate(BaseModel):
    name: str
    context: str
    expression: str
    language: str

class DomainModelCreate(BaseModel):
    name: str
    types: List[str] = None
    associations: List[str] = None
    generalizations: List[Tuple[str, str]] = None
    enumerations: List[str] = None
    packages: List[int] = None
    constraints: List[int] = None

# FastAPI application
app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a class
@app.post("/classes/")
def create_class(class_data: ClassCreate):
    if class_data.name in db_classes:
        raise HTTPException(status_code=400, detail="Class already exists")

    properties = []
    for property_data in class_data.properties:
        try:
            new_property_type = PrimitiveDataType(property_data.property_type)
        except ValueError:
            if property_data.property_type not in db_enumerations:
                raise HTTPException(status_code=400,
                                    detail=f"Property type {property_data.property_type} does not exist")
            new_property_type = db_enumerations[property_data.property_type]

        properties.append(
            Property(
                name=property_data.name,
                type=new_property_type,
                multiplicity=Multiplicity(property_data.multiplicity[0], property_data.multiplicity[1]),
                visibility=property_data.visibility,
                is_composite=property_data.is_composite,
                is_navigable=property_data.is_navigable,
                is_id=property_data.is_id,
                is_read_only=property_data.is_read_only
            )
        )
    parameters = []
    for method_data in class_data.methods:

        for param in method_data.parameters:
            try:
                param_type = PrimitiveDataType(param.parameter_type)
            except ValueError:
                if param.parameter_type in db_classes:
                    param_type = db_classes[param.parameter_type]
                elif param.parameter_type in db_enumerations:
                    param_type = db_enumerations[param.parameter_type]
                else:
                    raise HTTPException(status_code=400, detail=f"Parameter type {param.parameter_type} does not exist")
            parameters.append(Parameter(name=param.name, type=param_type))

    methods = [
        Method(
            name=method_data.name,
            visibility=method_data.visibility,
            is_abstract=method_data.is_abstract,
            parameters=set(parameters),
            type=Type(method_data.type),
            code=method_data.code
        ) for method_data in class_data.methods
    ]

    new_class = Class(
        name=class_data.name,
        attributes=set(properties),
        methods=set(methods),
        is_abstract=class_data.is_abstract,
        is_read_only=class_data.is_read_only
    )

    db_classes[class_data.name] = new_class

    return {"id": class_data.name, "message": "Class stored successfully"}

# Endpoint to get all classes
@app.get("/classes/")
def get_classes():
    def class_to_dict(class_obj):
        return {
            "name": class_obj.name,
            "is_abstract": class_obj.is_abstract,
            "is_read_only": class_obj.is_read_only,
            "attributes": [
                {
                    "name": attr.name,
                    "type": attr.type.name if isinstance(attr.type, NamedElement) else attr.type,
                    "multiplicity": (attr.multiplicity.min, attr.multiplicity.max),
                    "visibility": attr.visibility,
                    "is_composite": attr.is_composite,
                    "is_navigable": attr.is_navigable,
                    "is_id": attr.is_id,
                    "is_read_only": attr.is_read_only,
                }
                for attr in class_obj.attributes
            ],
            "methods": [
                {
                    "name": meth.name,
                    "visibility": meth.visibility,
                    "is_abstract": meth.is_abstract,
                    "parameters": [
                        {"name": param.name, "type": param.type.name}
                        for param in meth.parameters
                    ],
                    "type": meth.type.name if meth.type else None,
                    "code": meth.code,
                }
                for meth in class_obj.methods
            ],
        }

    classes_dict = {name: class_to_dict(cls) for name, cls in db_classes.items()}
    return jsonable_encoder(classes_dict)

# Endpoint to get a specific class by name
@app.get("/classes/{class_name}")
def get_class(class_name: str):
    def class_to_dict(class_obj):
        return {
            "name": class_obj.name,
            "is_abstract": class_obj.is_abstract,
            "is_read_only": class_obj.is_read_only,
            "attributes": [
                {
                    "name": attr.name,
                    "type": attr.type.name if isinstance(attr.type, NamedElement) else attr.type,
                    "multiplicity": (attr.multiplicity.min, attr.multiplicity.max),
                    "visibility": attr.visibility,
                    "is_composite": attr.is_composite,
                    "is_navigable": attr.is_navigable,
                    "is_id": attr.is_id,
                    "is_read_only": attr.is_read_only,
                }
                for attr in class_obj.attributes
            ],
            "methods": [
                {
                    "name": meth.name,
                    "visibility": meth.visibility,
                    "is_abstract": meth.is_abstract,
                    "parameters": [
                        {"name": param.name, "type": param.type.name}
                        for param in meth.parameters
                    ],
                    "return_type": meth.type.name if meth.type else None,
                    "code": meth.code,
                }
                for meth in class_obj.methods
            ],
        }

    if class_name not in db_classes:
        raise HTTPException(status_code=404, detail="Class not found")

    class_obj = db_classes[class_name]
    class_dict = class_to_dict(class_obj)
    return jsonable_encoder(class_dict)

@app.put("/classes/{class_id}")
def update_class(class_id: str, class_data: ClassCreate):
    if class_id not in db_classes:
        raise HTTPException(status_code=404, detail="Class not found")

    existing_class = db_classes[class_id]

    if class_id != class_data.name:
        if class_data.name in db_classes:
            raise HTTPException(status_code=400, detail="Class with the new name already exists")
        db_classes[class_data.name] = db_classes.pop(class_id)
        existing_class.name = class_data.name

    existing_properties = {prop.name: prop for prop in existing_class.attributes}
    existing_methods = {meth.name: meth for meth in existing_class.methods}

    new_properties = {}
    for property_data in class_data.properties:
        try:
            new_property_type = PrimitiveDataType(property_data.property_type)
        except ValueError:
            if property_data.property_type not in db_enumerations:
                raise HTTPException(status_code=400,
                                    detail=f"Property type {property_data.property_type} does not exist")
            new_property_type = db_enumerations[property_data.property_type]

        if property_data.name in existing_properties:
            property = existing_properties[property_data.name]
            property.type = new_property_type
            property.multiplicity = Multiplicity(property_data.multiplicity[0], property_data.multiplicity[1])
            property.visibility = property_data.visibility
            property.is_composite = property_data.is_composite
            property.is_navigable = property_data.is_navigable
            property.is_id = property_data.is_id
            property.is_read_only = property_data.is_read_only
            new_properties[property_data.name] = property
        else:
            new_property = Property(
                name=property_data.name,
                type=new_property_type,
                multiplicity=Multiplicity(property_data.multiplicity[0], property_data.multiplicity[1]),
                visibility=property_data.visibility,
                is_composite=property_data.is_composite,
                is_navigable=property_data.is_navigable,
                is_id=property_data.is_id,
                is_read_only=property_data.is_read_only
            )
            new_properties[property_data.name] = new_property

    existing_class.attributes = set(new_properties.values())

    new_methods = {}
    for method_data in class_data.methods:
        if method_data.name in existing_methods:
            method = existing_methods[method_data.name]
            method.visibility = method_data.visibility
            method.is_abstract = method_data.is_abstract
            method.parameters = {Parameter(name=param.name, type=PrimitiveDataType(param.parameter_type)) for param in method_data.parameters}
            method.type = PrimitiveDataType(method_data.return_type) if method_data.return_type else None
            method.code = method_data.code
            new_methods[method_data.name] = method
        else:
            new_method = Method(
                name=method_data.name,
                visibility=method_data.visibility,
                is_abstract=method_data.is_abstract,
                parameters={Parameter(name=param.name, type=PrimitiveDataType(param.parameter_type)) for param in method_data.parameters},
                type=PrimitiveDataType(method_data.return_type) if method_data.return_type else None,
                code=method_data.code
            )
            new_methods[method_data.name] = new_method

    existing_class.methods = set(new_methods.values())

    existing_class.is_abstract = class_data.is_abstract
    existing_class.is_read_only = class_data.is_read_only

    return get_class(class_data.name)




# Endpoint to create an association
@app.post("/associations/")
def create_association(association_data: AssociationCreate):
    if association_data.name in db_associations:
        raise HTTPException(status_code=400, detail="Association already exists")

    ends = []
    for property_data in association_data.ends:
        if property_data.property_type not in db_classes:
            raise HTTPException(status_code=400, detail=f"Property type {property_data.property_type} does not exist")

        new_property = Property(
            name=property_data.name,
            type=db_classes[property_data.property_type],  # Validate and retrieve the class
            multiplicity=Multiplicity(property_data.multiplicity[0], property_data.multiplicity[1]),
            visibility=property_data.visibility,
            is_composite=property_data.is_composite,
            is_navigable=property_data.is_navigable,
            is_id=property_data.is_id,
            is_read_only=property_data.is_read_only
        )
        ends.append(new_property)

    new_association = Association(
        name=association_data.name,
        ends=ends
    )

    db_associations[association_data.name] = new_association

    return {"id": association_data.name, "message": "Association stored successfully"}

# Endpoint to get all associations
@app.get("/associations/")
def get_associations():
    def association_to_dict(association_obj):
        return {
            "name": association_obj.name,
            "ends": [
                {
                    "name": end.name,
                    "type": end.type.name if isinstance(end.type, Class) else end.type,
                    "multiplicity": end.multiplicity,
                    "visibility": end.visibility,
                    "is_composite": end.is_composite,
                    "is_navigable": end.is_navigable,
                    "is_id": end.is_id,
                    "is_read_only": end.is_read_only,
                }
                for end in association_obj.ends
            ],
        }

    associations_dict = {name: association_to_dict(assoc) for name, assoc in db_associations.items()}
    return jsonable_encoder(associations_dict)

# Endpoint to get a specific association by name
@app.get("/associations/{association_name}")
def get_association(association_name: str):
    def association_to_dict(association_obj):
        return {
            "name": association_obj.name,
            "ends": [
                {
                    "name": end.name,
                    "type": end.type.name if isinstance(end.type, Class) else end.type,
                    "multiplicity": end.multiplicity,
                    "visibility": end.visibility,
                    "is_composite": end.is_composite,
                    "is_navigable": end.is_navigable,
                    "is_id": end.is_id,
                    "is_read_only": end.is_read_only,
                }
                for end in association_obj.ends
            ],
        }

    if association_name not in db_associations:
        raise HTTPException(status_code=404, detail="Association not found")

    association_obj = db_associations[association_name]
    association_dict = association_to_dict(association_obj)
    return jsonable_encoder(association_dict)

@app.put("/associations/{association_id}")
def update_association(association_id: str, association_data: AssociationCreate):
    if association_id not in db_associations:
        raise HTTPException(status_code=404, detail="Association not found")

    existing_association = db_associations[association_id]

    if association_id != association_data.name:
        if association_data.name in db_associations:
            raise HTTPException(status_code=400, detail="Association with the new name already exists")
        db_associations[association_data.name] = db_associations.pop(association_id)
        existing_association.name = association_data.name

    existing_ends = {end.name: end for end in existing_association.ends}

    new_ends = []
    for end_data in association_data.ends:
        if end_data.property_type not in db_classes:
            raise HTTPException(status_code=400, detail=f"Property type {end_data.property_type} does not exist")

        if end_data.name in existing_ends:
            end = existing_ends[end_data.name]
            end.type = db_classes[end_data.property_type]
            end.multiplicity = Multiplicity(end_data.multiplicity[0], end_data.multiplicity[1])
            end.visibility = end_data.visibility
            end.is_composite = end_data.is_composite
            end.is_navigable = end_data.is_navigable
            end.is_id = end_data.is_id
            end.is_read_only = end_data.is_read_only
        else:
            end = Property(
                name=end_data.name,
                type=db_classes[end_data.property_type],
                multiplicity=Multiplicity(end_data.multiplicity[0], end_data.multiplicity[1]),
                visibility=end_data.visibility,
                is_composite=end_data.is_composite,
                is_navigable=end_data.is_navigable,
                is_id=end_data.is_id,
                is_read_only=end_data.is_read_only
            )
        new_ends.append(end)

    existing_association.ends = new_ends

    return get_association(association_data.name)

# Binary Associations
# Endpoint to create a binary association
@app.post("/binary_associations/")
def create_binary_association(association_data: BinaryAssociationCreate):
    if association_data.name in db_associations:
        raise HTTPException(status_code=400, detail="Binary Association already exists")

    ends = []
    for property_data in association_data.ends:
        if property_data.property_type not in db_classes:
            raise HTTPException(status_code=400, detail=f"Property type {property_data.property_type} does not exist")

        new_property = Property(
            name=property_data.name,
            type=db_classes[property_data.property_type],  # Validate and retrieve the class
            multiplicity=Multiplicity(property_data.multiplicity[0], property_data.multiplicity[1]),
            visibility=property_data.visibility,
            is_composite=property_data.is_composite,
            is_navigable=property_data.is_navigable,
            is_id=property_data.is_id,
            is_read_only=property_data.is_read_only
        )
        ends.append(new_property)

    new_binary_association = BinaryAssociation(
        name=association_data.name,
        ends=ends
    )

    db_associations[association_data.name] = new_binary_association

    return {"id": association_data.name, "message": "Binary Association stored successfully"}

# Generalizations
# Endpoint to create a generalization
@app.post("/generalizations/")
def create_generalization(generalization_data: GeneralizationCreate):
    if generalization_data.general not in db_classes or generalization_data.specific not in db_classes:
        raise HTTPException(status_code=404, detail="General or Specific class not found")

    new_generalization = Generalization(
        general=db_classes[generalization_data.general],
        specific=db_classes[generalization_data.specific]
    )

    db_generalizations[(generalization_data.general, generalization_data.specific)] = new_generalization

    return {"id": (generalization_data.general, generalization_data.specific), "message": "Generalization stored successfully"}

# Endpoint to get all generalizations
@app.get("/generalizations/")
def get_generalizations():
    def generalization_to_dict(generalization_obj):
        return {
            "general": generalization_obj.general.name,
            "specific": generalization_obj.specific.name,
        }

    generalizations_dict = {
        f"{gen.general.name}-{gen.specific.name}": generalization_to_dict(gen)
        for gen in db_generalizations.values()
    }
    return jsonable_encoder(generalizations_dict)

# Endpoint to get a specific generalization by general and specific class names
@app.get("/generalizations/{general_name}/{specific_name}")
def get_generalization(general_name: str, specific_name: str):
    def generalization_to_dict(generalization_obj):
        return {
            "general": generalization_obj.general.name,
            "specific": generalization_obj.specific.name,
        }

    generalization_key = (general_name, specific_name)
    if generalization_key in db_generalizations:
        generalization_obj = db_generalizations[generalization_key]
        generalization_dict = generalization_to_dict(generalization_obj)
        return jsonable_encoder(generalization_dict)

    raise HTTPException(status_code=404, detail="Generalization not found")


# Enumerations
# Endpoint to create an enumeration
@app.post("/enumerations/")
def create_enumeration(enumeration_data: EnumerationCreate):
    if enumeration_data.name in db_enumerations:
        raise HTTPException(status_code=400, detail="Enumeration already exists")

    literals = {EnumerationLiteral(name=lit, owner=None) for lit in enumeration_data.literals}
    new_enumeration = Enumeration(
        name=enumeration_data.name,
        literals=literals
    )

    db_enumerations[enumeration_data.name] = new_enumeration

    return {"id": enumeration_data.name, "message": "Enumeration stored successfully"}

# Endpoint to get a specific enumeration by name
@app.get("/enumerations/{enumeration_name}")
def get_enumeration(enumeration_name: str):
    def enumeration_to_dict(enumeration_obj):
        return {
            "name": enumeration_obj.name,
            "literals": [literal.name for literal in enumeration_obj.literals],
        }

    if enumeration_name not in db_enumerations:
        raise HTTPException(status_code=404, detail="Enumeration not found")

    enumeration_obj = db_enumerations[enumeration_name]
    enumeration_dict = enumeration_to_dict(enumeration_obj)
    return jsonable_encoder(enumeration_dict)


# Packages
# Endpoint to create a package
@app.post("/packages/")
def create_package(package_data: PackageCreate):
    if package_data.name in db_packages:
        raise HTTPException(status_code=400, detail="Package already exists")

    classes = {db_classes[class_name] for class_name in package_data.classes if class_name in db_classes}
    new_package = Package(
        name=package_data.name,
        classes=classes
    )

    db_packages[package_data.name] = new_package

    return {"id": package_data.name, "message": "Package stored successfully"}

# Endpoint to get all packages
@app.get("/packages/")
def get_packages():
    def package_to_dict(package_obj):
        return {
            "name": package_obj.name,
            "classes": [cls.name for cls in package_obj.classes],
        }

    packages_dict = {name: package_to_dict(pkg) for name, pkg in db_packages.items()}
    return jsonable_encoder(packages_dict)

# Endpoint to get a specific package by name
@app.get("/packages/{package_name}")
def get_package(package_name: str):
    def package_to_dict(package_obj):
        return {
            "name": package_obj.name,
            "classes": [cls.name for cls in package_obj.classes],
        }

    if package_name not in db_packages:
        raise HTTPException(status_code=404, detail="Package not found")

    package_obj = db_packages[package_name]
    package_dict = package_to_dict(package_obj)
    return jsonable_encoder(package_dict)


# Constraints
# Endpoint to create a constraint
@app.post("/constraints/")
def create_constraint(constraint_data: ConstraintCreate):
    if constraint_data.name in db_constraints:
        raise HTTPException(status_code=400, detail="Constraint already exists")

    if constraint_data.context not in db_classes:
        raise HTTPException(status_code=400, detail=f"Context class {constraint_data.context} does not exist")

    new_constraint = Constraint(
        name=constraint_data.name,
        context=db_classes[constraint_data.context],
        expression=constraint_data.expression,
        language=constraint_data.language
    )

    db_constraints[constraint_data.name] = new_constraint

    return {"id": constraint_data.name, "message": "Constraint stored successfully"}

# Endpoint to get all constraints
@app.get("/constraints/")
def get_constraints():
    def constraint_to_dict(constraint_obj):
        return {
            "name": constraint_obj.name,
            "context": constraint_obj.context.name,
            "expression": constraint_obj.expression,
            "language": constraint_obj.language,
        }

    constraints_dict = {name: constraint_to_dict(constr) for name, constr in db_constraints.items()}
    return jsonable_encoder(constraints_dict)

# Endpoint to get a specific constraint by name
@app.get("/constraints/{constraint_name}")
def get_constraint(constraint_name: str):
    def constraint_to_dict(constraint_obj):
        return {
            "name": constraint_obj.name,
            "context": constraint_obj.context.name,
            "expression": constraint_obj.expression,
            "language": constraint_obj.language,
        }

    if constraint_name not in db_constraints:
        raise HTTPException(status_code=404, detail="Constraint not found")

    constraint_obj = db_constraints[constraint_name]
    constraint_dict = constraint_to_dict(constraint_obj)
    return jsonable_encoder(constraint_dict)


# Domain Models
# Endpoint to create a domain model
@app.post("/domainmodels/")
def create_domain_model(domain_model_data: DomainModelCreate, db: Session = Depends(get_db)):
    # Fetch and validate classes
    classes = [db_classes[class_name] for class_name in domain_model_data.types if class_name in db_classes]
    if len(classes) != len(domain_model_data.types):
        raise HTTPException(status_code=400, detail="One or more class names are invalid")

    # Fetch and validate associations
    associations = [db_associations[assoc_name] for assoc_name in domain_model_data.associations if assoc_name in db_associations]
    if len(associations) != len(domain_model_data.associations):
        raise HTTPException(status_code=400, detail="One or more association names are invalid")

    # Fetch and validate generalizations
    generalizations = [
        (db_classes[gen[0]], db_classes[gen[1]]) for gen in domain_model_data.generalizations
        if gen[0] in db_classes and gen[1] in db_classes
    ]
    if len(generalizations) != len(domain_model_data.generalizations):
        raise HTTPException(status_code=400, detail="One or more generalization names are invalid")

    # Fetch and validate enumerations
    enumerations = [db_enumerations[enum_name] for enum_name in domain_model_data.enumerations if enum_name in db_enumerations]
    if len(enumerations) != len(domain_model_data.enumerations):
        raise HTTPException(status_code=400, detail="One or more enumeration names are invalid")

    # Fetch and validate packages
    packages = [db_packages[package_name] for package_name in domain_model_data.packages if package_name in db_packages]
    if len(packages) != len(domain_model_data.packages):
        raise HTTPException(status_code=400, detail="One or more package names are invalid")

    # Fetch and validate constraints
    constraints = [db_constraints[constraint_name] for constraint_name in domain_model_data.constraints if constraint_name in db_constraints]
    if len(constraints) != len(domain_model_data.constraints):
        raise HTTPException(status_code=400, detail="One or more constraint names are invalid")

    new_domain_model = DomainModel(
        name=domain_model_data.name,
        types=set(classes),
        associations=set(associations),
        generalizations=generalizations,
        enumerations=set(enumerations),
        packages=set(packages),
        constraints=set(constraints)
    )

    db_domain_model = DomainModelModel(
        storage_name=domain_model_data.name,
        serialized_data=pickle.dumps(new_domain_model)
    )

    db.add(db_domain_model)
    db.commit()
    db.refresh(db_domain_model)

    return {"id": db_domain_model.id, "message": "Domain Model stored successfully"}

# Endpoint to get a domain model by ID
@app.get("/domainmodels/{model_id}")
def get_domain_model(model_id: int, db: Session = Depends(get_db)):
    db_domain_model = db.query(DomainModelModel).filter(DomainModelModel.id == model_id).first()
    if db_domain_model is not None:
        domain_model = pickle.loads(db_domain_model.serialized_data)
        return {"domain_model": str(domain_model)}
    else:
        raise HTTPException(status_code=404, detail="Domain Model not found")

# Endpoint to generate Pydantic models from a domain model
@app.get("/pydantic/{model_id}")
def get_pydantic(model_id: int, db: Session = Depends(get_db)):
    db_domain_model = db.query(DomainModelModel).filter(DomainModelModel.id == model_id).first()
    if db_domain_model is not None:
        domain_model = pickle.loads(db_domain_model.serialized_data)
        pydantic_model = PydanticGenerator(domain_model)
        pydantic_model.generate()
        return {"pydantic_classes generated"}
    else:
        raise HTTPException(status_code=404, detail="Domain Model not found")

# Run the application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
