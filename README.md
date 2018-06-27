# RV Jitter (oscillations & granulation) prediction code
This code is for the prediction of RV jitter due to stellar oscillations and granulation, in terms of various sets of fundamental stellar properties. Details are discribed in Yu et al (2018). If you make use of this code in your work, please cite our paper. 
### Installation

    install dependency
    pip install pandas
    
    (1) Download source and place it in your Python path
    git clone https://github.com/Jieyu126/Jitter.git
    
    (2) Install with pip
    pip install git+https://github.com/Jieyu126/Jitter.git
    
    
### Examples
Example 1:  

         # Predict RV jitter median +/- one sigma, and MC simulation. Note that 
         # the RV jitter is firstly predicted with sole contribution from stellar 
         # oscillations, and then multiplied by a recommended factor, which differs slightly in 
         # different models, to include an additional source, granulation. You are able to 
         # change the factor via the keyword CorFact, e.g. CorFact=1.0
         import RVJitter   
         target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, mass=1.304, masserr=0.064, teff=4963.00, tefferr=80.000).   
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.rv() 

           
Example 2:  

         # Visualize the Monte Carlo simulation. 
         # Predict RV jitter from luminosity, mass, and effectice temperature.     
         import RVJitter   
         target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, mass=1.304, masserr=0.064, teff=4963.00, tefferr=80.000)    
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')   
  
    
Example 3:  

         # Visualize the Monte Carlo simulation. 
         # Predict RV jitter from luminosity, effectice temperature, and surface gravity.    
         import RVJitter  
         target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, teff=4963.00, tefferr=80.000, logg=3.210, loggerr=0.006)  
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')   
     
     
Example 4:  

         # Visualize the Monte Carlo simulation. 
         # Predict RV jitter from effectice temperature and surface gravity   
         import RVJitter  
         target = RVJitter.rvjitter(teff=4963.00, tefferr=80.000,  logg=3.210, loggerr=0.006)  
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')  
    
    
Example 5:  

         # Visualize the Monte Carlo simulation. 
         # Predict RV jitter from luminosity and effectice temperature. In this case, evolutationary stage must be 
         # specified, via the keyword Lgiant, e.g. Lgiant=False
         import RVJitter  
         target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, teff=4963.00, tefferr=80.000, Lgiant=False)  
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')            
     
