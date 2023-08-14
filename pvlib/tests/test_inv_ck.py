from pvlib.inverter import ond_eff
from pvlib.iotools import parse_panond
import io
import pandas as pd
import numpy as np

inv_str = """PVObject_=pvGInverter
  Comment=ChintPower	CPS SCH275KTL-DO/US-800	Manufacturer 2020
  Version=6.81
  ParObj1=2020
  Flags=$00381562

  PVObject_Commercial=pvCommercial
    Comment=www.chintpower.com  (China)
    Flags=$0041
    Manufacturer=ChintPower
    Model=CPS SCH275KTL-DO/US-800
    DataSource=Manufacturer 2020
    YearBeg=2020
    Width=0.680
    Height=0.337
    Depth=1.100
    Weight=95.000
    NPieces=0
    PriceDate=02/06/20 00:02
    Currency=EUR
    Remarks, Count=2
      Str_1=Protection: -30 - +60, IP 66:  outdoor installable
      Str_2
    End of Remarks
  End of PVObject pvCommercial
  Transfo=Without

  Converter=TConverter
    PNomConv=250.000
    PMaxOUT=250.000
    VOutConv=800.0
    VMppMin=500
    VMPPMax=1500
    VAbsMax=1500
    PSeuil=500.0
    EfficMax=99.01
    EfficEuro=98.49
    FResNorm=0.00
    ModeOper=MPPT
    CompPMax=Lim
    CompVMax=Lim
    MonoTri=Tri
    ModeAffEnum=Efficf_POut
    UnitAffEnum=kW
    PNomDC=253.000
    PMaxDC=375.000
    IDCMax=0.0
    IMaxDC=360.0
    INomAC=181.0
    IMaxAC=199.0
    TPNom=45.0
    TPMax=40.0
    TPLim1=50.0
    TPLimAbs=60.0
    PLim1=225.000
    PLimAbs=90.000
    PInEffMax =150000.000
    PThreshEff=3332.4
    HasdefaultPThresh=False

    ProfilPIO=TCubicProfile
      NPtsMax=11
      NPtsEff=9
      LastCompile=$8085
      Mode=1
      Point_1=1250,0
      Point_2=7500,6923
      Point_3=12500,11875
      Point_4=25000,24250
      Point_5=50000,49100
      Point_6=75000,73875
      Point_7=150000,148515
      Point_8=250000,246500
      Point_9=275000,270325
      Point_10=0,0
      Point_11=0,0
    End of TCubicProfile
    VNomEff=880.0,1174.0,1300.0,
    EfficMaxV=98.260,99.040,98.860,
    EfficEuroV=97.986,98.860,98.661,

    ProfilPIOV1=TCubicProfile
      NPtsMax=11
      NPtsEff=9
      LastCompile=$8089
      Mode=1
      Point_1=300.0,0.0
      Point_2=13012.7,12500.0
      Point_3=25720.2,25000.0
      Point_4=51093.4,50000.0
      Point_5=76437.0,75000.0
      Point_6=127213.5,125000.0
      Point_7=190995.2,187500.0
      Point_8=255440.9,250000.0
      Point_9=281301.1,275000.0
      Point_10=0.0,0.0
      Point_11=0.0,0.0
    End of TCubicProfile

    ProfilPIOV2=TCubicProfile
      NPtsMax=11
      NPtsEff=9
      LastCompile=$8089
      Mode=1
      Point_1=300.0,0.0
      Point_2=12850.8,12500.0
      Point_3=25401.3,25000.0
      Point_4=50581.7,50000.0
      Point_5=75795.9,75000.0
      Point_6=126211.6,125000.0
      Point_7=189623.8,187500.0
      Point_8=253138.9,250000.0
      Point_9=278763.3,275000.0
      Point_10=0.0,0.0
      Point_11=0.0,0.0
    End of TCubicProfile

    ProfilPIOV3=TCubicProfile
      NPtsMax=11
      NPtsEff=9
      LastCompile=$8089
      Mode=1
      Point_1=300.0,0.0
      Point_2=12953.4,12500.0
      Point_3=25512.8,25000.0
      Point_4=50679.1,50000.0
      Point_5=75895.6,75000.0
      Point_6=126441.4,125000.0
      Point_7=189835.0,187500.0
      Point_8=253472.6,250000.0
      Point_9=279017.9,275000.0
      Point_10=0.0,0.0
      Point_11=0.0,0.0
    End of TCubicProfile
  End of TConverter
  NbInputs=36
  NbMPPT=12
  TanPhiMin=-0.750
  TanPhiMax=0.750
  NbMSInterne=2
  MasterSlave=No_M_S
  IsolSurvey =Yes
  DC_Switch=Yes
  MS_Thresh=0.8
  Night_Loss=5.00
End of PVObject pvGcomperter
"""
f_obj = io.StringIO(inv_str)
inv = parse_panond(f_obj)

df = pd.read_csv('C:/Users/Contractor1/Downloads/ond_eff_test.csv')
# dc_v_mpp = df[['v_0','v_1','v_2','v_3','v_4','v_5','v_6','v_7','v_8','v_9']]
# dc_i_mpp = df[['i_0','i_1','i_2','i_3','i_4','i_5','i_6','i_7','i_8','i_9']]
mps = 28
spi = 28.75

select_v = df[['v_0', 'v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_6', 'v_7', 'v_8', 'v_9']] * mps
select_i = df[['i_0', 'i_1', 'i_2', 'i_3', 'i_4', 'i_5', 'i_6', 'i_7', 'i_8', 'i_9']] * spi
dc_v = select_v.values
dc_i = select_i.values

test_out = ond_eff(df['dc_p_mpp'] * mps * spi, df['dc_v_mpp'] * mps, dc_v, dc_i, inv, tamb=df['Tamb'])
# TODO: !!! NEED to test with central inverter .ond
stop = 1