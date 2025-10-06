from data_generator import generator
gen = generator()

while True:
    imu_data, lc_data = next(gen)
    print(imu_data, lc_data)