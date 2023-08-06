import numpy as np
import matplotlib.pyplot as plt
import PyMieScatt


class single_distribute:
    def __init__(self, D_=590, sigma=0.15, start=300, end=900, count=51, random=False):
        self.D_ = 1E-9 * D_
        self.D = np.linspace(1E-9 * start, 1E-9 * end, 100, endpoint=True)
        self.sigma = sigma
        self.start, self.end, self.count = start, end, count
        self.random = random

    def calculate(self, D, D_, sigma):
        y0 = np.exp(-(np.power(np.log(D / D_), 2) / (2 * np.power(sigma, 2)))) / \
             (np.sqrt(2 * np.pi) * sigma * D * 10E5)
        return y0

    def fig(self):
        plt.figure(figsize=(8, 6), dpi=100)
        y = self.calculate(self.D, self.D_, self.sigma)
        plt.plot(self.D, y, color="green", linewidth=1.0, label="single")  # marker="^",dashes=[2,1]
        plt.xlabel("x", fontsize=13)
        plt.ylabel("f(x)", fontsize=13)
        plt.title("unimodal distribution")
        plt.legend(loc=1, handlelength=3, fontsize=13)  # 在右上角显示图例
        plt.show()

    def fetch(self):
        if self.random:
            seed_x = np.random.randint(self.start, self.end, size=self.count)
        else:
            seed_x = np.arange(self.start, self.end + 1, step=(self.end - self.start) / (self.count - 1))
        seed_x = np.multiply(seed_x, 1E-9)
        y = self.calculate(seed_x, self.D_, self.sigma)
        # plt.scatter(seed_x, y, color="red", linewidths=1)
        # plt.xlabel("diameter (m)", fontsize=13)
        # plt.ylabel("f(x)", fontsize=13)
        # plt.title("single peak psd")
        # plt.show()
        return seed_x, y


class multi_distribute:
    def __init__(self, d_list=[500, 800], sigma_list=[0.13, 0.045],
                 ratio_list=[0.8, 0.2], start=300, end=900, count=51, random=False):
        self.D_ = [1E-9 * i for i in d_list]
        self.D = np.linspace(30E-8, 100E-8, 200, endpoint=True)
        self.sigma = sigma_list
        self.ratio = ratio_list
        self.start, self.end, self.count = start, end, count
        self.random = random

    def calculate(self, x):
        def cal(D, D_, sigma):
            y0 = np.exp(-(np.power(np.log(D / D_), 2) / (2 * np.power(sigma, 2)))) / \
                 (np.sqrt(2 * np.pi) * sigma * D * 10E5)
            return y0

        num = 0
        for i in range(2):
            num = num + np.multiply(np.array(self.ratio[i]), cal(x, self.D_[i], self.sigma[i]))
        return num

    def fig(self):
        plt.figure(figsize=(8, 6), dpi=100)
        plt.plot(self.D, self.calculate(self.D), color="red", linewidth=1.0,
                 label="multiply")  # marker="^",dashes=[2,1]
        plt.xlabel("x", fontsize=13)
        plt.ylabel("f(x)", fontsize=13)
        plt.title("multimodal distribution")
        plt.legend(loc=1, handlelength=3, fontsize=13)  # 在右上角显示图例
        plt.show()

    def fetch(self):
        if self.random:
            seed_x = np.random.randint(self.start, self.end, size=self.count)
        else:
            seed_x = np.arange(self.start, self.end + 1, step=(self.end - self.start) / (self.count - 1))
        seed_x = np.multiply(seed_x, 1E-9)
        y = self.calculate(seed_x)
        # plt.scatter(seed_x, y, color="red", linewidths=1)
        # plt.xlabel("diameter (m)", fontsize=13)
        # plt.ylabel("f(x)", fontsize=13)
        # plt.title("double peak psd")
        # plt.show()
        return seed_x, y


def cumulate(theta,stamp, acf,n_surrounding=1.33, lambda0=532, viscosity=0.89, T=293):
    lambda0,viscosity = lambda0*1E-9, viscosity*1E-3
    Kb = 138E-25
    buffer = np.log(acf)
    coef = np.polyfit(stamp, buffer, stamp.shape[-1])
    poly = np.poly1d(coef)
    # print(coef,poly)
    Tao = 16 * np.pi * np.power(n_surrounding, 2) * Kb * T * np.power(np.sin(theta / 2), 2) / \
          (3 * viscosity * lambda0 ** 2)  # 散射矢量的模
    D_caculate = -Tao / coef[-2]
    return D_caculate


def mie_scatter(surrounding_index = 1.48,sphere_index = 2.63,radius=200,lambda0=532):
    surrounding_index = 1.48  # 介质折射率
    sphere_index = 2.63  # 球体折射率
    radius = 1E-9* radius  # 半径
    num_angle = 9000  # 在0-π中要求的点数
    lambda0 = lambda0*1E-9 / surrounding_index  # 光在介质中的波长
    raw_angle_array = np.array([i / num_angle for i in range(0, num_angle, 10)])
    angle_array = 180 * raw_angle_array
    radian_array = np.pi * raw_angle_array

    # 创建一个8x6大小的图像, dpi=80表示分辨率每英尺80点
    plt.figure(figsize=(8, 6), dpi=100)
    scatter_strength_list = []
    for radian in radian_array[:]:
        x = 2 * np.pi * radius / lambda0  # 尺寸参数：相对于波长的球体尺寸
        s1, s2 = PyMieScatt.MieS1S2(sphere_index/surrounding_index, x, np.cos(radian))
        scatter_strength = np.power(abs(s1), 2) + np.power(abs(s2), 2)
        scatter_strength_list.append(scatter_strength)
    plt.plot(angle_array, scatter_strength_list, color="red", linewidth=1.0, label=str(radius)+"nm")  # marker="^"
    plt.xlabel("x", fontsize=13)
    plt.ylabel("f(x)", fontsize=13)
    plt.title("scattering strength with scattering angles")
    plt.legend()  # 显示图例
    plt.show()


if __name__ == '__main__':
    # single1 = single_distribute()
    # single1.fetch()
    multi = multi_distribute()
    multi.fig()
    # cumulate()
