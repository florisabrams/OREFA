from OREFA.Parcel import Parcel

perceel = Parcel(id=1, crop='Cereal', soil = 'Loam', deposition=1000, geom= 'Polygon')

perceel.read_config(config_path = '/Users/florisabrams/orefa_assets/config.ini')

perceel.product_conc_prediction(time = 1)