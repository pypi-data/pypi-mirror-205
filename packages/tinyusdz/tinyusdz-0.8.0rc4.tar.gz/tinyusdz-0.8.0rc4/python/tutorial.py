import tinyusdz

print("TinyUSDZ version", tinyusdz.version.version) # str
print("TinyUSDZ major_version", tinyusdz.version.major_version) # int
print("TinyUSDZ minor_version", tinyusdz.version.minor_version) # int
print("TinyUSDZ micro_version", tinyusdz.version.micro_version) # int

print("numpy available? ", tinyusdz.is_numpy_available()) # bool
print("pandas available? ", tinyusdz.is_pandas_available()) # bool

filename = "../models/suzanne.usdc"

if not tinyusdz.is_usd(filename):
    print("File is not a USD(USDA/USDC/USDZ) file.", filename)

stage = tinyusdz.load_usd(filename)

print(stage)
