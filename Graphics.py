import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    bienes_inmuebles1=pd.read_csv("bienes_inmuebles.csv")
    filter_1=bienes_inmuebles1[["mongo_id"\
                  ,"fechaAdquiscion"\
                  ,"valorConformeA"\
                  ,"tipoInmueble.valor"\
                  ,"formaPago"\
                  ,"valorAdquisicion.valor"\
                  ,"motivoBaja.clave"\
                  ,"motivoBaja.valor"\
                  ,"flg_valor"              
                 ]].sort_values("valorAdquisicion.valor")

   
    declaraciones_df=pd.read_csv("S1_declaraciuones.csv")
    
    filter_declaracion=\
        declaraciones_df[
                        ["mongo_id"\
                        ,"remuneracionMensualCargoPublico"\
                        ,"otrosIngresosMensualesTotal"\
                        ,"totalIngresosMensualesNetos"\
                        ,"BienesInmubeles"\
                        ,"Nombre"\
                        ,"Apellido 1"\
                        ,"Apellido 2"\
                        ,"nivelEmpleoCargoComision"
                        ]
                        ]
    
    declarcion_propiedadaes_df=pd.merge(filter_declaracion,filter_1, on='mongo_id',how='inner')
    
    declarcion_propiedadaes_contado_df=declarcion_propiedadaes_df[\
                                   (declarcion_propiedadaes_df["flg_valor"]=='>1M')
                                   &
                                   (declarcion_propiedadaes_df["remuneracionMensualCargoPublico"].notnull())
                                   &
                                   (declarcion_propiedadaes_df["formaPago"]=='CONTADO')
                                  ]

########################ESTADISTICAS GENERALES DE LA DATA #############################
    
    ######################## DISTRIBUCION DE INGRESOS NETOS MENSUALES #############################
    plt.figure(figsize=(12, 8))
    sns.distplot(declarcion_propiedadaes_df['totalIngresosMensualesNetos'].dropna()/1000.0, color='blue',bins=100)
    plt.xlim(-250,1000)
    plt.title("DISTRIBUCIÓN DE INGRESOS TOTALES MENSUALES (en miles de pesos) GENERAL",fontsize=14,fontweight="bold")
    plt.xlabel('INGRESOS',fontsize=14,fontweight="bold")
    plt.ylabel('DISTRIBUCIÓN',fontsize=14,fontweight="bold")
    plt.axvline((declarcion_propiedadaes_df['totalIngresosMensualesNetos'].dropna()/1000.0).mean(),
                color='blue',
                ls='--', 
                lw=1.5)
    plt.text(200,0.004,\
             "mean : {}"\
             .format(round((declarcion_propiedadaes_df['totalIngresosMensualesNetos'].dropna()/1000.0)\
             .mean(),2))\
             , fontsize = 14
             ,fontweight="bold")
    plt.savefig('imagen00.png')
    
    ######################## PORCENTAJES DE DISTINTOS TIPOS DE PAGO  #############################

    frecuencias = list(declarcion_propiedadaes_df.groupby(["formaPago"])["formaPago"].count().values)
    nombres = list(declarcion_propiedadaes_df.groupby(["formaPago"])["formaPago"].count().index)
    colores = ['tab:blue', 'tab:cyan', 'tab:gray']
    desfase = (0.1, 0, 0)
    plt.figure(figsize=(10, 5))
    plt.title("DIFERENTES FORMAS DE PAGO PARA LA OBTENCIÓN DE BIENES INMUEBLES",fontsize=14,fontweight="bold")
    plt.pie(frecuencias\
        ,labels=nombres\
        ,autopct="%0.2f %%"\
        ,colors=colores\
        ,explode=desfase\
        ,shadow=True\
        ,startangle=90)
    plt.axis("equal")
    plt.savefig('imagen01.jpg')
    
    ######################## TIPOS DE PROPIEDADES DECLARADAS  #############################
    
    def flat_data(propiedad):
        propiedad_general=None
        if propiedad in ('CASA','DEPARTAMENTO','EDIFICIO'):
            propiedad_general='CASA HABITACION'
        elif propiedad in ('TERRENO','EJIDO','LOTE'):
            propiedad_general='TERRENO'
        else:
            propiedad_general='OTROS'
        return propiedad_general

    declarcion_propiedadaes_df['tipoInmueble.valor']=\
                declarcion_propiedadaes_df['tipoInmueble.valor'].str.strip()

    declarcion_propiedadaes_df['flat_tipoInmueble']=\
                declarcion_propiedadaes_df['tipoInmueble.valor'].\
                apply(lambda x:flat_data(x))
    declarcion_propiedadaes_df

    frecuencias = list(
                   declarcion_propiedadaes_df\
                  .dropna()\
                  .groupby(["flat_tipoInmueble"])["tipoInmueble.valor"]\
                  .count()\
                  .values
                   )
    nombres = list(
            declarcion_propiedadaes_df\
            .dropna()\
            .groupby(["flat_tipoInmueble"])["tipoInmueble.valor"]\
            .count().index
              )
    colores = ['tab:blue', 'tab:red', 'tab:cyan',]
    desfase = (0.1, 0, 0)
    plt.figure(figsize=(10,5))
    plt.title("DIFERENTES BIENES INMUEBLES",fontsize=14,fontweight="bold")
    plt.pie(frecuencias\
        ,labels=nombres\
        ,autopct="%0.2f %%"\
        ,colors=colores\
        ,explode=desfase\
        ,shadow=True\
        ,startangle=90)
    plt.axis("equal")
    plt.savefig('imagen001.jpg')
    
    
