# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_Parcel.ipynb.

# %% auto 0
__all__ = ['Parcel']

# %% ../nbs/00_Parcel.ipynb 3
# Pydantic for polygon is difficult

class Parcel():
    def __init__(self, id, crop, soil, deposition, geom, config = None):
        self.id = id
        self.crop = crop
        self.soil = soil
        self.deposition = deposition
        self.geom = geom
        self.config = None
        
    def __repr__(self):
        return "<Parcel('%s', '%s', '%s', '%s')>" % (self.crop, self.soil, self.deposition, self.geom)
    
    def read_config(self, config_path):
        # import the config file
        import configparser
        config = configparser.ConfigParser()
        config.read(config_path)
        self.config = config
    def product_conc_prediction(self, config, time):
            import json
            from math import exp, log

            with open(self.config["ModelInputs"]["CropGroupProperties"], 'r') as crop_group_to_properties:
                dict_crop_group_to_properties = json.load(crop_group_to_properties)
            with open(self.config["ModelInputs"]["SoilGroupProperties"], 'r') as soil_properties:
                dict_soil_to_properties = json.load(soil_properties)
            with open(self.config["ModelInputs"]["RnProperties"], 'r') as RN_properties:
                dict_RN_properties = json.load(RN_properties)
            with open(self.config["ModelInputs"]["TF"], 'r') as TF:
                TF_dict = json.load(TF)
            with open(self.config["ModelInputs"]["CfilLevel"], 'r') as cfil:
                intervention_levels = json.load(cfil)
            with open(self.config["ModelInputs"]["AnimalFeedIntake"], 'r') as feed:
                animal_daily_feed_intake = json.load(feed)
            with open(self.config["ModelInputs"]["AnimalDryWeight"], 'r') as dry:
                dict_dry_weight_animal_feed = json.load(dry)

            root_zone_depth = float(dict_crop_group_to_properties.get(self.crop).get('root_depth'))
            soil_density = float(dict_soil_to_properties.get(self.soil).get('density'))
            net_infiltration = float(
                dict_soil_to_properties.get(self.soil).get("Net_infiltration_rate"))
            Volumetric_water = float(
                dict_soil_to_properties.get(self.soil).get("Volumetric_water_content"))
            kd = float(dict_soil_to_properties.get(self.soil).get("kd"))

            leaching_rate = net_infiltration / (root_zone_depth * (Volumetric_water + (soil_density * kd)))
            decay_rate = float(dict_RN_properties.get("Cs-137").get("decay_rate"))

            # as long as the time_to_clean field is not field contin to search for the year where concentration is below CFIL
            # time untill concentration is = fill vegetation

            # best to have real values for soil concenrtation, but we divide the surface contamination over 30 cm soil with density of 135O kg/m3
            # Also possible to use this factor of 1/53, it is a homogenous distribution of cesium over the soil based on a japanese paper
            current_soil_concentration = float(self.deposition) / (soil_density * float(root_zone_depth)) * exp(-(decay_rate + leaching_rate) * time)
            concentration_in_vegetation = float(current_soil_concentration)  * float(TF_dict.get(self.crop).get(self.soil))

            if self.crop in ["pasture", "feed crop"]:
                if self.crop in ["pasture"]:
                    ratio_soiltopasture = animal_daily_feed_intake.get('cow').get(self.crop).get('soil')
                    pasture_intake = animal_daily_feed_intake.get('cow').get(self.crop).get('grass')
                    pasture_intake_fresh = float(pasture_intake) / float(dict_dry_weight_animal_feed.get('pasture'))

                    transfer_to_milk = 0.0052
                    transfer_to_meat = 0.019

                    milk_concentration = ((concentration_in_vegetation + (
                                current_soil_concentration * float(ratio_soiltopasture))) * float(
                        pasture_intake_fresh)) * transfer_to_milk
                    meat_concentration = ((concentration_in_vegetation + (
                            current_soil_concentration * float(ratio_soiltopasture))) * float(
                        pasture_intake_fresh)) * transfer_to_meat

                else:
                    pasture_intake = animal_daily_feed_intake.get('cow').get(self.crop)
                    pasture_intake_fresh = float(pasture_intake) / float(dict_dry_weight_animal_feed.get('pasture'))
                    transfer_to_milk = 0.0052
                    transfer_to_meat = 0.019

                    milk_concentration = ((concentration_in_vegetation) * pasture_intake_fresh) * transfer_to_milk
                    meat_concentration = ((concentration_in_vegetation) * pasture_intake_fresh) * transfer_to_meat

                # Will always be higher than milk
                self.product_concentration = milk_concentration

                if self.product_concentration < float(intervention_levels.get('milk')):
                    self.remediation_needed = False
                else:
                    self.remediation_needed = True


            else:
                self.product_concentration = concentration_in_vegetation

                if self.product_concentration < float(intervention_levels.get('crops')):
                    self.remediation_needed = False
                else:
                    self.remediation_needed = True

            return
