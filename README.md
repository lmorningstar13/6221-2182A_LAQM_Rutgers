# SR830/335/6221-2182A_LAQM_Rutgers

[Overview] 

**Keithley.py**

This code is for using Keithley instruments 6221 and 2182A to perform a delta measurement and save the data with little human interaction. As of 08/02/2022, this code will run and collect data for a delta measurement into ten files, each file holding 65536 data points (the maximum data the 6221 instrument buffer can contain), over a time period of 25 hours after the user runs the file. Our goal is to create a user-friendly interface that can complete multiple measurments indefinitely for these instruments. 

**CodeNew.Py**

This code improves on the *Keithley.py* file. In particular, compatability is added with the SR830 Lock-In Amplifier, Lakeshore 335 Temperature Controller, and Pulse Delta Mode with the same Keithley Instruments (6221 and 2182A). The Delta mode was also configured to work with more instruments. The length of time that data is taken for can be adjusted by modifying one command. For the Keithley instruments, the CSV file outputs time, voltage, temperature, PID parameters, ramp rate, and setpoint. For the Lock-In Amplifier, the CSV file outputs time, voltage, frequency, Channel 1, Channel 2, Sensitivity, Temperature, PID, ramp rate, and setpoint. There is an auto-sensitivity method in the code that adjusts the sensitivity from the provided values according to a function (less than or equal to 10 times the corresponding voltage). Additionally, depending on what instrument is connected (Lock-in or Keithley), the corresponding machine code is automatically used. This code greatly facilitates the experimentation process and allows for much easier analysis of various properties, such as phase-transitions.

These files were programmed by undergraduate researchers Libby Morningstar and Nidhish Sharma under the supervision of Tsung-Chi Wu, Dr. Jak Chakhalian, & Dr. Mikhail Kareev of the LAQM at Rutgers University. This was completed under the guidance of the PhD candidate, Tsung-Chi Wu, who served as a research mentor for the project.

We undertstand this is not perfected and encourage everyone to collaborate with us to improve it.

Our next steps are to
1. Test other measurement types such as the 2-W technique
2. Add a live plot
3. Make a user-friendly interface

**[Installation tips]**

-Keithley driver is required for proper use. Here is a helpful guide: https://download.tek.com/manual/KUSB-488B-903-01_Sept2018_KUSB-488B-903-01B.pdf

-Pymeasure was used for the consol log feature. However, it is not necessary to run properly. The code will work fine if you remove any lines starting with log.info and the corresponding imports

-If you are having trouble connecting with the instruments, this may be an issue regarding pyvisa (the FAQ is active and very helpful)

-Contact Nidhish Sharma - *ns1300@scarletmail.rutgers.edu* for help with setting up instruments, code errors, or any other general questions. 
