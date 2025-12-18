from app.database import Base
from sqlalchemy import Column, String, Float
from geoalchemy2 import Geometry

class Farm(Base):
    __tablename__ = "farms"

    cod_imovel = Column(String, index=True, primary_key=True)
    cod_tema = Column(String)
    nom_tema = Column(String)
    mod_fiscal = Column(Float)
    num_area = Column(Float)
    ind_status = Column(String)
    ind_tipo = Column(String)
    des_condic = Column(String)
    municipio = Column(String)
    cod_estado = Column(String)
    dat_criaca = Column(String)
    dat_atuali = Column(String)
    geometry = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
