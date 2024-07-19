import pickle
from typing import List, Union, Set
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from enum import Enum
from besser.BUML.metamodel.deployment import (PublicCluster, Service, Deployment, Region, Protocol, ServiceType,
                                              Provider, DeploymentModel, Resources, Application, Container)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./deployment_model_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./deployment_model_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database model for storing serialized deployment models
class DeploymentModelModel(Base):
    __tablename__ = 'deployment_models'
    id = Column(Integer, primary_key=True, index=True)
    storage_name = Column(String, unique=True)
    serialized_data = Column(LargeBinary)

Base.metadata.create_all(bind=engine)

# In-memory databases
db_applications = {}
db_services = {}
db_containers = {}
db_deployments = {}
db_regions = {}
db_clusters = {}
db_deployment_models = {}


# Pydantic models for request data
class ResourcesCreate(BaseModel):
    cpu: int
    memory: int

class ApplicationCreate(BaseModel):
    name: str
    image_repo: str
    port: int
    required_resources: ResourcesCreate
    domain_model: str

class ServiceCreate(BaseModel):
    name: str
    port: int
    target_port: int
    protocol: Protocol
    type: ServiceType
    application_name: str

class ContainerCreate(BaseModel):
    name: str
    application_name: str
    resources_limit: ResourcesCreate

class DeploymentCreate(BaseModel):
    name: str
    replicas: int
    containers: List[str]

class RegionCreate(BaseModel):
    name: str
    zones: List[str] = []

class PublicClusterCreate(BaseModel):
    name: str
    num_nodes: int
    provider: Provider
    config_file: str
    services: List[str]
    deployments: List[str]
    regions: List[str]

class DeploymentModelCreate(BaseModel):
    name: str
    clusters: List[str]


# FastAPIapplication
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create an application
@app.post("/applications/")
def create_application(application_data: ApplicationCreate):
    if application_data.name in db_applications:
        raise HTTPException(status_code=400, detail="Application already exists")

    new_application = Application(
        name=application_data.name,
        image_repo=application_data.image_repo,
        port=application_data.port,
        required_resources=Resources(
            cpu=application_data.required_resources.cpu,
            memory=application_data.required_resources.memory
        ),
        domain_model=application_data.domain_model
    )

    db_applications[application_data.name] = new_application

    return {"name": application_data.name, "message": "Application stored successfully"}


# Endpoint to get all applications
@app.get("/applications/")
def get_applications():
    return jsonable_encoder({name: app.__dict__ for name, app in db_applications.items()})


# Endpoint to create a service
@app.post("/services/")
def create_service(service_data: ServiceCreate):
    if service_data.name in db_services:
        raise HTTPException(status_code=400, detail="Service already exists")

    if service_data.application_name not in db_applications:
        raise HTTPException(status_code=400, detail="Associated application does not exist")

    application = db_applications[service_data.application_name]

    new_service = Service(
        name=service_data.name,
        port=service_data.port,
        target_port=service_data.target_port,
        protocol=service_data.protocol,
        type=service_data.type,
        application=application
    )

    db_services[service_data.name] = new_service

    return {"name": service_data.name, "message": "Service stored successfully"}


# Endpoint to get all services
@app.get("/services/")
def get_services():
    return jsonable_encoder({name: service.__dict__ for name, service in db_services.items()})


# Endpoint to create a container
@app.post("/containers/")
def create_container(container_data: ContainerCreate):
    if container_data.name in db_containers:
        raise HTTPException(status_code=400, detail="Container already exists")

    if container_data.application_name not in db_applications:
        raise HTTPException(status_code=400, detail="Associated application does not exist")

    application = db_applications[container_data.application_name]

    new_container = Container(
        name=container_data.name,
        application=application,
        resources_limit=Resources(
            cpu=container_data.resources_limit.cpu,
            memory=container_data.resources_limit.memory
        )
    )

    db_containers[container_data.name] = new_container

    return {"name": container_data.name, "message": "Container stored successfully"}


# Endpoint to get all containers
@app.get("/containers/")
def get_containers():
    return jsonable_encoder({name: container.__dict__ for name, container in db_containers.items()})


# Endpoint to create a deployment
@app.post("/deployments/")
def create_deployment(deployment_data: DeploymentCreate):
    if deployment_data.name in db_deployments:
        raise HTTPException(status_code=400, detail="Deployment already exists")

    containers = set()
    for container_name in deployment_data.containers:
        if container_name not in db_containers:
            raise HTTPException(status_code=400, detail=f"Container {container_name} does not exist")
        containers.add(db_containers[container_name])

    new_deployment = Deployment(
        name=deployment_data.name,
        replicas=deployment_data.replicas,
        containers=containers
    )

    db_deployments[deployment_data.name] = new_deployment

    return {"name": deployment_data.name, "message": "Deployment stored successfully"}


# Endpoint to get all deployments
@app.get("/deployments/")
def get_deployments():
    return jsonable_encoder({name: deployment.__dict__ for name, deployment in db_deployments.items()})


# Endpoint to create a region
@app.post("/regions/")
def create_region(region_data: RegionCreate):
    if region_data.name in db_regions:
        raise HTTPException(status_code=400, detail="Region already exists")

    new_region = Region(
        name=region_data.name,
        zones=set(region_data.zones)
    )

    db_regions[region_data.name] = new_region

    return {"name": region_data.name, "message": "Region stored successfully"}