#### Generador de imagen 1    
    plt.figure(figsize=(12, 8))
    sns.distplot(declarcion_propiedadaes_contado_df["valorAdquisicion.valor"]/1000000.0, color='purple',)
    plt.xlim(-10,50)
    plt.title("DISTRIBUCIÓN DE PROPIEDADES '>1M' (en millones de pesos) adquiridas de contado",fontsize=14,fontweight="bold")
    plt.xlabel('VALOR DE PROPIEDADES',fontsize=14,fontweight="bold")
    plt.ylabel('DISTRIBUCIÓN',fontsize=14,fontweight="bold")
    plt.axvline((declarcion_propiedadaes_contado_df["valorAdquisicion.valor"]/1000000.0).mean(),
            color='red',
            ls='--', 
            lw=1.5)
    plt.text(10,0.150,\
         "mean : {}"\
         .format(round((declarcion_propiedadaes_contado_df["valorAdquisicion.valor"]/1000000.0)\
         .mean()))\
         , fontsize = 14
         ,fontweight="bold")
    plt.savefig('imagen1.png')
    
#### Generador de imagen 2    
    
    plt.figure(figsize=(12, 8))
    sns.distplot(declarcion_propiedadaes_contado_df["totalIngresosMensualesNetos"]/1000.0, color='blue')
    plt.xlim(-100,1000)
    plt.title("DISTRIBUCIÓN DE INGRESOS TOTALES MENSUALES (en miles de pesos)",fontsize=14,fontweight="bold")
    plt.xlabel('INGRESOS',fontsize=14,fontweight="bold")
    plt.ylabel('DISTRIBUCIÓN',fontsize=14,fontweight="bold")
    plt.axvline((declarcion_propiedadaes_contado_df["totalIngresosMensualesNetos"]/1000.0).mean(),
                color='blue',
                ls='--', 
                lw=1.5)
    plt.text(200,0.008,\
             "mean : {}"\
             .format(round((declarcion_propiedadaes_contado_df["totalIngresosMensualesNetos"]/1000.0)\
             .mean(),2))\
             , fontsize = 14
             ,fontweight="bold")
    plt.savefig('imagen2.png')

    
    declarcion_propiedadaes_credito_df=declarcion_propiedadaes_df[\
                                   (declarcion_propiedadaes_df["flg_valor"]=='>1M')
                                   &
                                   (declarcion_propiedadaes_df["remuneracionMensualCargoPublico"].notnull())
                                   &
                                   (declarcion_propiedadaes_df["formaPago"]=='CRÉDITO')
                                  ]
