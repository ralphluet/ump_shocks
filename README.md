# Unconventional Monetary Shocks 

This code and the resulting data were generated for Bügel, Hidalgo and Luetticke (2024). So if you use it for your own work, please cite the accompanying paper.

These files generate monetary policy shocks following the narrative approach of Romer and Romer (2004).


In particular, we provide the following three python scripts:
- CMP_shocks_update.py: Updates the extension of Wieland and Yang (2020) to December 2008.
- UMP_shocks.py: Generates a series of unconventional monetary policy shocks as explained in the paper.
- RR_shocks.py: Automatically generates monetary policy shocks up to the latest available Tealbook forecast.

Each file is independent and can be run without the other two files. Thus, for each case, before estimating the shocks, the dataset is created and saved as "RR_data.csv" in the outputs folder. This dataset is similar to that originally produced by Romer and Romer updated up to the latest Tealbook forecast and including the Wu-Xia shadow rate for the ZLB period.

Except for the FOMC_meeting_dates.xlsx and target_ffr.xlsx files, all data files are automatically downloaded from the Philadelphia Fed and Atlanta Fed websites. 

Each script generates the following files for both monthly and quarterly frequency:
- CMP_shocks_update.py --> CMP_shocks.csv : Conventional monetary policy shocks for the period 1969M1-2008M12
- UMP_shocks.py --> UMP_shocks.csv : Unconventional monetary policy shocks for the period 2009M1-2015M12
- RR_shocks.py --> RR_shocks.csv : All monetary policy shocks for the period 1969M1-until latest 
Tealbook forecast.

If you find any errors, please contact me at albert.hidalgo-higueras@uni-tuebingen.de

Albert Hidalgo, May 2024.
