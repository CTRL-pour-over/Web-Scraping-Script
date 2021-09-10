from pandas import DataFrame
import test as t
    
print(t.li_Vendor ,len(t.li_Vendor))
print(t.li_Strain ,len(t.li_Strain))
print(t.li_Straintype ,len(t.li_Straintype))
print(t.li_Weight ,len(t.li_Weight))
print(t.li_THC_Contents ,len(t.li_THC_Contents))
print(t.li_CBD_Contents ,len(t.li_CBD_Contents))
print(t.li_Type ,len(t.li_Type))
print(t.li_Price ,len(t.li_Price))
print(t.li_THCwt ,len(t.li_THCwt))
print(t.li_PpTHC ,len(t.li_PpTHC))

dict = {
    "----Vendor----": t.li_Vendor,
    "----Strain----": t.li_Strain,
    "-------Straintype-------": t.li_Straintype,
    "----Weight----": t.li_Weight,
    "----THC_Contents----": t.li_THC_Contents,
    "----Type----": t.li_Type,
    "----Price----": t.li_Price,
    "----mg of THC----": t.li_THCwt,
    "----Price Per mg of THC----": t.li_PpTHC
    }

df = DataFrame(dict)
print(df)