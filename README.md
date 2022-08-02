# 6221-2182A_LAQM_Rutgers

[Overview] 


This code is the product programmed by undergraduate researcher Libby Morningstar under the supervision of Tsung-Chi Wu, Dr. Jak Chakhalian, & Dr. Mikhail Kareev of the LAQM at Rutgers University. This was completed under the guidance of the PhD candidate, Tsung-Chi Wu, who served as a research mentor for the project.

We undertstand this is not perfected and encourage everyone to collaborate with us to improve it.

Our next steps are to
1. Add other measurement types such as pulse_delta (this is in progress but untested)
2. Add a live plot
3. Make a user-friendly interface

[Installation tips]
Keithley driver is required for proper use. Here is a helpful guide: https://download.tek.com/manual/KUSB-488B-903-01_Sept2018_KUSB-488B-903-01B.pdf
pymeasure was used for the consol log feature. However, it is not necessary to run properly. The code will work fine if you remove any lines starting with log.info and the corresponding imports
If you are having trouble connecting with the instruments, this may be an issue regarding pyvisa