#### Generador de imagen 3

    plt.figure(figsize=(12, 8))
    sns.distplot(declarcion_propiedadaes_credito_df["valorAdquisicion.valor"]/1000000, color='green')
    plt.xlim(-10,100)
    plt.xlabel('VALOR DE PROPIEDADES',fontsize=14,fontweight="bold")
    plt.ylabel('DISTRIBUCIÓN',fontsize=14,fontweight="bold")
    plt.title("DISTRIBUCIÓN DE PROPIEDADES '>1M' (en millones de pesos) adquiridas con crédito",fontsize=14,fontweight="bold")
    plt.axvline((declarcion_propiedadaes_credito_df["valorAdquisicion.valor"]/1000000).mean(),
                color='green',
                ls='--', 
                lw=1.5)
    plt.text(20,0.050,\
             "mean : {}"\
             .format(round((declarcion_propiedadaes_credito_df["valorAdquisicion.valor"]/1000000)\
             .mean()))\
             , fontsize = 14
             ,fontweight="bold")
    plt.savefig('imagen3.png')

#### Generador de imagen 4
    plt.figure(figsize=(12, 8))
    sns.distplot(declarcion_propiedadaes_credito_df["totalIngresosMensualesNetos"]/1000, color='orange')
    plt.xlim(-100,1000)
    plt.title("DISTRIBUCIÓN DE INGRESOS TOTALES MENSUALES (en miles de pesos)",fontsize=14,fontweight="bold")
    plt.xlabel('INGRESOS',fontsize=14,fontweight="bold")
    plt.ylabel('DISTRIBUCIÓN',fontsize=14,fontweight="bold")
    plt.axvline((declarcion_propiedadaes_credito_df["totalIngresosMensualesNetos"]/1000).mean(),
                color='orange',
                ls='--', 
                lw=1.5)
    plt.text(200,0.008,\
             "mean : {}"\
             .format(round((declarcion_propiedadaes_credito_df["totalIngresosMensualesNetos"]/1000)\
             .mean(),2))\
             , fontsize = 14
             ,fontweight="bold")
    plt.savefig('imagen4.png')

    print('###################################################################')
    print('SECCION DONDE SE EXPORTAN LOS DATAFRAMES PARA ANOMALIAS PARA BIENES INMUEBLES')
    print('###################################################################')
       
    
    print('###################################################################')
    print('ANOMALIAS BIENES INMUEBLES DE CONTADO')
    print('###################################################################')
    df_yellow=declarcion_propiedadaes_contado_df[\
                                       (declarcion_propiedadaes_contado_df["valorAdquisicion.valor"]>=1000000.0)
                                       &
                                       (declarcion_propiedadaes_contado_df["valorAdquisicion.valor"]<=6000000.0)
                                       &
                                       (declarcion_propiedadaes_contado_df["totalIngresosMensualesNetos"]<=100000.0)
                                      ]
    df_yellow["Anomaly_level"]='yellow'
    
    df_red=declarcion_propiedadaes_contado_df[\
                                   (declarcion_propiedadaes_contado_df["valorAdquisicion.valor"]>6000000.0)
                                   &
                                   (declarcion_propiedadaes_contado_df["totalIngresosMensualesNetos"]<=100000.0)
                                  ]
    df_red["Anomaly_level"]='red'
    df_anomaly_contado=pd.concat([df_yellow,df_red])
    df_contado_verde=declarcion_propiedadaes_df[\
                            (declarcion_propiedadaes_df["flg_valor"]!='>1M')
                            &
                            (declarcion_propiedadaes_df["remuneracionMensualCargoPublico"].notnull())
                            &
                            (declarcion_propiedadaes_df["formaPago"]=='CONTADO')
                          ]

    df_contado_verde["Anomaly"]=0.0
    df_contado_verde["Anomaly_level"]='green'
    
    df_anomaly_contado2=pd.concat([df_anomaly_contado,df_contado_verde])
    
    df_anomaly_contado_to_export=df_anomaly_contado2[[
                                                 "mongo_id",\
                                                 "totalIngresosMensualesNetos",\
                                                 "valorAdquisicion.valor",\
                                                 "formaPago",\
                                                 "Nombre",\
                                                 "Apellido 1",\
                                                 "Apellido 2",\
                                                 'Anomaly_level'\
                                                 ]]
    print('###################################################################')
    print('EXPORTANDO CSV ANOMALIAS EN BIENES INMUEBLES CONTADO')
    print('###################################################################')
    df_anomaly_contado_to_export.to_csv("anomaly_bienesInmuebles_contado.csv")
    
    
    print('###################################################################')
    print('ANOMALIAS BIENES INMUEBLES DE CREDITO')
    print('###################################################################')
    
    df_yellow_credit=declarcion_propiedadaes_credito_df[\
                                   (declarcion_propiedadaes_credito_df["valorAdquisicion.valor"]>=1000000.0)
                                   &
                                   (declarcion_propiedadaes_credito_df["valorAdquisicion.valor"]<=7000000.0)
                                   &
                                   (declarcion_propiedadaes_credito_df["totalIngresosMensualesNetos"]<=105000.0)
                                  ]
    df_yellow_credit["Anomaly_level"]='yellow'


    df_red_credit=declarcion_propiedadaes_credito_df[\
                                       (declarcion_propiedadaes_credito_df["valorAdquisicion.valor"]>7000000.0)
                                       &
                                       (declarcion_propiedadaes_credito_df["totalIngresosMensualesNetos"]<=105000.0)
                                      ]
    df_red_credit["Anomaly_level"]='red'
    
    df_anomaly_credito=pd.concat([df_yellow_credit,df_red_credit])
    
    df_credito_verde=declarcion_propiedadaes_df[\
                                (declarcion_propiedadaes_df["flg_valor"]!='>1M')
                                &
                                (declarcion_propiedadaes_df["remuneracionMensualCargoPublico"].notnull())
                                &
                                (declarcion_propiedadaes_df["formaPago"]=='CRÉDITO')
                              ]

    df_credito_verde["Anomaly"]=0.0
    df_credito_verde["Anomaly_level"]='green'
    
    df_anomaly_credito2=pd.concat([df_anomaly_credito,df_credito_verde])
    
    df_anomaly_credito_to_export=df_anomaly_credito2[[
                                                 "mongo_id",\
                                                 "totalIngresosMensualesNetos",\
                                                 "valorAdquisicion.valor",\
                                                 "formaPago",\
                                                 "Nombre",\
                                                 "Apellido 1",\
                                                 "Apellido 2",\
                                                 'Anomaly_level'\
                                                 ]]
    
    print('###################################################################')
    print('EXPORTANDO CSV ANOMALIAS EN BIENES INMUEBLES CREDITO')
    print('###################################################################')
    
    df_anomaly_credito_to_export.to_csv("anomaly_bienesInmuebles_credito.csv")
    
    print('###################################################################')
    print('SECCION DE VEHÍCULOS')
    print('###################################################################')
    
    df_vehiculos=pd.read_csv("vehiculos.csv")
    declaraciones_df=pd.read_csv("S1_declaraciuones.csv")

    df_vehiculos2=df_vehiculos[[\
              "mongo_id"\
              ,'anio'\
              ,'tipoVehiculo.valor'\
              ,'formaAdquisicion.valor'\
              ,'valorAdquisicion.valor'\
              ,'valorAdquisicion.moneda'\
              ,'formapago'
             ]]
    filter_declaracion=\
        declaraciones_df[
                        ["mongo_id"\
                        ,"remuneracionMensualCargoPublico"\
                        ,"otrosIngresosMensualesTotal"\
                        ,"totalIngresosMensualesNetos"\
                        ,"BienesInmubeles"\
                        ,"Nombre"\
                        ,"Apellido 1"\
                        ,"Apellido 2"\
                        ,"nivelEmpleoCargoComision"
                        ]
                        ]

    declarcion_vehiculos_df=pd.merge(filter_declaracion,df_vehiculos2, on='mongo_id',how='inner')

    def flat_data_moneda(moneda):
        moneda_ajustada=None
        if moneda in ('AFN','USN','USS','XDR'):
            moneda_ajustada='OTRA'
        else:
            moneda_ajustada=moneda
        return moneda_ajustada

    declarcion_vehiculos_df['valorAdquisicion.moneda']=\
                declarcion_vehiculos_df['valorAdquisicion.moneda'].str.strip()

    declarcion_vehiculos_df["moneda_ajustada"]\
                        =declarcion_vehiculos_df["valorAdquisicion.moneda"]\
                        .apply(lambda x : flat_data_moneda(x))
    
    
    print('###################################################################')
    print('PRIMER GRÁFICO')
    print('###################################################################')
    
    frecuencias = list(
                   declarcion_vehiculos_df.\
                   groupby(["moneda_ajustada"])["moneda_ajustada"].\
                   count().\
                   values
                  )
    nombres = list(
            declarcion_vehiculos_df.\
            groupby(["moneda_ajustada"])["moneda_ajustada"].\
            count().\
            index
            )
    colores = ['tab:red', 'tab:grey', 'tab:cyan']
    desfase = (0.5, 1.0, 0)
    plt.figure(figsize=(10, 5))
    plt.title("DIFERENTES MONEDAS CON LAS QUE SE HAN PAGADO LOS VEHÍCULOS DECLARADOS",fontsize=14,fontweight="bold")
    plt.pie(frecuencias\
        ,labels=nombres\
        ,autopct="%0.2f %%"\
        ,colors=colores\
        ,explode=desfase\
        ,shadow=True\
        ,startangle=200)
    plt.axis("equal")
    plt.savefig('imagen_general_vehiculos_0.png')
    
    
    print('###################################################################')
    print('SEGUNDO GRÁFICO')
    print('###################################################################')
    
    def flat_data_vehiculo(vehiculo):
        vehiculo_ajustado=None
        if vehiculo in ('AUTOMOVIL/MOTOCICLETA',\
                    'AUTOMOVIL SUV',\
                    'AUTOMÓVIL/MOTOCICLETA',\
                    'AUTOMÃVIL/MOTOCICLETA',\
                    'CAMIONETA SUBURBAN',\
                    'MOTOCICLETA',\
                    'CAMIONETA DOBLE CABINA',\
                    'COMIONETA 3 TONELADAS',\
                    'PIKUPS',\
                    'SUV',\
                    'VEHICULO',\
                    'VEHICULO AUTOMOTOR'
                    ):
            vehiculo_ajustado='AUTOMOVIL/CAMIONETA/MOTOCICLETA'   
        elif vehiculo in (
                        'NINGUNA',\
                        'NINGUNO',\
                        'NO CUENTO CON VEHICULO',\
                        'NO TENGO NINGÚN TIPO DE VEHICULO.'
                        ):
            vehiculo_ajustado='NINGUNO'
        else:
            vehiculo_ajustado='OTROS'
        
        return vehiculo_ajustado

    declarcion_vehiculos_df['tipoVehiculo.valor']=\
                    declarcion_vehiculos_df['tipoVehiculo.valor'].str.strip()

    declarcion_vehiculos_df["vehiculo_ajustado"]\
                            =declarcion_vehiculos_df["tipoVehiculo.valor"]\
                            .apply(lambda x : flat_data_vehiculo(x))


    frecuencias = list(
                       declarcion_vehiculos_df.\
                       groupby(["vehiculo_ajustado"])["vehiculo_ajustado"].\
                       count().\
                       values
                      )
    nombres = list(
                declarcion_vehiculos_df.\
                groupby(["vehiculo_ajustado"])["vehiculo_ajustado"].\
                count().\
                index
                )
    colores = ['tab:orange', 'tab:grey', 'tab:cyan']
    desfase = (0.2,0.1,0)
    plt.figure(figsize=(10, 5))
    plt.title("VEHÍCULOS DECLARADOS",fontsize=14,fontweight="bold")
    plt.pie(frecuencias\
            ,labels=nombres\
            ,autopct="%0.2f %%"\
            ,colors=colores\
            ,explode=desfase\
            ,shadow=True\
            ,startangle=45)
    plt.axis("equal")
    plt.savefig('imagen_general_vehiculos_1.png')
    
    print('###################################################################')
    print('TERCER GRÁFICO')
    print('###################################################################')
    
    plt.figure(figsize=(12, 8))
    sns.distplot(declarcion_vehiculos_df["valorAdquisicion.valor"]/1000, color='red')
    plt.xlim(-5000,50000)
    plt.title("DISTRIBUCIÓN DE PRECIOS DE VEHÍCULOS DECLARADOS (en miles de pesos)",fontsize=14,fontweight="bold")
    plt.xlabel('PRECIO',fontsize=14,fontweight="bold")
    plt.ylabel('DISTRIBUCIÓN',fontsize=14,fontweight="bold")
    plt.axvline((declarcion_vehiculos_df["valorAdquisicion.valor"]/1000).mean(),
            color='red',
            ls='--', 
            lw=1.5)
    plt.text(5000,0.00015,\
            "mean : {}"\
            .format(round((declarcion_vehiculos_df["valorAdquisicion.valor"]/1000)\
            .mean(),2))\
            , fontsize = 14
            ,fontweight="bold")
    
    plt.savefig('imagen_general_vehiculos_2.png')


if __name__=='__main__':
    main()
