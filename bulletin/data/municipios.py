import pandas as pd
from unidecode import unidecode
from os.path import dirname, join

from bulletin import __file__ as __root__
from bulletin.commom.normalize import normalize_text

def read(path:str=join(dirname(__root__),'tmp','estimativa_dou.xls'), sheet: str="Municípios", skiprows: int=1, nrows: int=5570):
	#read excel sheet from ibge
	municipios = pd.read_excel(path,sheet,skiprows=skiprows,nrows=nrows)

	#normalize columns to remove non ascii characteres and lower string
	municipios.columns = [ normalize_text(x) for x in municipios.columns ]

	#rename columns labels
	municipios = municipios.rename(columns={'nome_do_municipio':'mun_nome','populacao_estimada':'populacao'})

	#normalize data to remove artifacts and standardize data
	municipios['populacao'] = municipios['populacao'].apply(lambda x: int(str(x).split("(")[0]))
	municipios['cod_uf'] = municipios['cod_uf'].apply(normalize_text)
	municipios['cod_munic'] = municipios['cod_munic'].apply(lambda x: str(x)[:len(str(x))-1].zfill(4))

	#generate  and insert ibge-6 code join cod_uf and cod_munic
	ibge = list(map(lambda cod_uf,cod_munic: int(cod_uf+cod_munic),  municipios['cod_uf'], municipios['cod_munic']))
	municipios.insert(0,'ibge',ibge)

	#select and save columns to HDF5 format
	municipios = municipios[['ibge','uf','mun_nome','populacao']]
	# municipios.to_hdf(join(dirname(__root__),'resources','database','municipios.h5'),'municipios',index=None, encoding='utf-8-sig')
	municipios.to_pickle(join(dirname(__root__),'resources','database','municipios.pkl'))

	return municipios

def load():
	return pd.read_pickle(join(dirname(__root__),'resources','database','municipios.pkl'))
