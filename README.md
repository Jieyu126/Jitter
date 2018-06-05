# RV Jitter (oscillations & granulation) prediction code
This code is for the prediction of RV jitter due to stellar oscillations and granulation, in terms of various sets of fundamental stellar properties. Details are discribed in Yu et al (2018). If you make use of this code in your work, please cite our paper. 

### Examples
Example 1:  

         #Generate MC samples using the model F=F(L, M, T)     
         import RVJitter   
         target = RVJitter.rvjitter(lumi=12.006,   
                                    lumierr=1.131,   
                                    mass=1.304,   
                                    masserr=0.064,   
                                    teff=4963.00,   
                                    tefferr=80.000).   
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.rv() 

           
Example 2:  

         #Generate MC samples using the model F=F(L, M, T), and plot out.     
         import RVJitter      
         target = RVJitter.rvjitter(lumi=12.006,   
                                    lumierr=1.131,   
                                    mass=1.304,   
                                    masserr=0.064,   
                                    teff=4963.00,   
                                    tefferr=80.000)    
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')   
  
    
Example 3:  

         #Generate MC samples using the model F=F(L, T, g), and plot out.  
         import RVJitter  
         target = RVJitter.rvjitter(lumi=12.006, 
                                    lumierr=1.131, 
                                    teff=4963.00, 
                                    tefferr=80.000, 
                                    logg=3.210, 
                                    loggerr=0.006)  
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')   
     
     
Example 4:  

         #Generate MC samples using the model F=F(T, g), and plot out.  
         import RVJitter  
         target = RVJitter.rvjitter(teff=4963.00, 
                                    tefferr=80.000, 
                                    logg=3.210, 
                                    loggerr=0.006)  
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')  
    
    
Example 5:  

         #Generate MC samples using the model F=F(L, T), and plot out. Note   
         import RVJitter  
         target = RVJitter.rvjitter(lumi=12.006, 
                                    lumierr=1.131, 
                                    teff=4963.00, 
                                    tefferr=80.000, 
                                    Lgiant=False)  
         sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')            
     
