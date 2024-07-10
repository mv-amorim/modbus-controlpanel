from database.db import Base
from sqlalchemy import Column, Integer, Float, DateTime

class DadoCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadoclp'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    vel = Column(Float)
    #fv01 = Column(Float)
    pit01 = Column(Float)
    fit03 = Column(Float)
    fit02 = Column(Float)
    
    temp_r = Column(Float)
    temp_s = Column(Float)
    temp_t = Column(Float)
    temp_carc = Column(Float)
    
    tensao_rs = Column(Float)
    tensao_st = Column(Float)
    tensao_tr = Column(Float)

    ativa_r = Column(Float)
    ativa_s = Column(Float)
    ativa_t = Column(Float)
    ativa_tot = Column(Float)
    reativa_r = Column(Float)
    reativa_s = Column(Float)
    reativa_t = Column(Float)
    reativa_tot = Column(Float)
    aparente_r = Column(Float)
    aparente_s = Column(Float)
    aparente_t = Column(Float)
    aparente_tot = Column(Float)

    corrente_r = Column(Float)
    corrente_s = Column(Float)
    corrente_t = Column(Float)
    corrente_n = Column(Float)
    corrente_med = Column(Float)
    
    def get_attr_printable_list(self):
        return [self.id,
        self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
        self.temp_r,
        self.temp_s,
        self.temp_t,
        self.temp_carc,
        self.vel,
        self.pit01,
        #self.fv01,
        self.fit03,
        self.fit02,
        self.corrente_r,
        self.corrente_s,
        self.corrente_t,
        self.corrente_n,
        self.corrente_med,
        self.tensao_rs,
        self.tensao_st,
        self.tensao_tr,
        self.ativa_r,
        self.ativa_s,
        self.ativa_t,
        self.ativa_tot,
        self.reativa_r, 
        self.reativa_s,
        self.reativa_t,
        self.reativa_tot,
        self.aparente_r,
        self.aparente_s,
        self.aparente_t,
        self.aparente_tot]