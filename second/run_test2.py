import numpy as np
from second.pointcloud_utils import pol2cart, reduce_resolution, cart2sph
import matplotlib.pyplot as plt

out = np.linspace(-np.pi, np.pi, 4000)

rho = np.ones(4000)

array = np.array([rho, out, rho, rho]).transpose()

cart_array = np.zeros([array.shape[0], array.shape[1]], dtype='f')

# Convert polar data to cartesian data
for i in range(len(array)):
    # print(f"i: {i}")

    x, y = pol2cart(array[i, 0], array[i, 1])

    cart_array[i] = np.array([x, y, array[i, 2], array[i, 3]], dtype='f')

# Convert cartesian to spherical
sph_array = np.zeros([cart_array.shape[0], cart_array.shape[1]], dtype='f')

for i in range(len(cart_array)):
    az, el, r = cart2sph(cart_array[i, 0], cart_array[i, 1], cart_array[i, 2])
    sph_array[i] = np.array([az, el, r, cart_array[i, 3]], dtype='f')




plt.scatter(sph_array[:,0], sph_array[:,1], s=0.5)
plt.ylabel('some numbers')
plt.show()

reduced = reduce_resolution(cart_array, 4096, 1024)

plt.scatter(reduced[:,0], reduced[:,1], s=0.5)
plt.ylabel('some numbers')
plt.show()

print("Done")
