import time
import numpy as np
import matplotlib.pyplot as plt
import PyMieScatt
import utils
from tqdm import tqdm


class generator:
    def __init__(self, n_surrounding=1.33, sphere_index=1.59, lambda0=532, viscosity=0.89,
                 T=293, single=True, theta_list=None):
        '''
        draw_fig:  是否绘图，记得改plt.show()的位置
        method:  "line":数据集特征是电场自相关曲线,"cumulate":数据集特征是累积量计算结果
        '''
        self.n_surrounding, self.sphere_index, self.lambda0, = n_surrounding, sphere_index, lambda0 * 1E-9
        self.viscosity, self.T, self.Kb = viscosity * 1E-3, T, 138E-25
        self.single = single

        if theta_list is None:
            self.theta_list = [np.pi / 4]
        else:
            self.theta_list = theta_list
        self.n = len(self.theta_list)  # 输入向量的维度。后面会多次用到
        self.Tao = np.zeros(self.n)

    def check(self, Dg_list, sigma_list, ratio_list):
        if self.single:
            assert (len(Dg_list) == len(sigma_list)) and (len(Dg_list) != 0) and (
                    len(sigma_list) != 0), "the shape of dg and sigma should be same!(!=0)"
            Dg_list, sigma_list, ratio_list = Dg_list, sigma_list, [0]
        else:
            assert len(Dg_list[0]) == 2, "you should provide two values for each element of Dg_list"
            assert len(sigma_list[0]) == 2, "you should provide two values for each element of sigma_list"
            assert len(np.array(ratio_list).shape) == 1, "the shape if ratio_list should be (1,-1)"
            ratio_list_all = []
            for big in ratio_list:
                ratio_list_all.append([big, 1 - big])
            ratio_list = ratio_list_all
        return Dg_list, sigma_list, ratio_list

    def generate(self, Dg_list=None, sigma_list=None, ratio_list=None, start=100, end=1200,
                 count=51, time_series=None, method="cumulate"):
        Dg_list, sigma_list, ratio_list = self.check(Dg_list, sigma_list, ratio_list)
        data_x, data_y = [], []
        for ratio in ratio_list:
            pbar = tqdm(Dg_list, total=len(Dg_list), leave=True, ncols=150, unit="个", unit_scale=False, colour="red")
            for idx, Dg in enumerate(pbar):
                pbar.set_description(f"Epoch {idx}/{len(Dg_list)}")
                start_time = time.perf_counter()
                for sigma in sigma_list:
                    result0, result1 = self.electric_line(Dg, sigma, ratio, start=start, end=end,
                                                          count=count, time_series=time_series, method=method)
                    data_x.append(result0)
                    data_y.append(result1)
                end_time = time.perf_counter()
                pbar.set_postfix({"正在处理的中心粒径": Dg, "双峰加权系数": ratio[0]}, cost_time=(end_time - start_time))
        data_x, data_y = np.array(data_x), np.array(data_y)
        print(f"the shape of x is {data_x.shape}, the shape of y is {data_y.shape}")
        return data_x, data_y

    def electric_line(self, Dg, sigma, ratio, start=100, end=1200, count=51, time_series=None,
                      method="line", add_noise=False, noise_level=0.001):
        if self.single:
            single = utils.single_distribute(random=False, D_=Dg, sigma=sigma,
                                             start=start, end=end, count=count)
            D_list, f_D = single.fetch()  # 获取仿真所得的粒径数据(单位是nm）和分布
        else:
            multi = utils.multi_distribute(random=False, d_list=Dg, sigma_list=sigma,
                                           ratio_list=ratio, start=start, end=end, count=count)
            D_list, f_D = multi.fetch()  # 获取仿真所得的粒径数据(单位是nm）和分布

        k_theta = np.zeros(self.n)  # 存储散射角的权重系数
        strength_list = np.zeros((self.n, D_list.shape[0]))  # 存储mie散射光强分数的二维数组
        h_theta = np.zeros((self.n, D_list.shape[0]))  # 存储电场自相关系数的二维数组
        D_theta = np.zeros(self.n)  # 输入GRNN神经网络中的输入向量
        G_theta = np.zeros(self.n)  # 存储各个散射角处光强自相关函数基线值
        for index0 in range(self.n):  # 开始对每个散射角进行遍历求解
            for index1 in range(D_list.shape[0]):
                # 尺寸参数：相对于波长的球体尺寸
                x = 2 * np.pi * D_list[index1] * self.n_surrounding / self.lambda0
                s1, s2 = PyMieScatt.MieS1S2(
                    self.sphere_index / self.n_surrounding,
                    x, np.cos(self.theta_list[index0]))
                scatter_strength = np.power(abs(s1), 2) + np.power(abs(s2), 2)
                strength_list[index0][index1] = scatter_strength
            light_summary = np.sum(strength_list[index0])  # 二维数组中axis=1是按行相加
            strength_list[index0] = np.divide(strength_list[index0], light_summary)  # 散射光强分数矩阵
            CIxfD = np.multiply(strength_list[index0], f_D)
            G_theta[index0] = 10E-7 * np.power(np.sum(CIxfD), 2)
            k_theta[index0] = 1 / np.sum(CIxfD)
            D_theta[index0] = np.sum(CIxfD) / \
                              np.matmul(strength_list[index0],
                                        np.divide(f_D, D_list))  # 计算输入到GRNN网络中的特征向量数值
            # print(k_theta)
            h_theta[index0] = np.multiply(k_theta[index0], CIxfD)
        # print(h_theta, np.sum(h_theta, axis=1))  # 验证h_theta的累计和为1
        # print(D_theta, f_D)  # 分别打印输入和输出
        if method == "cumulate":
            return D_theta, f_D

        elif method == "line":
            if time_series is None:
                self.t = np.logspace(np.log10(1E-5), np.log10(5), 50, base=10.0, endpoint=True)  # 时间间隔
            else:
                self.t = time_series
            buffer = []
            for i in range(self.n):
                Tao = 16 * np.pi * np.power(self.n_surrounding, 2) * self.Kb * self.T * np.power(
                    np.sin(self.theta_list[i] / 2), 2) / \
                      (3 * self.viscosity * self.lambda0 ** 2)  # 散射矢量的模
                self.Tao[i] = Tao
                y = []
                for tt in self.t[:]:
                    yy = np.multiply(h_theta[i], np.exp(-Tao * tt / D_list))
                    yy = np.sum(yy)
                    y.append(yy)
                if add_noise:
                    li_x = np.random.normal(loc=0, scale=1, size=self.t.shape[0])
                    y = li_x * noise_level + np.array(y)
                buffer.append(y)
            return buffer, f_D
        else:
            print("please confirm the method you want to use!")

    def cumulate(self, tao, acf):  # 每个角度处的累积量法计算
        buffer = np.log(acf)
        coef = np.polyfit(self.t, buffer, acf.shape[0])
        D_caculate = -tao / coef[-2]  # 指数项为1的系数
        return D_caculate


if __name__ == '__main__':
    data = generator(single=True, theta_list=[np.pi / 4, np.pi / 2])
    t = np.logspace(np.log10(1E-5), np.log10(5), 50, base=10.0, endpoint=True)
    # data.generate([[300,500]],[[0.1,0.2]],[0.8,0.7],time_series=t,method="cumulate")
    a, _ = data.electric_line(500, 0.2, 0.8, time_series=t, method="line",add_noise=True,noise_level=0.001)
    print(a)
    for aa in a:
        plt.semilogx(t, aa, color="red", linewidth=1)
        plt.show()
