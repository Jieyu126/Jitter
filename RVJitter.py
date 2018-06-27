import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import AutoMinorLocator




class rvjitter(object):
      """
         Predicting RV jitter due to stellar oscillations, in terms of fundamental stellar properties.
         Example 1:
                  #Generate MC samples using the model F=F(L, M, T)
                  import RVJitter
                  target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, mass=1.304, masserr=0.064, teff=4963.00, tefferr=80.000)
                  sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.rv()

         Example 2:
                  #Generate MC samples using the model F=F(L, M, T) and plot out.
                  import RVJitter
                  target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, mass=1.304, masserr=0.064, teff=4963.00, tefferr=80.000)
                  sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png') 

         Example 3:
                  #Generate MC samples using the model F=F(L, T, g) and plot out.
                  import RVJitter
                  target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, teff=4963.00, tefferr=80.000, logg=3.210, loggerr=0.006)
                  sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png') 
                          
         Example 4:
                  #Generate MC samples using the model F=F(T, g) and plot out.
                  import RVJitter
                  target = RVJitter.rvjitter(teff=4963.00, tefferr=80.000, logg=3.210, loggerr=0.006)
                  sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')

         Example 5:
                  #Generate MC samples using the model F=F(L, T) and plot out. Note 
                  import RVJitter
                  target = RVJitter.rvjitter(lumi=12.006, lumierr=1.131, teff=4963.00, tefferr=80.000, Lgiant=False)
                  sigmarv, sigmarvperr, sigmarvmerr, mcsigmarv = target.plot(figshow=True, figsave=True, figname='jitter.png')          

      """
 

      def __init__(self, lumi=None, lumierr=None, mass=None, masserr=None, teff=None, tefferr=None, logg=None, loggerr=None, Lgiant=None, CorFact=None):
          self.teffsun = 5777.
          self.gravsun = 10**4.44
          self.nsample = int(100000)
          self.loggthreshold = 3.5

          # The variable "CorFact" denotes a correction factor used to convert the RV jitter due to 
          # only stellar oscillations to the jitter due to both stellar oscilations and granulation. 
          # A correction factor of 1.6 is recommended. 
          if CorFact is not None:
             self.CorFact = CorFact
          #else:
          #   self.CorFact = 1.6



          if (lumi is not None) & (lumierr is not None): 
             self.lumi = lumi
             self.lumierr = lumierr
          if (mass is not None) & (masserr is not None):    
             self.mass = mass
             self.masserr = masserr
          if (teff is not None) & (tefferr is not None):
             self.teff = teff
             self.tefferr = tefferr
          if (logg is not None) & (loggerr is not None):
             self.grav = 10**logg
             self.graverr = loggerr/np.log(10)/logg
          if Lgiant is not None:
             self.Lgiant=Lgiant


          # Check a target is either either a dwarf/subgiant or giant.
          if hasattr(self,'Lgiant'): 
               if self.Lgiant==True: logg=2.44  
               if self.Lgiant==False: logg=4.44 #only used for representing either a dwarf/subgiant or giant.
          elif hasattr(self,'grav'): logg =  np.log10(self.grav)
          elif hasattr(self,'lumi') & hasattr(self,'mass') & hasattr(self,'teff'): 
               logg = np.log10(self.gravsun)-np.log10(self.lumi)+np.log10(self.mass)+4.*np.log10(self.teff/self.teffsun)
          else:  
               print('Input data does not apply to any of the four models')
               raise sys.exit()



          # Read in fitted parameters and their uncertainties.
          rms = pd.read_csv('fitparamsrms.csv')
          rms.loc[np.where(rms['std']<0.005)[0], 'std'] = 0.01
          
          if logg<=np.log10(self.loggthreshold):
             self.lmt_alpha = rms[rms.parameter=='RV_RMS_All_Giant_LMT_alpha'].iloc[0]['value']          
             self.lmt_beta =  rms[rms.parameter=='RV_RMS_All_Giant_LMT_beta'].iloc[0]['value'] 
             self.lmt_gamma = rms[rms.parameter=='RV_RMS_All_Giant_LMT_gamma'].iloc[0]['value']
             self.lmt_delta = rms[rms.parameter=='RV_RMS_All_Giant_LMT_delta'].iloc[0]['value']
             self.lmt_alpha_sig = rms[rms.parameter=='RV_RMS_All_Giant_LMT_alpha'].iloc[0]['std']
             self.lmt_beta_sig =  rms[rms.parameter=='RV_RMS_All_Giant_LMT_beta'].iloc[0]['std'] 
             self.lmt_gamma_sig = rms[rms.parameter=='RV_RMS_All_Giant_LMT_gamma'].iloc[0]['std']
             self.lmt_delta_sig = rms[rms.parameter=='RV_RMS_All_Giant_LMT_delta'].iloc[0]['std']

             self.ltg_alpha =   rms[rms.parameter=='RV_RMS_All_Giant_LTg_alpha'].iloc[0]['value']      
             self.ltg_beta =    rms[rms.parameter=='RV_RMS_All_Giant_LTg_beta'].iloc[0]['value']     
             self.ltg_delta =   rms[rms.parameter=='RV_RMS_All_Giant_LTg_gamma'].iloc[0]['value']   
             self.ltg_epsilon = rms[rms.parameter=='RV_RMS_All_Giant_LTg_delta'].iloc[0]['value']   
             self.ltg_alpha_sig =   rms[rms.parameter=='RV_RMS_All_Giant_LTg_alpha'].iloc[0]['std']
             self.ltg_beta_sig =    rms[rms.parameter=='RV_RMS_All_Giant_LTg_beta'].iloc[0]['std']  
             self.ltg_delta_sig =   rms[rms.parameter=='RV_RMS_All_Giant_LTg_gamma'].iloc[0]['std']  
             self.ltg_epsilon_sig = rms[rms.parameter=='RV_RMS_All_Giant_LTg_delta'].iloc[0]['std']   

             self.tg_alpha =    rms[rms.parameter=='RV_RMS_All_Giant_Tg_alpha'].iloc[0]['value']  
             self.tg_delta =    rms[rms.parameter=='RV_RMS_All_Giant_Tg_beta'].iloc[0]['value']   
             self.tg_epsilon =  rms[rms.parameter=='RV_RMS_All_Giant_Tg_gamma'].iloc[0]['value']   
             self.tg_alpha_sig =   rms[rms.parameter=='RV_RMS_All_Giant_Tg_alpha'].iloc[0]['std']  
             self.tg_delta_sig =   rms[rms.parameter=='RV_RMS_All_Giant_Tg_beta'].iloc[0]['std']   
             self.tg_epsilon_sig = rms[rms.parameter=='RV_RMS_All_Giant_Tg_gamma'].iloc[0]['std']      
     
             self.lt_alpha =  rms[rms.parameter=='RV_RMS_All_Giant_LT_alpha'].iloc[0]['value']   
             self.lt_beta =   rms[rms.parameter=='RV_RMS_All_Giant_LT_beta'].iloc[0]['value']   
             self.lt_delta =  rms[rms.parameter=='RV_RMS_All_Giant_LT_gamma'].iloc[0]['value']  
             self.lt_alpha_sig =  rms[rms.parameter=='RV_RMS_All_Giant_LT_alpha'].iloc[0]['std'] 
             self.lt_beta_sig =   rms[rms.parameter=='RV_RMS_All_Giant_LT_beta'].iloc[0]['std'] 
             self.lt_delta_sig =  rms[rms.parameter=='RV_RMS_All_Giant_LT_gamma'].iloc[0]['std']

          else:
             self.lmt_alpha = rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_alpha'].iloc[0]['value']          
             self.lmt_beta =  rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_beta'].iloc[0]['value'] 
             self.lmt_gamma = rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_gamma'].iloc[0]['value']
             self.lmt_delta = rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_delta'].iloc[0]['value']
             self.lmt_alpha_sig = rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_alpha'].iloc[0]['std']
             self.lmt_beta_sig =  rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_beta'].iloc[0]['std'] 
             self.lmt_gamma_sig = rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_gamma'].iloc[0]['std']
             self.lmt_delta_sig = rms[rms.parameter=='RV_RMS_All_Dwarf_LMT_delta'].iloc[0]['std']

             self.ltg_alpha =   rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_alpha'].iloc[0]['value']      
             self.ltg_beta =    rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_beta'].iloc[0]['value']     
             self.ltg_delta =   rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_gamma'].iloc[0]['value']   
             self.ltg_epsilon = rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_delta'].iloc[0]['value']   
             self.ltg_alpha_sig =   rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_alpha'].iloc[0]['std']
             self.ltg_beta_sig =    rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_beta'].iloc[0]['std']  
             self.ltg_delta_sig =   rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_gamma'].iloc[0]['std']  
             self.ltg_epsilon_sig = rms[rms.parameter=='RV_RMS_All_Dwarf_LTg_delta'].iloc[0]['std']   

             self.tg_alpha =    rms[rms.parameter=='RV_RMS_All_Dwarf_Tg_alpha'].iloc[0]['value']  
             self.tg_delta =    rms[rms.parameter=='RV_RMS_All_Dwarf_Tg_beta'].iloc[0]['value']   
             self.tg_epsilon =  rms[rms.parameter=='RV_RMS_All_Dwarf_Tg_gamma'].iloc[0]['value']   
             self.tg_alpha_sig =   rms[rms.parameter=='RV_RMS_All_Dwarf_Tg_alpha'].iloc[0]['std']  
             self.tg_delta_sig =   rms[rms.parameter=='RV_RMS_All_Dwarf_Tg_beta'].iloc[0]['std']   
             self.tg_epsilon_sig = rms[rms.parameter=='RV_RMS_All_Dwarf_Tg_gamma'].iloc[0]['std']      
     
             self.lt_alpha =  rms[rms.parameter=='RV_RMS_All_Dwarf_LT_alpha'].iloc[0]['value']   
             self.lt_beta =   rms[rms.parameter=='RV_RMS_All_Dwarf_LT_beta'].iloc[0]['value']   
             self.lt_delta =  rms[rms.parameter=='RV_RMS_All_Dwarf_LT_gamma'].iloc[0]['value']  
             self.lt_alpha_sig =  rms[rms.parameter=='RV_RMS_All_Dwarf_LT_alpha'].iloc[0]['std'] 
             self.lt_beta_sig =   rms[rms.parameter=='RV_RMS_All_Dwarf_LT_beta'].iloc[0]['std'] 
             self.lt_delta_sig =  rms[rms.parameter=='RV_RMS_All_Dwarf_LT_gamma'].iloc[0]['std']





      def rv(self): 
          # Run Monte Carlo simulation
          # Model 1: rvjitter = rvjitter(L, M, T)
          if hasattr(self,'lumi') & hasattr(self,'mass') & hasattr(self,'teff'):
             np.random.seed(seed=1) #makes the random numbers predictable
             mclumi = self.lumi+np.random.randn(self.nsample)*self.lumierr 
             np.random.seed(seed=2)
             mcmass = self.mass+np.random.randn(self.nsample)*self.masserr
             np.random.seed(seed=3)
             mcteff = self.teff+np.random.randn(self.nsample)*self.tefferr
             np.random.seed(seed=4)
             mcalpha = self.lmt_alpha+np.random.randn(self.nsample)*self.lmt_alpha_sig
             np.random.seed(seed=5)
             mcbeta  = self.lmt_beta+np.random.randn(self.nsample)*self.lmt_beta_sig          
             np.random.seed(seed=6)
             mcgamma = self.lmt_gamma+np.random.randn(self.nsample)*self.lmt_gamma_sig
             np.random.seed(seed=7)
             mcdelta = self.lmt_delta+np.random.randn(self.nsample)*self.lmt_delta_sig
             # Compute the jitter samples              
             if hasattr(self,'CorFact'): 
                mcsigmarv = self.CorFact * mcalpha * mclumi**mcbeta * mcmass**mcgamma * (mcteff/self.teffsun)**mcdelta
             else: 
                mcsigmarv = 1.93 * mcalpha * mclumi**mcbeta * mcmass**mcgamma * (mcteff/self.teffsun)**mcdelta




          # Model 2: rvjitter = rvjitter(L, T, g)
          elif hasattr(self,'lumi') & hasattr(self,'teff') & hasattr(self,'grav'): 
             np.random.seed(seed=8) #makes the random numbers predictable
             mclumi = self.lumi+np.random.randn(self.nsample)*self.lumierr 
             np.random.seed(seed=9)
             mcteff = self.teff+np.random.randn(self.nsample)*self.tefferr
             np.random.seed(seed=10)
             mcgrav = self.grav+np.random.randn(self.nsample)*self.graverr
             np.random.seed(seed=11)
             mcalpha = self.ltg_alpha+np.random.randn(self.nsample)*self.ltg_alpha_sig
             np.random.seed(seed=12)
             mcbeta  = self.ltg_beta+np.random.randn(self.nsample)*self.ltg_beta_sig          
             np.random.seed(seed=13)
             mcdelta = self.ltg_delta+np.random.randn(self.nsample)*self.ltg_delta_sig
             np.random.seed(seed=14)
             mcepsilon = self.ltg_epsilon+np.random.randn(self.nsample)*self.ltg_epsilon_sig
             # Compute the jitter samples        
             if hasattr(self,'CorFact'):
                  mcsigmarv = self.CorFact * mcalpha * mclumi**mcbeta * (mcteff/self.teffsun)**mcdelta * (mcgrav/self.gravsun)**mcepsilon
             else:
                  mcsigmarv = 1.93 * mcalpha * mclumi**mcbeta * (mcteff/self.teffsun)**mcdelta * (mcgrav/self.gravsun)**mcepsilon



          # Model 3: rvjitter = rvjitter(T, g)
          elif hasattr(self,'teff') & hasattr(self,'grav'): 
             np.random.seed(seed=15)
             mcteff = self.teff+np.random.randn(self.nsample)*self.tefferr
             np.random.seed(seed=16)
             mcgrav = self.grav+np.random.randn(self.nsample)*self.graverr
             np.random.seed(seed=17)
             mcalpha = self.tg_alpha+np.random.randn(self.nsample)*self.tg_alpha_sig
             np.random.seed(seed=18)
             mcdelta = self.tg_delta+np.random.randn(self.nsample)*self.tg_delta_sig            
             np.random.seed(seed=19)
             mcepsilon = self.tg_epsilon+np.random.randn(self.nsample)*self.tg_epsilon_sig            
             # Compute the jitter samples 
             if hasattr(self,'CorFact'):
                mcsigmarv = self.CorFact * mcalpha * (mcteff/self.teffsun)**mcdelta * (mcgrav/self.gravsun)**mcepsilon
             else:
                mcsigmarv = 2.01 * mcalpha * (mcteff/self.teffsun)**mcdelta * (mcgrav/self.gravsun)**mcepsilon                        




          # Model 4: rvjitter = rvjitter(L, T)
          elif hasattr(self,'lumi') & hasattr(self,'teff'): 
             np.random.seed(seed=20) #makes the random numbers predictable
             mclumi = self.lumi+np.random.randn(self.nsample)*self.lumierr 
             np.random.seed(seed=21)
             mcteff = self.teff+np.random.randn(self.nsample)*self.tefferr
             np.random.seed(seed=22)
             mcalpha = self.lt_alpha+np.random.randn(self.nsample)*self.lt_alpha_sig
             np.random.seed(seed=23)
             mcbeta = self.lt_beta+np.random.randn(self.nsample)*self.lt_beta_sig
             np.random.seed(seed=24)
             mcdelta = self.lt_delta+np.random.randn(self.nsample)*self.lt_delta_sig
             # Compute the jitter samples
             if hasattr(self,'CorFact'):
                mcsigmarv = self.CorFact * mcalpha * mclumi**mcbeta * (mcteff/self.teffsun)**mcdelta
             else: 
                mcsigmarv = 1.87 * mcalpha * mclumi**mcbeta * (mcteff/self.teffsun)**mcdelta
          else:  
               print('Input data does not apply to any of the four models')
               raise SystemExit



          # get rid of crazy simulated samples
          mcsigmarv = mcsigmarv[np.isfinite(mcsigmarv)]
          sigmarv=np.median(mcsigmarv)
          sigmarvperr=np.percentile(mcsigmarv,84.1)-sigmarv
          sigmarvmerr=sigmarv-np.percentile(mcsigmarv,15.9)
          sigmarverr = np.sqrt((sigmarvperr**2+sigmarvmerr**2)/2.)
          mcsigmarv = mcsigmarv[np.where(abs(mcsigmarv-sigmarv)<10*sigmarverr)[0]]


          # Compute median RV jitter and uncertainties.
          sigmarv=np.median(mcsigmarv)
          sigmarvperr=np.percentile(mcsigmarv,84.1)-sigmarv
          sigmarvmerr=sigmarv-np.percentile(mcsigmarv,15.9)


          self.sigmarv=sigmarv
          self.sigmarvperr=sigmarvperr
          self.sigmarvmerr=sigmarvmerr
          self.mcsigmarv=mcsigmarv
          return self.sigmarv, self.sigmarvperr, self.sigmarvmerr, self.mcsigmarv




      def plot(self, figshow=None, figsave=None, figname=None):
          """Plot Monte Carlo simulations of RV jitter"""
          self.rv()
          fig, ax = plt.subplots(1,1, figsize=(8,6))
          ax.tick_params(which='major', labelsize=20, direction='in', top=True, right=True, length=6, width=1.4)
          ax.tick_params(which='minor', labelsize=20, direction='in', top=True, right=True, length=3, width=1.4)
          for axis in ['top','bottom','left','right']: ax.spines[axis].set_linewidth(2.0)
          bins = np.linspace(min(self.mcsigmarv)*0.99, max(self.mcsigmarv)*1.01, num=100)
          posty, postx, patches = ax.hist(self.mcsigmarv, bins=bins, ec='b', color='gray', density=True)
          ax.plot([self.sigmarv, self.sigmarv], [0, max(posty)], 'r')
          ax.plot([self.sigmarv+self.sigmarvperr, self.sigmarv+self.sigmarvperr], [0, max(posty)], '--r')
          ax.plot([self.sigmarv-self.sigmarvmerr, self.sigmarv-self.sigmarvmerr], [0, max(posty)], '--r')
          minorLocator = AutoMinorLocator()
          ax.xaxis.set_minor_locator(minorLocator)
          minorLocator = AutoMinorLocator()
          ax.yaxis.set_minor_locator(minorLocator)
          ax.set_xlabel(r'$\sigma_{\rm rms, rv}\ [\rm m/s]$', fontsize=20)
          ax.set_ylabel('Probability Density', fontsize=20)
          ax.annotate(r'$\sigma_{\rm rms,\ RV}$', xy=(0.45, 0.9), xycoords="axes fraction", fontsize=18)
          ax.annotate(r'= {:.2f} +{:.2f} -{:.2f} [m/s]'.format(self.sigmarv, self.sigmarvperr, self.sigmarvmerr), xy=(0.58, 0.9), xycoords="axes fraction", fontsize=15)
          plt.tight_layout()
          if figsave==True: plt.savefig(figname) if figname is not None else plt.savefig('rvjitter.png')
          if figshow==True: plt.show()
          plt.close('all')
          return self.sigmarv, self.sigmarvperr, self.sigmarvmerr, self.mcsigmarv