# Endpoint to get all regions
@app.get("/regions/")
def get_regions():
    return jsonable_encoder({name: region.__dict__ for name, region in db_regions.items()})


# Endpoint to create a public cluster
@app.post("/clusters/")
def create_public_cluster(cluster_data: PublicClusterCreate):
    if cluster_data.name in db_clusters:
        raise HTTPException(status_code=400, detail="Cluster already exists")

    services = set()
    for service_name in cluster_data.services:
        if service_name not in db_services:
            raise HTTPException(status_code=400, detail=f"Service {service_name} does not exist")
        services.add(db_services[service_name])

    deployments = set()
    for deployment_name in cluster_data.deployments:
        if deployment_name not in db_deployments:
            raise HTTPException(status_code=400, detail=f"Deployment {deployment_name} does not exist")
        deployments.add(db_deployments[deployment_name])

    regions = set()
    for region_name in cluster_data.regions:
        if region_name not in db_regions:
            raise HTTPException(status_code=400, detail=f"Region {region_name} does not exist")
        regions.add(db_regions[region_name])

    new_cluster = PublicCluster(
        name=cluster_data.name,
        num_nodes=cluster_data.num_nodes,
        provider=cluster_data.provider,
        config_file=cluster_data.config_file,
        services=services,
        deployments=deployments,
        regions=regions
    )

    db_clusters[cluster_data.name] = new_cluster

    return {"name": cluster_data.name, "message": "Public cluster stored successfully"}


# Endpoint to get all clusters
@app.get("/clusters/")
def get_clusters():
    return jsonable_encoder({name: cluster.__dict__ for name, cluster in db_clusters.items()})


# Endpoint to create a deployment model
@app.post("/deployment_models/")
def create_deployment_model(deployment_model_data: DeploymentModelCreate, db: Session = Depends(get_db)):
    if db.query(DeploymentModelModel).filter(DeploymentModelModel.storage_name == deployment_model_data.name).first():
        raise HTTPException(status_code=400, detail="Deployment model already exists")

    clusters = set()
    for cluster_data in deployment_model_data.clusters:
        if cluster_data not in db_clusters:
            raise HTTPException(status_code=400, detail=f"Cluster {cluster_data} does not exist")
        clusters.add(db_clusters[cluster_data])

    new_deployment_model = DeploymentModel(
        name=deployment_model_data.name,
        clusters=clusters
    )

    db_deployment_model = DeploymentModelModel(
        storage_name=deployment_model_data.name,
        serialized_data=pickle.dumps(new_deployment_model)
    )
    db.add(db_deployment_model)
    db.commit()
    db.refresh(db_deployment_model)

    return {"id": db_deployment_model.id, "message": "Deployment model stored successfully"}


# Endpoint to get all deployment models
@app.get("/deployment_models/")
def get_deployment_models(db: Session = Depends(get_db)):
    deployment_models = db.query(DeploymentModelModel).all()
    results = []
    for model in deployment_models:
        deployment_model = pickle.loads(model.serialized_data)
        clusters_data = []
        for cluster in deployment_model.clusters:
            services_data = [
                {"name": s.name, "port": s.port, "target_port": s.target_port, "protocol": s.protocol, "type": s.type,
                 "application": s.application.name} for s in cluster.services]
            deployments_data = [{"name": d.name, "replicas": d.replicas, "containers": [c.name for c in d.containers]}
                                for d in cluster.deployments]
            regions_data = [{"name": r.name, "zones": list(r.zones)} for r in cluster.regions]
            clusters_data.append({"name": cluster.name, "num_nodes": cluster.num_nodes, "provider": cluster.provider,
                                  "config_file": cluster.config_file, "services": services_data,
                                  "deployments": deployments_data, "regions": regions_data})
        results.append({"name": deployment_model.name, "clusters": clusters_data})
    return results


# Endpoint to get a specific deployment model by name
@app.get("/deployment_models/{model_name}")
def get_deployment_model(model_name: str, db: Session = Depends(get_db)):
    model = db.query(DeploymentModelModel).filter(DeploymentModelModel.storage_name == model_name).first()
    if not model:
        raise HTTPException(status_code=404, detail="Deployment model not found")

    deployment_model = pickle.loads(model.serialized_data)
    clusters_data = []
    for cluster in deployment_model.clusters:
        services_data = [
            {"name": s.name, "port": s.port, "target_port": s.target_port, "protocol": s.protocol, "type": s.type,
             "application": s.application.name} for s in cluster.services]
        deployments_data = [{"name": d.name, "replicas": d.replicas, "containers": [c.name for c in d.containers]} for d
                            in cluster.deployments]
        regions_data = [{"name": r.name, "zones": list(r.zones)} for r in cluster.regions]
        clusters_data.append({"name": cluster.name, "num_nodes": cluster.num_nodes, "provider": cluster.provider,
                              "config_file": cluster.config_file, "services": services_data,
                              "deployments": deployments_data, "regions": regions_data})
    return {"name": deployment_model.name, "clusters": clusters_data}


# Run the application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)