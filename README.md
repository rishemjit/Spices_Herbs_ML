# Cuisine-Spice-Disease-Network-Science

<<<<<<< HEAD
=======
Herbs and spices each contain about 3000 phytochemicals on average and there is much traditional knowledge on their health benefits. However, there is a lack of systematic study to understand the relationship among herbs and spices, their phytochemical constituents, their potential health benefits, and their usage in regional cuisines. Here we use a network-based approach to elucidate established relationships and predict novel associations between the phytochemicals present in herbs and spices with health indications. Our top 100 inferred indication-phytochemical relationships rediscover 40% known relationships and 20% that have been inferred via gene-chemical interactions with high confidence. The remaining 40% are hypotheses generated in a principled way for further experimental investigations. We also develop an algorithm to find the minimum set of spices needed to cover a target group of health conditions. Drawing on spice usage patterns in several regional Indian cuisines, and a copy-mutate model for regional cuisine evolution, we characterize the spectrum of health conditions covered by existing regional cuisines. The spectrum of health conditions can expand through the nationalization/globalization of culinary practice.

For more information read out pre-print: https://arxiv.org/abs/2410.17286


Folder Structure
## Crawlers
 * Global_Disease_Burden
 * Malacards
 * SanjeevKapoor/SKapoor
 * Spice_handbook
 * TarlaDalal_English
 * phytochemicals
 
 combine_pharmacydata.ipynb 
 
 Input -> Duke-Source-CSV (Spice-phytochemicals), Spice_handbook/spice2info_spicehnd.json, spice2info_herbhnd.json (spice/herb-indications, also contains scientific names, safety scores, indication score, etc ) 
 
 Output-> spiceherb_phy_nonzeroactivity.json (spice/herb-phytochemical)



>>>>>>> 1422563 (first commit)
## Network_Analysis
